import unittest
import paramunittest
import readConfig as readConfig
from common.log import Log
from common import commons
from common import configHttp as ConfigHttp
from common.log import MyLog
import json

create_house_xls = commons.get_xls("caseforparame.xlsx", "Itemsupdate")

print('create_house_xls %s ' % create_house_xls)
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}
Authorization_id = commons.get_Authorization()

@paramunittest.parametrized(*create_house_xls)
class Itemsupdate(unittest.TestCase):
    def setParameters(self,case_name, id,cnName, enName, isApplyToStudent, isApplyToTeacher, isNeedAuditStudent,
                      isNeedAuditTeacher, isReleased, roomTypeCnName,roomTypeEnName,roomTypeId,roomTypeKey,sn,result,response):
        self.case_name = str(case_name)
        self.id_change = int(id)
        self.cnName = str(cnName)
        self.enName = str(enName)
        self.isApplyToStudent = int(isApplyToStudent)
        self.isApplyToTeacher = int(isApplyToTeacher)
        self.isNeedAuditStudent = int(isNeedAuditStudent)
        self.isNeedAuditTeacher = int(isNeedAuditTeacher)
        self.isReleased = int(isReleased)
        self.roomTypeCnName = str(roomTypeCnName)
        self.roomTypeEnName = str(roomTypeEnName)
        self.roomTypeId = int(roomTypeId)
        self.roomTypeKey = str(roomTypeKey)
        self.result = result

    def setUp(self):
        # print(self.case_name+"测试开始前准备")
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.sn = commons.get_Parameter()

    def test01_Itemsupdate(self):

        get_xls_Addrepair = commons.get_xls("caseforparame.xlsx", "Addproject")
        try:
            xls_01 = get_xls_Addrepair[0]
            xls_02 = get_xls_Addrepair[1]
        except:
            print("超出列表值")
        xls_reponses_Addrepairs = get_xls_Addrepair[0][-1]
        xls_reponses_Addrepair = json.loads(xls_reponses_Addrepairs)


        # set url
        self._testMethodDoc = self.case_name
        self.url = commons.get_url_from_xml('Itemsupdate')
        self.id_change = commons.get_parameter_from_xls(xls_reponses_Addrepair, 'id', None)
        self.url_new = self.url + "/" + str(self.id_change)
        configHttp.set_url(self.url_new)
        print("第一步：设置url  "+self.url_new)

        #set headers
        Content_Type = localReadConfig.get_headers('Content-Type')
        no_cache = localReadConfig.get_headers('Cache-Control')
        header = {"Content-Type": Content_Type,'Authorization':Authorization_id,'Cache-Control':no_cache}
        print('header%s ' % header )
        configHttp.set_headers(header)
        print("第二步：设置header等")

        # set params
        data = {
            "cnName":self.cnName,
            "enName": self.enName ,
            "isApplyToStudent":self.isApplyToStudent ,
            "isApplyToTeacher": self.isApplyToTeacher,
            "isNeedAuditStudent": self.isNeedAuditStudent,
            "isNeedAuditTeacher": self.isNeedAuditTeacher,
            "isReleased": self.isReleased,
            "roomTypeList": [
                {
                    "roomTypeCnName": self.roomTypeCnName,
                    "roomTypeEnName": self.roomTypeEnName,
                    "roomTypeId": self.roomTypeId,
                    "roomTypeKey": self.roomTypeKey
                }
            ],
            "sn": self.sn
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

    def tearDown(self):
        print("测试结束，输出log完结\n\n")

    def checkResult(self):

        self.info = commons.show_return_msg(self.return_json)
        #     # if self.result == '0':
        self.infos = json.loads(self.info)
        result_status = commons.get_parameter_from_xls(self.infos, "success", None)
        #     email = commons.get_value_from_return_json(self.info, 'member', 'email')
        print(result_status)
        self.assertEqual(result_status, self.result)
        #     print('第六步，記錄響應結果')
        commons.Deposit_xls('caseforparame.xlsx', 'Itemsupdate', self.info, self.case_name)
    #     # if self.result == '0':
    #     email = commons.get_value_from_return_json(self.info, 'member', 'email')
    #     self.assertEqual(self.info['code'], self.code)
    #     print('第六步，記錄響應結果')
    #         # self.assertEqual(self.info['msg'], self.msg)
    #         # self.assertEqual(email, self.email)
    #     # if self.result == '1':
    #     #     self.assertEqual(self.info['code'], self.code)
    #     #     self.assertEqual(self.info['msg'], self.msg)

