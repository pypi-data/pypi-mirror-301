import re
import json
import os
import sys
import traceback
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from shutil import make_archive
import oss2
import requests
import yaml
from oss2 import determine_part_size, SizedFileAdapter
from oss2.models import PartInfo
from tqdm import tqdm
from colorama import Fore

from lbgcli import util
from lbgcli.const import GlobalConfig, PROD_ENV
# from lbgcli.job._jcc import JCCOperator
from lbgcli.module_impl import Module, append_format_to_parser, TableResult, TolerantException
from lbgcli.util import query_yes_no, zip_dir, download, base64url_decode

LAUNCHING_URN_RE = re.compile(r'^launching\+(?P<type>datasets|models)://(?P<element>.*?)(@(?P<version>.*))?$')


class JobModule(Module):

    def __init__(self, cli):
        super().__init__(cli)

    def add_to_parser(self, subparser):
        self.parser = subparser.add_parser('job', help='Operating Job Module')
        self.parser.set_defaults(func=lambda _: self.parser.print_help())
        self.sub_parser = self.parser.add_subparsers()
        self.load_ls()
        self.load_delete()
        self.load_kill()
        self.load_terminate()
        self.load_log()
        self.load_submit()
        self.load_download()
        self.load_describe()
        # self.load_jcc()

    def load_ls(self):
        parser_ls = self.sub_parser.add_parser('ls', help='list all job')
        parser_ls.set_defaults(func=lambda args: self.func_ls(args))
        parser_ls.add_argument('-jg', '--job_group_id', action='store', type=int, help='job group id')
        parser_ls.add_argument('-l', '--long', action='store_true', help='long listing format')
        parser_ls.add_argument('-fa', '--fail', action='store_const', const=-1, help='only show failed job')
        parser_ls.add_argument('-pe', '--pending', action='store_const', const=0, help='only show pending job')
        parser_ls.add_argument('-ru', '--running', action='store_const', const=1, help='only show running job')
        parser_ls.add_argument('-fi', '--finished', action='store_const', const=2, help='only show finished job')
        parser_ls.add_argument('-sc', '--scheduling', action='store_const', const=3, help='only show scheduling job')
        parser_ls.add_argument('-st', '--stopping', action='store_const', const=4, help='only show stopping job')
        parser_ls.add_argument('-sp', '--stopped', action='store_const', const=5, help='only show stopped job')
        parser_ls.add_argument('-q', '--quiet', action='store_true', help='only show job id')
        append_format_to_parser(parser_ls)
        parser_ls.add_argument('-n', '--number', action='store', type=int, default=-1,
                               help='number of result to be display, default 10')

    def func_ls(self, args):
        jgid = -1
        if args.job_group_id:
            jgid = args.job_group_id
        status = []
        if args.fail is not None:
            status.append(args.fail)
        if args.pending is not None:
            status.append(args.pending)
        if args.running is not None:
            status.append(args.running)
        if args.finished is not None:
            status.append(args.finished)
        if args.scheduling is not None:
            status.append(args.scheduling)
        if args.stopping is not None:
            status.append(args.stopping)
        if args.stopped is not None:
            status.append(args.stopped)

        def mapper(v):
            out = {}
            out['id'] = v['id']
            out['jobName'] = v['jobName']
            out['jobGroupId'] = v.get('jobGroupId') and str(v['jobGroupId']) or '-'
            out['jobGroupName'] = v.get('jobGroupName') and v['jobGroupName'] or '-'
            out['spendTime'] = v['spendTime']
            out['status'] = self.job_status_to_str(v['webStatus'])
            out['cost'] = v['cost']
            out['errorInfo'] = v.get('errorInfo') and v['errorInfo'] or '-'
            out['createTime'] = v['createTime']
            out['projectName'] = v.get('projectName') and v['projectName'] or '-'
            out['endTime'] = v['endTime']
            out['exitCode'] = v['exitCode']
            return out

        if args.number and args.number <= 0:
            args.number = 10
        result = self.cli.client.job.list_by_number(jgid, args.number, status=status)
        tr = TableResult(result, first_col='id', columns_order=['id', 'jobName', 'jobGroupId'],
                         no_header=args.noheader, mapper_func=mapper, default_format=self.cli.output_format())
        if args.quiet:
            for each in tr.data:
                self.cli.print(each['id'])
            return
        result = tr.output(args)
        self.cli.print(result)

    def load_delete(self):
        parser_tm = self.sub_parser.add_parser('rm', help='delete selected job')
        parser_tm.set_defaults(func=lambda args: self.func_delete(args))
        parser_tm.add_argument('job_ids', nargs='+', type=int, help='id of the job')
        parser_tm.add_argument('-f', '--force', action='store_true', help='force delete job')

    def job_status_to_str(self, status):
        if status == -1:
            return 'Failed'
        elif status == 0:
            return 'Pending'
        elif status == 1:
            return 'Running'
        elif status == 2:
            return 'Finished'
        elif status == 3:
            return 'Scheduling'
        elif status == 4:
            return 'Stopping'
        elif status == 5:
            return 'Stopped'
        elif status == 6:
            return 'Terminating'
        elif status == 7:
            return 'Killing'
        elif status == 8:
            return 'Uploading'
        elif status == 9:
            return 'Wait'
        else:
            return f'Unknown {status}'

    def func_delete(self, args):
        job_ids = args.job_ids
        force = args.force
        for each in job_ids:
            if not force:
                if not query_yes_no(f'do you want to delete this job with id: {each}', default='no'):
                    continue
            result = self.cli.client.job.delete(each)
            if result == {}:
                self.cli.print(f'successfully delete job with id: {each}')

    def load_terminate(self):
        parser_tm = self.sub_parser.add_parser('terminate', help='terminate selected job')
        parser_tm.set_defaults(func=lambda args: self.func_terminate(args))
        parser_tm.add_argument('job_id', nargs='+', type=int, help='id of the job')
        parser_tm.add_argument('-f', '--force', action='store_true', help='force terminate job')

    def func_terminate(self, args):
        job_ids = args.job_id
        force = args.force
        for each in job_ids:
            if not force:
                if not query_yes_no(f'do you want to terminate this job with id: {each}', default='no'):
                    continue
            result = self.cli.client.job.terminate(each)
            if result == {}:
                self.cli.print(f'successfully terminate job with id: {each}')

    def load_kill(self):
        parser_tm = self.sub_parser.add_parser('kill', help='kill selected job')
        parser_tm.set_defaults(func=lambda args: self.func_kill(args))
        parser_tm.add_argument('job_ids', nargs='+', type=int, help='id of the job')
        parser_tm.add_argument('-f', '--force', action='store_true', help='force kill job')

    def func_kill(self, args):
        job_ids = args.job_ids
        force = args.force
        for each in job_ids:
            if not force:
                if not query_yes_no(f'do you want to kill this job with id: {each}', default='no'):
                    continue
            result = self.cli.client.job.kill(each)
            if result == {}:
                self.cli.print(f'successfully kill job with id: {each}')

    def load_log(self):
        parser_tm = self.sub_parser.add_parser('log', help='show selected job log')
        parser_tm.set_defaults(func=lambda args: self.func_log(args))
        parser_tm.add_argument('-o', '--out', action='store', help='save file location')
        parser_tm.add_argument('job_ids', nargs='+', type=int, help='id of the job')

    def func_log(self, args):
        job_ids = args.job_ids
        for each in job_ids:
            if args.out:
                result = self.cli.client.job.detail(each)
                if not result.get('jobFiles'):
                    self.cli.print(f'job id: {each} does not have job files yet.')
                    continue

                logFiles = result['jobFiles'].get('logFiles')
                for logFile in logFiles:
                    if not logFile.get('url'):
                        self.cli.print(f'job id: {each} does not have log yet.')
                        continue

                    p = Path(args.out).joinpath(str(result['id'])).joinpath(logFile['name'])
                    outPath = p.parent
                    if not outPath.exists():
                        outPath.mkdir(exist_ok=True, parents=True)
                    if not download(logFile['url'], p, suffix=""):
                        self.cli.print(f'job id: {each} does not have log: {logFile["name"]} yet.')
            else:
                result = self.cli.client.job.log(each)
                log = ''
                try:
                    if 'log' not in result:
                        log = f"job: {each} does not have log yet."
                    else:
                        try:
                            log = json.loads(result.get('log')).get('log')
                            if isinstance(log, list):
                                log = '\n'.join(log)
                        except:
                            log = result.get('log')
                except Exception as e:
                    traceback.print_exc()
                self.cli.print(log)

    def load_submit(self):
        parser_tm = self.sub_parser.add_parser('submit', help='submit job')
        parser_tm.set_defaults(func=lambda args: self.func_submit_v2(args))
        parser_tm.add_argument('-i', '--file', action='store', help='predefined file')
        parser_tm.add_argument('-p', '--input', action='store', nargs='*', help='input file location')
        parser_tm.add_argument('-jt', '--job_type', action='store', help='indicate/container')
        parser_tm.add_argument('-jgid', '--job_group_id', action='store', type=int, help='job group id')
        parser_tm.add_argument('-pjid', '--project_id', action='store', type=int,
                               help='project id, will overwrite default')
        parser_tm.add_argument('-n', '--job_name', action='store', help='name')
        parser_tm.add_argument('-im', '--image_name', action='store', help='image name')
        parser_tm.add_argument('-ds', '--disk_size', action='store', help='disk size (GB)')
        parser_tm.add_argument('-sc', '--scass_type', action='store', help='scass type')
        parser_tm.add_argument('-mt', '--machine_type', action='store', help='machine type')
        parser_tm.add_argument('-nn', '--nnode', action='store', type=int, help='nnode')
        parser_tm.add_argument('-igid', '--instance_group_id', action='store', type=int, help='instance group id')
        parser_tm.add_argument('-c', '--cmd', action='store', help='command')
        parser_tm.add_argument('-l', '--log_file', action='store', help='log file location')
        parser_tm.add_argument('-o', '--out_files', action='store', help='log file location', nargs='*')
        parser_tm.add_argument('-pf', '--platform', action='store', help='ali/sugon')
        parser_tm.add_argument('-rg', '--region', action='store', help='region name')
        parser_tm.add_argument('-r', '--result', action='store', help='download result')
        parser_tm.add_argument('-odm', '--on_demand', action='store', type=int, help='0:spot(default) 1:on_demand ')
        parser_tm.add_argument('-ckptt', '--checkpoint_time', action='store', type=int, help='checkpoint time (minute)')
        parser_tm.add_argument('-ckptf', '--checkpoint_files', action='store', help='checkpoint file', nargs='?')
        parser_tm.add_argument('-dpb', '--disable_progress', action='store_true', help='disable progress bar')
        parser_tm.add_argument('-oji', '--only_job_id', action='store_true', help='only show job id')
        parser_tm.add_argument('-ojgi', '--only_job_group_id', action='store_true', help='only show job id')
        parser_tm.add_argument('-ckmt', '--check_machine_type', action='store', type=int, help='check machine_type')

    def func_submit_v2(self, args):
        data = {}
        if args.file:
            p = Path(args.file)
            d = {}
            if p.suffix == '.json':
                d = json.loads(p.read_text())
            elif p.suffix == '.yaml' or p.suffix == '.yml':
                d = yaml.safe_load(p.read_text())
            else:
                raise ValueError('unsupported file formate, current support are json yaml yml.')
            for k, v in d.items():
                if k == "backward_files":
                    data["out_files"] = v
                else:
                    if v:
                        data[k] = v
        if args.job_type:
            data['job_type'] = args.job_type
        else:
            if 'job_type' not in data:
                data['job_type'] = 'indicate'
        if args.job_group_id:
            data['job_group_id'] = args.job_group_id
        if args.project_id:
            data['project_id'] = args.project_id
        else:
            if 'project_id' not in data:
                if 'program_id' in data:
                    data['project_id'] = data['program_id']
                else:
                    data['project_id'] = self.cli.program_id()
        if args.job_name:
            data['job_name'] = args.job_name
        if args.image_name:
            data['image_name'] = args.image_name
        if args.disk_size:
            data['disk_size'] = args.disk_size
        if 'machine_type' in data:
            data['scass_type'] = data['machine_type']
        if args.scass_type:
            data['scass_type'] = args.scass_type
        if args.machine_type:
            data['scass_type'] = args.machine_type
        if args.nnode:
            data['nnode'] = args.nnode
        if args.instance_group_id:
            data['instance_group_id'] = args.instance_group_id
        if args.cmd:
            data['cmd'] = args.cmd
        else:
            if 'command' in data:
                data['cmd'] = data['command']
        if args.log_file:
            data['log_file'] = args.log_file
        if args.out_files:
            data['out_files'] = args.out_files
        if args.platform:
            data['platform'] = args.platform
        if args.region:
            data['region'] = args.region
        if args.on_demand:
            data['on_demand'] = args.on_demand
        if data.get('image_address') and not data.get('image_name'):
            data['image_name'] = data.get('image_address')
        if args.result or 'result' in data:
            result_path = args.result if args.result else data['result']
            ep = os.path.expanduser(result_path)
            p = Path(ep).absolute().resolve()
            p = p.joinpath(str(uuid.uuid4()) + "_temp.zip")
            data['download_path'] = str(p.absolute().resolve())
            retry = 7
            get_id_ok = False
            for i in range(retry):
                try:
                    if not util.is_bohr_instance():
                        break
                    resp = requests.get("http://100.100.100.200/latest/meta-data/instance-id", timeout=2)
                    resp.raise_for_status()
                    data['cli_instance_id'] = resp.text
                    get_id_ok = True
                    break
                except:
                    pass
            if not get_id_ok:
                self.cli.warn("current node is not belong to Bohrium, auto download is disable")
        if args.checkpoint_time:
            data['checkpoint_time'] = args.checkpoint_time
        if args.checkpoint_files:
            data['checkpoint_files'] = args.checkpoint_files
        if args.input or data.get('input'):
            inputs = []
            if args.input is not None:
                if isinstance(args.input, list):
                    inputs.extend(args.input)
                elif isinstance(args.input, str):
                    inputs.append(args.input)
            if data.get('input'):
                input_data = data.get('input')
                if isinstance(input_data, list):
                    inputs.extend(input_data)
                elif isinstance(input_data, str):
                    inputs.append(input_data)
            group_id = 0
            bohr_group_id = 0
            if data.get('job_group_id'):
                group_id = int(data.get('job_group_id'))
            elif data.get('bohrGroupId') or data.get('bohr_group_id'):
                bohr_group_id = int(data.get('bohrGroupId') or data.get('bohr_group_id'))
            res = self.cli.client.job.create(int(data['project_id']), name=data.get('job_name'),
                                             group_id=group_id, bohr_group_id=bohr_group_id)
            result_input = []
            prefix = Path(res['storePath']).joinpath('input').as_posix()
            # data['job_group_id'] = res['jobGroupId']
            app_key = ''
            tag = ''
            token = res['token']
            try:
                b = str.encode(token.split(".")[1])
                decoded = base64url_decode(b)
                claims = json.loads(decoded)
                app_key = claims['appKey']
                tag = claims['tag']
            except Exception as e:
                raise ValueError(f'storage token error, {e}')
            data['job_id'] = res['jobId']
            input_path = ''
            for each in inputs:
                if each.startswith('http://') or each.startswith('https://'):
                    result_input.append(each)
                    continue
                elif '=' in each:
                    param_name, param_value = each.split('=', 1)
                    matched = LAUNCHING_URN_RE.match(param_value)
                    if matched:
                        type = matched.group('type')
                        version = matched.group('version') or 'latest'
                        element = matched.group('element')
                        mount_type = 'rw' if version == 'draft' else 'ro'
                        result_input.append(f'launching://{type}/{element}@{version}?alias={param_name}&action={mount_type}')
                    else:
                        raise ValueError(f'invalid input format: {each}')
                    continue
                if os.path.exists(str(Path(each).absolute().resolve())):
                    each = str(Path(each).absolute().resolve())
                    input_path = Path(each)
                    data['work_path'] = str(Path(input_path).absolute().resolve())
                    oss_path = self._upload_job_data_to_tiefblue(
                        prefix, token, input_path, progress_bar=not args.disable_progress, need_parse=False)
                else:
                    raise ValueError(f'input path does not exist: {each}')
            data['oss_path'] = [oss_path]
            data['input_file_method'] = 1
            data['input_file_type'] = 3
        else:
            raise ValueError('missing input file')
        # sys.exit(0)
        for each in ["disk_size", "project_id", "job_group_id"]:
            if each in data and not isinstance(data[each], int):
                if isinstance(data[each], str):
                    try:
                        data[each] = int(data[each])
                    except:
                        data[each] = 0
                else:
                    data[each] = 0
        result = self.cli.client.job.insert(**data)
        if args.only_job_id:
            self.cli.print(result['jobId'])
            return
        if args.only_job_group_id:
            self.cli.print(result['jobGroupId'])
            return
        self.cli.print("Submit job succeed. JOB GROUP ID: %s, JOB ID: %s" % (result['jobGroupId'], result['jobId']))
        self.cli.log("job", "submit",
                     {'jobGroupId': result['jobGroupId'], 'jobId': result['jobId'],
                      'submitLocation': os.path.abspath(input_path)})

    def func_submit(self, args):
        data = {}
        if args.file:
            p = Path(args.file)
            d = {}
            if p.suffix == '.json':
                d = json.loads(p.read_text())
            elif p.suffix == '.yaml' or p.suffix == '.yml':
                d = yaml.safe_load(p.read_text())
            else:
                raise ValueError('unsupported file formate, current support are json yaml yml.')
            for k, v in d.items():
                if k == "backward_files":
                    data["out_files"] = v
                else:
                    data[k] = v
        if args.job_type:
            data['job_type'] = args.job_type
        else:
            if 'job_type' not in data:
                data['job_type'] = 'indicate'
        if args.job_group_id:
            data['job_group_id'] = args.job_group_id
        if args.project_id:
            data['project_id'] = args.project_id
        else:
            if 'project_id' not in data:
                if 'program_id' in data:
                    data['project_id'] = data['program_id']
                else:
                    data['project_id'] = self.cli.program_id()
        if args.job_name:
            data['job_name'] = args.job_name
        if args.image_name:
            data['image_name'] = args.image_name
        if args.disk_size:
            data['disk_size'] = args.disk_size
        if 'machine_type' in data:
            data['scass_type'] = data['machine_type']
        if args.scass_type:
            data['scass_type'] = args.scass_type
        if args.machine_type:
            data['scass_type'] = args.machine_type
        if args.nnode:
            data['nnode'] = args.nnode
        if args.instance_group_id:
            data['instance_group_id'] = args.instance_group_id
        if args.cmd:
            data['cmd'] = args.cmd
        else:
            if 'command' in data:
                data['cmd'] = data['command']
        if args.log_file:
            data['log_file'] = args.log_file
        if args.out_files:
            data['out_files'] = args.out_files
        if args.platform:
            data['platform'] = args.platform
        if args.region:
            data['region'] = args.region
        if args.on_demand:
            data['on_demand'] = args.on_demand
        if data.get('image_address') and not data.get('image_name'):
            data['image_name'] = data.get('image_address')
        if args.result or 'result' in data:
            result_path = args.result if args.result else data['result']
            ep = os.path.expanduser(result_path)
            p = Path(ep).absolute().resolve()
            p = p.joinpath(str(uuid.uuid4()) + "_temp.zip")
            data['download_path'] = str(p.absolute().resolve())
            retry = 7
            get_id_ok = False
            for i in range(retry):
                try:
                    resp = requests.get("http://100.100.100.200/latest/meta-data/instance-id", timeout=2)
                    resp.raise_for_status()
                    data['cli_instance_id'] = resp.text
                    get_id_ok = True
                    break
                except:
                    pass
            if not get_id_ok:
                self.cli.warn("current node is not belong to Bohrium, auto download is disable")
        if args.checkpoint_time:
            data['checkpoint_time'] = args.checkpoint_time
        if args.checkpoint_files:
            data['checkpoint_files'] = args.checkpoint_files
        if args.check_machine_type != 0:
            result = self.cli.client.job.checkMachineType(data['scass_type'])
            if result['type'] and result['msg'] and result['type'] != 'QUICK':
                if result['type'] == "NULL":
                    notice = f"{Fore.RED}" + result['msg'] + f"{Fore.RESET}"
                    self.cli.print(notice)
                    return
                else:
                    notice = f"{Fore.YELLOW}" + result['msg'] + f"{Fore.RESET}"
                    self.cli.print(notice)
                    isForceAdd = self._ask_for('y/n')
                    if isForceAdd != 'n' and isForceAdd != 'y':
                        self.cli.print("must be y/n")
                        return
                    if isForceAdd == 'y':
                        self.cli.print("Please replace the machine_type")
                        return
        if args.input:
            inputs = []
            n_local_inputs = 0
            for each in args.input:
                if '=' in each:
                    param_name, param_value = each.split('=', 1)
                    matched = LAUNCHING_URN_RE.match(param_value)
                    if matched:
                        type = matched.group('type')
                        version = matched.group('version') or 'latest'
                        element = matched.group('element')
                        mount_type = 'rw' if version == 'draft' else 'ro'
                        inputs.append(f'launching://{type}/{element}@{version}?alias={param_name}&action={mount_type}')
                    else:
                        raise ValueError(f'invalid input format: {each}')
                else:
                    if n_local_inputs > 0:
                        raise ValueError('only one local input is allowed')
                    n_local_inputs += 1
                    input_path = Path(each)
                    if not input_path.exists():
                        raise ValueError(f'input path does not exist: {input_path}')
                    data['work_path'] = str(Path(input_path).absolute().resolve())
                    oss_path = self._upload_job_data(
                        job_type='indicate', zip_path=input_path, disable_progress=args.disable_progress)
                    inputs.append(oss_path)
            if n_local_inputs == 0:
                raise ValueError('missing input file')
            data['oss_path'] = inputs
        else:
            raise ValueError('missing input file')
        for each in ["disk_size", "project_id", "job_group_id"]:
            if each in data and not isinstance(data[each], int):
                if isinstance(data[each], str):
                    try:
                        data[each] = int(data[each])
                    except:
                        data[each] = 0
                else:
                    data[each] = 0
        result = self.cli.client.job.insert(**data)
        if args.only_job_id:
            self.cli.print(result['jobId'])
            return
        if args.only_job_group_id:
            self.cli.print(result['jobGroupId'])
            return
        self.cli.print("Submit job succeed. JOB GROUP ID: %s, JOB ID: %s" % (result['jobGroupId'], result['jobId']))
        self.cli.log("job", "submit",
                     {'jobGroupId': result['jobGroupId'], 'jobId': result['jobId'],
                      'submitLocation': os.path.abspath(input_path)})

    def _upload_job_data(self, job_type, zip_path, **kwargs):
        task_uuid = uuid.uuid1().hex
        zip_path = os.path.abspath(zip_path)
        zip_dir_target, zip_name = os.path.split(zip_path.rstrip('/').rstrip("\\"))
        zip_task_file = Path(os.path.join(zip_dir_target, zip_name)).as_posix()
        ziped_file = make_archive(zip_task_file, "zip", zip_path)
        self.cli.print("Zip File Success!")
        self.cli.print("Uploading")
        oss_task_dir = f'dpcloudserver/{job_type}/{task_uuid}/{task_uuid}.zip'
        self._upload_file_to_oss(oss_task_dir, ziped_file, **kwargs)
        if not PROD_ENV:
            oss_task_dir = urllib.parse.urljoin('https://dpcloudserver-test.' + self.cli.storage_endpoint(), oss_task_dir)
        else:
            oss_task_dir = urllib.parse.urljoin('https://dpcloudserver.' + self.cli.storage_endpoint(), oss_task_dir)
        self.cli.print("Uploaded")
        os.remove(ziped_file)
        return oss_task_dir

    def _upload_job_data_to_tiefblue(self, path_prefix, token, zip_path, **kwargs):
        zip_dir_target, zip_name = os.path.split(zip_path.as_posix().rstrip('/').rstrip("\\"))
        zip_path = os.path.abspath(zip_path)
        zip_task_file = Path(os.path.join(zip_dir_target, zip_name)).as_posix()
        oss_task_dir = Path(os.path.join(path_prefix, zip_name + '.zip')).as_posix()
        make_archive(zip_task_file, "zip", zip_path)
        client = self.cli.tiefblue_client(token)
        client.upload_from_file(oss_task_dir, zip_task_file + ".zip", **kwargs)
        os.remove(zip_task_file + ".zip")
        return oss_task_dir

    def _upload_file_to_oss(self, oss_task_dir, zip_task_file, **kwargs):
        bucket = self._get_oss_bucket()
        total_size = os.path.getsize(zip_task_file)
        part_size = determine_part_size(total_size, preferred_size=1000 * 1024)
        upload_id = bucket.init_multipart_upload(oss_task_dir).upload_id
        parts = []
        with open(zip_task_file, 'rb') as fileobj:
            bar_format = "{l_bar}{bar}| {n:.02f}/{total:.02f} %  [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
            pbar = tqdm(total=100, desc="Uploading to oss", smoothing=0.01, bar_format=bar_format,
                        disable=kwargs.get('disable_progress'))
            part_number = 1
            offset = 0
            while offset < total_size:
                num_to_upload = min(part_size, total_size - offset)
                percent = num_to_upload * 100 / (total_size + 1)
                result = bucket.upload_part(
                    oss_task_dir, upload_id, part_number, SizedFileAdapter(fileobj, num_to_upload))
                parts.append(PartInfo(part_number, result.etag))
                offset += num_to_upload
                part_number += 1
                pbar.update(percent)
            pbar.close()
        bucket.complete_multipart_upload(oss_task_dir, upload_id, parts)

    def _get_oss_bucket(self):
        data = self.cli.client.job.get_sts()
        auth = oss2.StsAuth(data['AccessKeyId'], data['AccessKeySecret'], data['SecurityToken'])
        bucket = oss2.Bucket(auth, self.cli.storage_endpoint(), GlobalConfig.STORAGE_BUCKET_NAME)
        return bucket

    def load_download(self):
        parser_tm = self.sub_parser.add_parser('download', help='download selected job')
        parser_tm.set_defaults(func=lambda args: self.func_download(args))
        parser_tm.add_argument('job_ids', nargs='+', type=int, help='id of the job')
        parser_tm.add_argument('-p', '--path', action='store', help='download location default current dir')
        parser_tm.add_argument('-pr', '--parent', action='store_true', help='create parent dir if needed')

    def func_download(self, args, tolerate=False):
        job_ids = args.job_ids
        if args.path:
            target = args.path
        else:
            target = os.getcwd()
        bar_format = "{l_bar}{bar}| {n:.02f}/{total:.02f} %  [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
        parent_bar = tqdm(job_ids, desc="Downloading Job", bar_format=bar_format)
        download_paths = []
        for each in job_ids:
            parent_bar.set_description("Downloading Job " + str(each))
            result = self.cli.client.job.detail(each)
            if result.get('resultUrl'):
                u = result.get('resultUrl')
                suf = Path(urllib.parse.urlparse(u).path).suffix
                p = Path(target)
                result_path = Path(result.get('result'))
                if not p.exists():
                    if args.parent:
                        p.mkdir(exist_ok=True, parents=True)
                    else:
                        p.mkdir(exist_ok=True)
                target_path = Path(target).joinpath(str(result['id']))
                if not download(result.get('resultUrl'), target_path, suffix=suf):
                    self.cli.print(f'job id: {result["id"]} does not have result yet.')
                download_paths.append((result["id"], target_path.absolute()))
            else:
                self.cli.print(f'job id: {result["id"]} does not have result yet.')
            parent_bar.update(1)
        parent_bar.close()
        for (k, v) in download_paths:
            self.cli.print(f'job {k} download to {v}')

    def load_describe(self):
        parser_ls = self.sub_parser.add_parser('describe', help='describe job')
        parser_ls.set_defaults(func=lambda args: self.func_describe(args))
        parser_ls.add_argument('-l', '--long', action='store_true', help='long listing format')
        parser_ls.add_argument('job_id', nargs='+', type=int, help='id of the job')
        append_format_to_parser(parser_ls)

    def func_describe(self, args):
        jobs = []
        for each in args.job_id:
            result = self.cli.client.job.detail(each)
            jobs.append(result)

        def mapper(v):
            if not args.long:
                del v['machines']
                del v['result']
                del v['resultUrl']
                del v['updateTime']
                del v['isK8s']
                del v['thirdpartyId']
                del v['jobFiles']
                del v['inputData']
                # v['jobFiles.LogFiles'] = v['jobFiles'].get('logFiles')
                # v['jobFiles.InputFiles'] = v['jobFiles'].get('inputFiles')
                # v['jobFiles.outFiles'] = v['jobFiles'].get('outFiles')
            v['status'] = self.job_status_to_str(v['status'])
            return v

        tr = TableResult(jobs, first_col='id', columns_order=['id', 'jobName', 'jobGroupId'], mapper_func=mapper,
                         no_header=args.noheader, default_format=self.cli.output_format())
        result = tr.output(args)
        self.cli.print(result)

    # def load_jcc(self):
    #     parser_ls = self.sub_parser.add_parser('view', help='view job file')
    #     parser_ls.set_defaults(func=lambda args: self.func_jcc(args))
    #     parser_ls.add_argument('job_id', type=int, help='id of the job')

    # def func_jcc(self, args):
    #     JCCOperator(self.cli, args.job_id).start()

    def _ask_for(self, query):
        while True:
            question = f"{query}: "
            result = input(question)
            if not result:
                self.cli.print("This is required")
                continue
            return result
