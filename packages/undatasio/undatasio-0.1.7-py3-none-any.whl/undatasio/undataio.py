import os
from typing import Dict, List

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class UnDatasIO:
    def __init__(self, token: str, task_name: str = ""):
        self.token = token
        # self.ip = ip
        # self.base_url = f"http://{ip}:8087/api/api"
        self.task_name = task_name
        self.base_url = 'http://116.204.67.82:8087/api/api'

    def upload(self, file_dir_path: str) -> Dict:
        for file_path in os.listdir(file_dir_path):
            file_read_path = os.path.join(file_dir_path, file_path)
            with open(file_read_path, "rb") as file:
                fields = {
                    "user_id": self.token,
                    "task_name": self.task_name,
                    "file": (file_path, file, "application/octet-stream"),
                }
                m = MultipartEncoder(fields=fields)

                # 发送 POST 请求
                headers = {"Content-Type": m.content_type}
                response = requests.post(
                    f"{self.base_url}/upload", data=m, headers=headers
                )
                if response.json()['code'] != 200:
                    return {"error": response.json()['msg']}
        return "上传成功"

    def parser(self, file_name_list: List) -> Dict:
        API_ENDPOINT = f"{self.base_url}/task_return_list"
        data = {
            "user_id": self.token,
            "task_name": self.task_name,
            "fileName": file_name_list,  # 根据你的接口定义，文件名参数应该是 fileName
        }

        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.json()['code'] != 200:
                return {"error": response.json()['msg']}
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"请求失败: {e}"}

    def download(self, version: str) -> Dict:
        API_ENDPOINT = f"{self.base_url}/download"
        data = {
            "user_id": self.token,
            "task_name": self.task_name,
            "version": version,  # 根据你的接口定义，文件名参数应该是 fileName
        }

        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.json()['code'] != 200:
                return {"error": response.json()['msg']}
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"请求失败: {e}"}

    def show_version(self) -> Dict:
        API_ENDPOINT = f"{self.base_url}/version_info"
        data = {"user_id": self.token, "task_name": self.task_name}

        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.json()['code'] != 200:
                return {"error": response.json()['msg']}
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"请求失败: {e}"}

    def show_upload(self) -> Dict:
        API_ENDPOINT = f"{self.base_url}/view_upload_file"
        data = {"user_id": self.token, "task_name": self.task_name}

        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.json()['code'] != 200:
                return {"error": response.json()['msg']}
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"请求失败: {e}"}

    def get_result_type(
        self, type_info: List, file_name: str, version: str
    ):
        """
        :param type_info: 请在title, table, text, title, interline_equation中选择
        :param file_name: 文件名称
        :param version: 版本
        :return:
        """
        API_ENDPOINT = f"{self.base_url}/get_type_info"
        data = {
            "user_id": self.token,
            "type_info": type_info,
            "file_name": file_name,
            "version": version,
            "task_name": self.task_name,
        }
        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.json()['code'] != 200:
                return {"error": response.json()['msg']}
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"请求失败: {e}"}
