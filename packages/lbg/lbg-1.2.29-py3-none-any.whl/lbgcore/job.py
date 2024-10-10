import humps
from lbgcli.const import GlobalConfig

class Job:
    def __init__(self, client):
        self.client = client

    def list_by_page(self, job_group_id, status=None, page=1, per_page=50):
        params = {
            'groupId': job_group_id,
            'page': page,
            'pageSize': per_page,
            'client': 0,
            'submitUserId': self.client.user_id
        }
        if status:
            params['status'] = status
        data = self.client.get(f'/bohrapi/v2/job/list', params=params)
        return data

    def list_by_number(self, job_group_id, number, status=None):
        if status is None:
            status = []
        if number == 0:
            number = 10
        per_page = 50
        job_list = []
        data = self.list_by_page(job_group_id, page=1, per_page=per_page, status=status)
        total = data['total']
        per_page = data['pageSize']
        page_number = 0
        while page_number * per_page < total:
            page_number = page_number + 1
            if page_number > 1:
                data = self.list_by_page(job_group_id, page=page_number, per_page=per_page, status=status)
            for each in data['items']:
                job_list.append(each)
                if number != -1 and len(job_list) >= number:
                    return job_list
        return job_list

    def delete(self, job_id):
        data = self.client.post(f"/brm/v1/job/del/{job_id}")
        return data

    def terminate(self, job_id):
        data = self.client.post(f"/brm/v1/job/terminate/{job_id}")
        return data

    def kill(self, job_id):
        data = self.client.post(f"/brm/v1/job/kill/{job_id}")
        return data

    def log(self, job_id):
        data = self.client.get(f"/brm/v1/job/{job_id}/log")
        return data

    def get_sts(self):
        data = self.client.get("/data/get_sts_token")
        return data

    def insert(self, **kwargs):
        must_fill = ['job_type', 'oss_path', 'project_id', 'scass_type', 'command', 'image_name']
        for each in must_fill:
            if each not in kwargs:
                raise ValueError(f'{each} is required when submitting job')
        camel_data = {humps.camelize(k): v for k, v in kwargs.items()}
        if not isinstance(camel_data['ossPath'], list):
            camel_data['ossPath'] = [camel_data['ossPath']]
        if 'logFile' in camel_data:
            camel_data['logFiles'] = camel_data['logFile']
        if 'logFiles' in camel_data and not isinstance(camel_data['logFiles'], list):
            camel_data['logFiles'] = [camel_data['logFiles']]
        if self.client.debug:
            print(camel_data)
        data = self.client.post("/brm/v2/job/add", data=camel_data)
        return data

    def detail(self, job_id):
        data = self.client.get(f"/brm/v1/job/{job_id}")
        return data

    def view_ls(self, job_id, path):
        if path == '':
            path = '/'
        params = {
            "path": path
        }
        data = self.client.post(f"/data/job/{job_id}/jcc/ls", data=params)
        return data.get('data', {})

    def view_read(self, job_id, path, start_byte=0, buf_size=8192):
        if path == '':
            path = '/'
        body = {
            "path": path
        }
        params = {
            'start_bytes': start_byte,
            'buf_size': buf_size
        }
        data = self.client.post(f"/data/job/{job_id}/jcc/read", data=body, params=params)
        return data.get('data', {})

    def view_state(self, job_id, path):
        if path == '':
            path = '/'
        params = {
            "path": path,
        }
        try:
            data = self.client.post(f"/data/job/{job_id}/jcc/state", data=params)
        except Exception as e:
            if 'no such file or directory' in str(e):
                return {}
            else:
                raise e
        return data.get('data', {})

    def create(self, project_id, name='', group_id=0, bohr_group_id=0):
        data = {
            'projectId': project_id
        }
        if name:
            data['name'] = name
        if group_id:
            data['groupId'] = group_id
        if bohr_group_id:
            data['bohrGroupId'] = bohr_group_id
        try:
            data = self.client.post(f"/brm/v1/job/create", data=data)
        except Exception as e:
            if 'no such file or directory' in str(e):
                return {}
            else:
                raise e
        return data
    def checkMachineType(self, machine_type):
        params = {
            'machineType': machine_type,
            'from': GlobalConfig.SOURCE_FROM
        }
        if self.client.debug:
            print(params)
        data = self.client.get(f'/bohrapi/v1/job/check_machine_type', params=params)
        return data
