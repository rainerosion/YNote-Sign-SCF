import requests, json, logging
from notify import Notify
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# requests.packages.urllib3.disable_warnings()
def getTotalSpace(cookie):
    session = requests.Session()
    url = f'https://note.youdao.com/yws/mapi/payment?method=status&pversion=v2&pt=true&ClientVer=61000010000&GUID=PC28ed1418f0f0a75de&client_ver=61000010000&device_id=PC28ed1418f0f0a75de&device_name=RAINEROSION&device_type=PC&keyfrom=pc&os=Windows&os_ver=Windows%2010&vendor=website&vendornew=website'
    headers = {
        "User-Agent": "YNote",
        "Host": "note.youdao.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Cookie": cookie
    }
    response = session.post(url, headers=headers)
    return response.json()

def getuser(cookie):
    session = requests.Session()
    url = f'https://note.youdao.com/yws/api/self?ClientVer=61000010000&GUID=PC28ed1418f0f0a75de&client_ver=61000010000&device_id=PC28ed1418f0f0a75de&device_name=RAINEROSION&device_type=PC&keyfrom=pc&method=get&os=Windows&os_ver=Windows%2010&subvendor=&vendor=website&vendornew=website'
    headers = {
        "User-Agent": "YNote",
        "Host": "note.youdao.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Cookie": cookie
    }
    response = session.get(url, headers=headers)
    return response.json()
def checkin(cookie):
    session = requests.Session()
    url = f'https://note.youdao.com/yws/mapi/user?method=checkin'
    headers = {
        "User-Agent": "YNote",
        # "Referer": "https://note.youdao.com",
        "Host": "note.youdao.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Cookie": cookie
    }
    response = session.post(url, headers=headers)
    json = response.json()
    logging.info(json)
    # ????????????
    message = ''
    if 'success' in json :
        user = getuser(cookie)
        space = getTotalSpace(cookie)
        message = "????????????%s\n?????????%s\n???????????????%dM,?????????%.2fG" % (user['name'], user['email'], json['space'] / 1048576, space['um']['q'] / 1073741824)

        if json['success'] == 1:
            logging.info("????????????")
            message += "\n?????????????????????"
        elif json['success'] == 0:
            logging.warning("????????????")
            message += "\n?????????????????????"
        logging.info(message)
    else:
        logging.info("????????????:%s",json['message'])
        message += "\n?????????????????????\n?????????" + json['message']
    Notify().sendMessage(message)
    return json

def main_handler(event, context):
    cookies = [
        ""
    ]
    for cookie in cookies:
        checkin(cookie)
