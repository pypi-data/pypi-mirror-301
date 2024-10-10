import datetime
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

from tqdm import tqdm

from lbgcli.module_impl import Module, append_format_to_parser, TableResult, TolerantException
from lbgcli.util import query_yes_no, download
from lbgcore.client import RequestInfoException


class JobGroupModule(Module):

    def __init__(self, cli):
        super().__init__(cli)

    def add_to_parser(self, subparser):
        self.parser = subparser.add_parser('jobgroup', help='Operating Job Group Module')
        self.parser.set_defaults(func=lambda _: self.parser.print_help())
        self.sub_parser = self.parser.add_subparsers()
        self.load_ls()
        self.load_terminate()
        self.load_delete()
        self.load_download()
        self.load_create()

    def load_create(self):
        parser_tm = self.sub_parser.add_parser('create', help='create job group')
        parser_tm.set_defaults(func=lambda args: self.func_create(args))
        parser_tm.add_argument('-n', '--name', action='store', help='name of the job group')
        parser_tm.add_argument('-pjid', '--project_id', action='store', help='project id of the job group')

    def func_create(self, args):
        name = args.name
        project_id = args.project_id
        if not name:
            raise ValueError(f'name is required, can add it by -n')
        try:
            pjid = int(project_id)
        except:
            raise ValueError(f'project_id is required, can add it by -pjid')
        
        result = self.cli.client.job_group.create(pjid, name)
        self.cli.print(result)

    def load_ls(self):
        parser_ls = self.sub_parser.add_parser('ls', help='list all job group')
        parser_ls.set_defaults(func=lambda args: self.func_ls(args))

        parser_ls.add_argument('-q', '--quiet', action='store_true', help='only show job group id')
        parser_ls.add_argument('-s', '--start', action='store',
                               type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                               help='default is a day ago. format is yyyy-mm-dd')
        parser_ls.add_argument('-e', '--end', action='store', type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                               help='default is a day today. format is yyyy-mm-dd')
        parser_ls.add_argument('-k', '--search', action='store', type=str,
                               help='allow search id/name')
        parser_ls.add_argument('-o', '--sortby', action='store', type=str,
                               help='sort by id/createTime default is id')
        parser_ls.add_argument('-as', '--asce', action='store_true',
                               help='list by ascending, default descending')
        parser_ls.add_argument('-l', '--long', action='store_true', help='long listing format')

        append_format_to_parser(parser_ls)
        parser_ls.add_argument('-n', '--number', action='store', type=int, default=50,
                               help='number of result to be display, default 50')

    def func_ls(self, args):
        params = {}
        if args.start:
            params['start_date'] = args.start
        if args.end:
            if args.end > datetime.now():
                raise ValueError(f'end date can not set to future. ({args.end})')
            if args.start and (args.end < args.start):
                raise ValueError(f'start date ({args.start}) can not less than end date ({args.end})')
            params['end_date'] = args.end
        if args.search:
            params['search_key'] = args.search
        if args.sortby:
            params['sort_by'] = args.sortby

        if args.asce:
            params['reverse'] = True
        else:
            params['reverse'] = False

        result = self.cli.client.job_group.list_job_group_by_number(self.cli.program_id(), args.number, **params)

        def mapper_func(each_value):
            each_value['Success Count'] = each_value['status'][0]
            each_value['Fail Count'] = each_value['status'][1]
            each_value['Running Count'] = each_value['status'][2]
            each_value['Pending Count'] = each_value['status'][3]
            each_value['spendTime'] = str(timedelta(seconds=each_value['spendTime']))
            if not args.long:
                del each_value['status']
            return each_value

        tr = TableResult(result, first_col='id', columns_order=['id', 'jobName'],
                         no_header=args.noheader, default_format=self.cli.output_format(), mapper_func=mapper_func)
        if args.quiet:
            for each in tr.data:
                self.cli.print(each['id'])
            return
        result = tr.output(args)
        self.cli.print(result)

    def load_terminate(self):
        parser_tm = self.sub_parser.add_parser('terminate', help='terminate selected job group')
        parser_tm.set_defaults(func=lambda args: self.func_terminate(args))
        parser_tm.add_argument('jobgroup_id', nargs='+', type=int, help='id of the job group')
        parser_tm.add_argument('-f', '--force', action='store_true', help='force terminate job group')

    def func_terminate(self, args):
        ids = args.jobgroup_id
        force = args.force
        for each in ids:
            if not force:
                if not query_yes_no(f'do you want to terminate this job group with id: {each}', default='no'):
                    continue
            result = self.cli.client.job_group.terminate(each)
            if result == {}:
                self.cli.print(f'successfully terminate job group with id: {each}')

    def load_delete(self):
        parser_tm = self.sub_parser.add_parser('rm', help='delete selected job group')
        parser_tm.set_defaults(func=lambda args: self.func_delete(args))
        parser_tm.add_argument('jobgroup_id', nargs='+', type=int, help='id of the job group')
        parser_tm.add_argument('-f', '--force', action='store_true', help='force delete job group')

    def func_delete(self, args):
        ids = args.jobgroup_id
        force = args.force
        for each in ids:
            if not force:
                if not query_yes_no(f'do you want to delete this job group with id: {each}', default='no'):
                    continue
            result = self.cli.client.job_group.delete(each)
            if result == {}:
                self.cli.print(f'successfully delete job group with id: {each}')

    def load_download(self):
        parser_tm = self.sub_parser.add_parser('download', help='download selected job group')
        parser_tm.set_defaults(func=lambda args: self.func_download(args))
        parser_tm.add_argument('jobgroup_id', nargs='+', type=int, help='id of the job group')
        parser_tm.add_argument('-p', '--path', action='store', help='download location default current dir')
        parser_tm.add_argument('-pr', '--parent', action='store_true', help='create parent dir if needed')

    def func_download(self, args):
        ids = args.jobgroup_id
        if args.path:
            target = args.path
        else:
            target = os.getcwd()
        p = Path(target)
        if not p.exists():
            if args.parent:
                p.mkdir(exist_ok=True, parents=True)
            else:
                p.mkdir(exist_ok=True)
        bar_format = "{l_bar}{bar}| {n:.02f}/{total:.02f} %  [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
        parent_bar = tqdm(total=len(ids), desc="Downloading JobGroup", bar_format=bar_format)
        download_paths = []
        failed = {}
        for each in ids:
            parent_bar.set_description("Downloading JobGroup " + str(each))
            group_path = p.joinpath(str(each))
            id_in_job_group = []
            result = self.cli.client.job.list_by_number(each, -1)
            for each_value in result:
                id_in_job_group.append(each_value['id'])
            sub_bar = tqdm(total=len(id_in_job_group), desc="Downloading Job", bar_format=bar_format, leave=False)
            failed[each] = self.download_jobs(id_in_job_group, group_path, sub_bar)
            sub_bar.close()
            parent_bar.update(1)
            download_paths.append((each, group_path.absolute()))
        parent_bar.close()
        for (k, v) in failed.items():
            for each in v:
                self.cli.print(f'job group {k}, job id {each} fail to download skipped')
        for (k, v) in download_paths:
            self.cli.print(f'job group {k} download to {v}')

    def download_jobs(self, job_ids, target, sub_bar):
        failed_id = []
        for each in job_ids:
            try:
                result = self.cli.client.job.detail(each)
                sub_bar.set_description("Downloading Job " + str(each))
                if result.get('resultUrl'):
                    u = result.get('resultUrl')
                    suf = Path(urllib.parse.urlparse(u).path).suffix
                    p = Path(target)
                    result_path = Path(result.get('result'))
                    if not p.exists():
                        p.mkdir(exist_ok=True, parents=True)
                    target_path = Path(target).joinpath(str(result['id']))
                    if not download(result.get('resultUrl'), target_path, suffix=suf):
                        failed_id.append(each)
                else:
                    failed_id.append(each)
            except(TolerantException, RequestInfoException, Exception) as e:
                failed_id.append(each)
            sub_bar.update(1)
        return failed_id
