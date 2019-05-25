import requests
import readConfig as readConfig
from common.log import MyLog as Log
import json

localReadConfig = readConfig.ReadConfig()


class ConfigHttp:

    def __init__(self):
        global scheme, host, port, timeout,host_au
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        host_au = localReadConfig.get_http("Authorization_url")
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.state = 0

    def set_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.url = scheme+ '://'+host+url
        print(self.url)
        return self.url

    def set_au_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.url = scheme+ '://'+host_au+url
        print(self.url)

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data

    def set_files(self, file):
        """
        set upload files
        :param filename:
        :return:
        """
        if file != '':

            self.files = file

            # file_path = 'C:/Users/admin/Pictures/Saved Pictures/' + filename
            # self.files_in = open(file_path, 'rb')
            #
            # files = {'relateType': (None, "REPAIR"), 'fileData': ("2.jpg", open(file_path, 'rb'))}

    # defined http get method
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            # self.logger.error("Time out!")
            return None

    # defined http post method
    # include get params and post data
    # uninclude upload file
    def post(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, params=self.params, data=self.data, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include upload file
    def postWithFile(self):
        """
                defined post method
               :return:
                 """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            # self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            aa = response.text
            print(response.text)
            # return response
        except TimeoutError:
            # self.logger.error("Time out!")
            return None

if __name__ == "__main__":
    a = ConfigHttp()
    a.post()



