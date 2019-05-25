import requests
import readConfig as readConfig
import os
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from common import configHttp as configHttp
from common.log import MyLog
import json,xlwt,threading
from xlutils.copy import copy

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConfigHttp = configHttp.ConfigHttp()
log = MyLog.get_log()
logger = log.get_logger()

caseNo = 0


def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    code = response.status_code
    # print("msg+++++++++++++++++++++++++++++++++++++++++++  %s" % msg)
    print("\n请求地址："+url)
    print("\n响应状态码：" + str(code))
    print("\n响应文本："+msg)

    # 可以显示中文
    # print("\n请求返回值："+'\n'+json.dumps(msg, ensure_ascii=False, sort_keys=True, indent=4))
    return msg

# ****************************** read testCase excel ********************************


def get_xls(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls

#從json中取出數據
def get_parameter_from_xls(dicts, objkey, default):
    tmp = dicts
    for k,v in tmp.items():
        if k == objkey or v == objkey:
            return v
        else:
            if isinstance(v, dict):
                print("v %s" % type(v))
                ret = get_parameter_from_xls(v, objkey, default)
                if ret is not default:
                    return ret
    return default


def Deposit_xls(xls_name, sheet_name, sheet_content, case_name):
    mutex = threading.Lock()
    mutex.acquire()
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    file = open_workbook(xlsPath)
    # get sheet by name
    rs_sheet = file.sheet_by_name(sheet_name)

    wb_sheet = copy(file)  # 瞳蚚xlutils.copy狟腔copy滲杅葩秶
    ws_sheet = wb_sheet.get_sheet(sheet_name)  # 鳳桶等0

    nrows = rs_sheet.nrows
    clo_list = rs_sheet.row_values(0)
    for index, value in enumerate(clo_list):
        if value == "response":
            for i in range(nrows):
                if rs_sheet.row_values(i)[0] == case_name:
                    ws_sheet.write(i, index, sheet_content)
                    wb_sheet.save(xlsPath)
    mutex.release()


#sheet_name_last要取数据的sheet
def Deposit_xls_relyon(xls_name,sheet_name,sheet_name_last,case_name):
    mutex = threading.Lock()
    mutex.acquire()
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    file = open_workbook(xlsPath)
    # get sheet by name
    rs_sheet_last = file.sheet_by_name(sheet_name_last)
    # wb_sheet_last = copy(file)
    # ws_sheet_last = wb_sheet_last.get_sheet(sheet_name_last)
    clo_list_last = rs_sheet_last.row_values(0)

    for index, value in enumerate(clo_list_last):
        rs_sheet = file.sheet_by_name(sheet_name)
        nrows = rs_sheet.nrows
        for i in range(nrows):
            if value == "response" and i != 0 and rs_sheet.row_values(i)[0]==case_name:
                print(i, index)
                xlsss = rs_sheet.row_values(1)[2]
                print(xlsss)
                xlss = rs_sheet_last.row_values(i)[index]
                mutex.release()
                return xlss
                # ws_sheet_last.write(i, index, sheet_content)
#扢离等啋跡style
def body_style(pattern=None):
    # 扢离excel等啋跡瑞跡
    font = xlwt.Font()  # Create Font
    font.name = "SimSun"  # 冼极
    font.height = 20 * 12  # 趼极湮苤
    style = xlwt.XFStyle()  # Create Style
    style.alignment.horz = 2  # 趼极懈笢
    style.alignment.vert = 1
    style.alignment.wrap = 1
    if pattern:
        pat = xlwt.Pattern()
        pat.pattern = xlwt.Pattern.SOLID_PATTERN  # 扢离掖劓晇伎
        pat.pattern_fore_colour = pattern
        style.pattern = pat
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    style.font = font
    style.borders = borders
    return style

# ****************************** read SQL xml ********************************
database = {}


def set_xml():
    """
    set sql xml
    :return:
    """
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            # print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    # print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table


def get_xml_dict(database_name, table_name):
    """
    get db dict by given name
    :param database_name:
    :param table_name:
    :return:
    """
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    """
    get sql by given name and sql_id
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql
# ****************************** read interfaceURL xml ********************************


def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)

    url = '/'+ '/'.join(url_list)
    return url

def get_parameter_one(sheet,x,y,filename="caseforparame.xlsx"):
    get_xls_Addrepair = get_xls("caseforparame.xlsx", sheet)
    xls_reponses= get_xls_Addrepair[x][y]
    return xls_reponses

def get_Authorization(username=None,password=None,txt_file="Authorizationid"):
    #獲取路徑
    mutex = threading.Lock()
    mutex.acquire()
    xlsPath = os.path.join(proDir, "testFile", txt_file)
    name = open(xlsPath, 'r')
    number = list(name.readlines())

        # 獲取date參數
    if username==None or password==None:
        if number == []:
            name.close()
            url = get_url_from_xml('Authorization')
            print(url)
            localConfigHttp.set_au_url(url)

            # 獲取header頭部
            Accept = localReadConfig.get_headers('Accept')
            headers = {"Accept": Accept}
            localConfigHttp.set_headers(headers)
            date = get_xls("caseforparame.xlsx", "Authorization")
            print('從excel獲取參數如下%s：' % date)
            date_01 = date[0]
            date_02 = date[1]
            Authorization_josn = {}
            for i in range(len(date_01)):
                Authorization_josn[date_01[i]] = date_02[i]
            Authorization_josn[date_01[-1]] = int(Authorization_josn[date_01[-1]])
            print("Authorization_josn %s" % Authorization_josn)
            localConfigHttp.set_data(Authorization_josn)
            # 發送請求獲取Authorization_id
            return_json = localConfigHttp.post()
            print(return_json)
            info = return_json.json()
            Authorization_id = info['accessToken']
            print('Authorization_id：' + Authorization_id)
            name = open(xlsPath, 'w')
            name.write(Authorization_id)
            name.close()
            mutex.release()
            return Authorization_id
        else:
            #如果txt存在id，直接取值
            each = str(number[0]).replace('\n', "")
            Authorization_id = each.replace('\r', '1')
            print("Authorization_id :       " + Authorization_id)
            name.close()
            mutex.release()
            return Authorization_id
    else:
        if number == []:
            # 如果不为空的情况下，拿参数去请求
            name.close()
            url = get_url_from_xml('Authorization')
            print(url)
            localConfigHttp.set_au_url(url)
            Authorization_josn = {
                "deviceToken": 123,
                "deviceld": 123,
                "clientid": 123,
                "username": username,
                "password": password
            }
            Authorization_josn_Final = json.dumps(Authorization_josn)
            localConfigHttp.set_data(Authorization_josn)
            # 發送請求獲取Authorization_id
            return_json = localConfigHttp.post()
            print(return_json)
            info = return_json.json()
            Authorization_id = info['accessToken']
            print('Authorization_id：' + Authorization_id)
            name = open(xlsPath, 'w')
            name.write(Authorization_id)
            name.close()
            mutex.release()
            return Authorization_id
        else:
            #如果txt存在id，直接取值
            each = str(number[0]).replace('\n', "")
            Authorization_id = each.replace('\r', '1')
            print("Authorization_id :       " + Authorization_id)
            name.close()
            mutex.release()
            return Authorization_id


def delete_Authorization_id():
    xlsPath = os.path.join(proDir, "testFile", 'Authorizationid')
    name = open(xlsPath, 'w')
    name.close()



def get_Parameter():
    xlsPath = os.path.join(proDir, "testFile", 'sn_Parameter')
    name = open(xlsPath, 'r')
    number = list(name.readlines())
    each = str(number[0]).replace('\n', "")
    Parameter = each.replace('\r', '1')
    del number[0]
    name.close()
    files = open(xlsPath, 'w')
    for i in number:
        files.write(i)
    files.close()
    return Parameter




if __name__ == "__main__":
    # print(get_xls("login"))
    get_Authorization()

