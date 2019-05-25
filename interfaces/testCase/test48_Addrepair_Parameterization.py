# -*- coding: UTF-8 -*-
#新增項目接口

import unittest
import paramunittest
import readConfig as readConfig
from common.log import Log
from common import commons
from common import configHttp as ConfigHttp
from common.log import MyLog
import json,threading
import os
import sys

Addrepair_xls = commons.get_xls("caseforparame.xlsx", "Addrp")



localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
Authorization_id = commons.get_Authorization()
list_info = []
filename = os.path.basename(sys.argv[0]).split(".")[0]

@paramunittest.parametrized(*Addrepair_xls)
class Addrepaircancel(unittest.TestCase):
    def setParameters(self,case_name, addr, attachmentIds, id, itemCnName, itemEnName, itemId, landCnName, landEnName,
                      landId,remark,roomCnName,roomEnName,roomId,roomTypeKey,tel,result,response):

        self.case_name = str(case_name)
        self.addr = str(addr)
        self.attachmentIds = int(attachmentIds)
        self.id_change = int(id)
        self.itemCnName = str(itemCnName)
        self.itemEnName = str(itemEnName)
        self.itemId = itemId
        self.landCnName = str(landCnName)
        self.landEnName = str(landEnName)
        self.landId = int(landId)
        self.remark = str(remark)
        self.roomCnName = str(roomCnName)
        self.roomEnName = str(roomEnName)
        self.roomId = int(roomId)
        self.roomTypeKey = str(roomTypeKey)
        self.tel = tel
        self.result = result
        # self.return_json = None
        # self.info = None

    # def description(self):
    #     """
    #     test report description
    #     :return:
    #     """
    #     self.case_name

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        # print(self.case_name+"测试开始前准备")
        pass


    def test01_Addrepaircancel(self):

        #依賴其他接口參數
        # Addproject_xls = commons.get_xls("caseforparame.xlsx", "Addproject")
        # xls_01 = Addproject_xls[0]
        # xls_02 = Addproject_xls[1]
        # xls_reponses = Addproject_xls[0][-1]
        # xls_reponse = json.loads(xls_reponses)

        # set url
        print('case ###############################################%s' % self.case_name)
        self._testMethodDoc = self.case_name
        self.url = commons.get_url_from_xml('Addrp')
        configHttp.set_url(self.url)
        print("第一步：设置url  "+self.url)

        # get visitor token
        # if self.token == '0':
        #     token = localReadConfig.get_headers("token_v")
        # elif self.token == '1':
        #     token = None

        #set headers
        Content_Type = localReadConfig.get_headers('Content-Type')
        no_cache = localReadConfig.get_headers('Cache-Control')
        header = {"Content-Type": Content_Type,'Authorization':Authorization_id,'Cache-Control':no_cache}
        print('header%s ' % header )
        configHttp.set_headers(header)
        print("第二步：设置header等")

        #從上一個接口獲取項目id，名稱
        # self.itemCnName = commons.get_parameter_from_xls(xls_reponse,"cnName",None)
        # self.itemEnName = commons.get_parameter_from_xls(xls_reponse,"enName",None)
        # self.itemId = commons.get_parameter_from_xls(xls_reponse,"id",None)

        # set params
        data = {
            "addr": self.addr,
            "attachmentIds": [self.attachmentIds],
            "id": self.id_change,
            "itemCnName": self.itemCnName,
            "itemEnName": self.itemEnName,
            "itemId": self.itemId,
            "landCnName": self.landCnName,
            "landEnName": self.landEnName,
            "landId": self.landId,
            "remark": self.remark,
            "roomCnName": self.roomCnName,
            "roomEnName": self.roomEnName,
            "roomId": self.roomId,
            "roomTypeKey": self.roomTypeKey,
            "tel": self.tel
        }
        DATE = json.dumps(data)
        print('DATE%s' % DATE)

        configHttp.set_data(DATE)
        print("第三步：设置发送请求的参数")
        self.logger.info("********creater********")

        # test interface
        try:
            self.return_json = configHttp.post()
        except Exception as e:
            print('e %s' % e)
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        print("第五步：检查结果")
        self.checkResult()
        return self.return_json

    # def test02_checkResult(self):
    #
    #     """
    #     check test result
    #     :return:
    #     """
    #     self.return_json = self.test01_Createhouse()
    #     print(type(self.return_json))
    #     self.info = self.return_json.json()
    #     # show return message
    #     common.show_return_msg(self.return_json)

        # if self.result == '0':
        #     email = common.get_value_from_return_json(self.info, 'member', 'email')
        # self.assertEqual(self.info['code'], self.code)
        # self.assertEqual(self.info['msg'], self.msg)
        # self.assertEqual(email, self.email)

        # if self.result == '1':
        #     self.assertEqual(self.info['code'], self.code)
        #     self.assertEqual(self.info['msg'], self.msg)

    def tearDown(self):
        """
        :return:
        """
        # info = self.info
        # if info['code'] == 0:
        #     # get uer token
        #     token_u = common.get_value_from_return_json(info, 'member', 'token')
        #     # set user token to config file
        #     localReadConfig.set_headers("TOKEN_U", token_u)
        # else:
        #     pass
        # self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])
        print("测试结束，输出log完结\n\n")

    def checkResult(self):
        """
        check test result
        :return:
        """
        # show return message

        self.info = commons.show_return_msg(self.return_json)
        #     # if self.result == '0':
        self.infos = json.loads(self.info)
        result_status = commons.get_parameter_from_xls(self.infos, "success", None)
        #     email = commons.get_value_from_return_json(self.info, 'member', 'email')
        print(result_status)
        self.assertEqual(result_status, self.result)
        #     print('第六步，記錄響應結果')
        commons.Deposit_xls('caseforparame.xlsx', 'Addrp', self.info, self.case_name)

    #     # if self.result == '0':
    #     email = commons.get_value_from_return_json(self.info, 'member', 'email')
    #     self.assertEqual(self.info['code'], self.code)
    #     print('第六步，記錄響應結果')

    #         # self.assertEqual(self.info['msg'], self.msg)
    #         # self.assertEqual(email, self.email)
    #
    #     # if self.result == '1':
    #     #     self.assertEqual(self.info['code'], self.code)
    #     #     self.assertEqual(self.info['msg'], self.msg)


