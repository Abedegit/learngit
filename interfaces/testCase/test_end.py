#该文件用来清除最后的testfile中所有的认证id，下次运行时生成新的
import unittest
import paramunittest
import readConfig as readConfig
from common.log import Log
from common import commons
from common import configHttp as ConfigHttp
from common.log import MyLog
import json,os

create_house_xls = commons.get_xls("caseforparame.xlsx", "Dispatchingre")



localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()




class Dispatchingre(unittest.TestCase):

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.proDir = readConfig.proDir

        # print(self.case_name+"测试开始前准备")

    def test_end(self):
        xlsPath_Authorizationid = os.path.join(self.proDir, "testFile", "Authorizationid")
        xlsPath_Authorizationid_approvals = os.path.join(self.proDir, "testFile", "Authorizationid_approvals")
        xlsPath_Authorizationid_repair = os.path.join(self.proDir, "testFile", "Authorizationid_repair")
        xlsPath_Authorizationid_dispatching = os.path.join(self.proDir, "testFile", "Authorizationid_dispatching")
        print(xlsPath_Authorizationid_approvals)

        f = open(xlsPath_Authorizationid,"w")
        f.truncate()
        f.close()
        k = open(xlsPath_Authorizationid_approvals,"w")
        # k.truncate()
        k.close()
        j = open(xlsPath_Authorizationid_dispatching,"w")
        j.truncate()
        j.close()
        w = open(xlsPath_Authorizationid_repair,"w")
        w.truncate()
        w.close()

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()



