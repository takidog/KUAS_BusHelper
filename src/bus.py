#-*- coding: utf-8 -*-
#Origin Author: NKUST-ITC
#Orgin from github.com/NKUST-ITC/AP-API/tree/master/src/kuas_api
#Edit :TakiDog

import requests
import execjs
import json
import time
import datetime

js = open('bus.js','r')
js_function = js.read()
js.close()

headers = {"User-Agnet":
           "Mozilla/5.0 (X11; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/35.0"}

# Bus url setting
BUS_URL = "http://bus.kuas.edu.tw"
BUS_SCRIPT_URL = "http://bus.kuas.edu.tw/API/Scripts/a1"
BUS_API_URL = "http://bus.kuas.edu.tw/API/"
BUS_LOGIN_URL = BUS_API_URL + "Users/login"
BUS_FREQ_URL = BUS_API_URL + "Frequencys/getAll"
BUS_RESERVE_URL = BUS_API_URL + "Reserves/getOwn"
BUS_BOOK_URL = BUS_API_URL + "Reserves/add"
BUS_UNBOOK_URL = BUS_API_URL + "Reserves/remove"

# Bus timeout setting
BUS_TIMEOUT = 1.0

def _get_real_time(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp) / 10000000 - 62135596800).strftime("%Y-%m-%d %H:%M")


def status():
    """Return Bus server status code

    :rtype: int
    :returns: A HTTP status code

    >>> status()
    200
    """

    try:
        bus_status_code = requests.head(
            BUS_URL, timeout=BUS_TIMEOUT).status_code
    except requests.exceptions.Timeout:
        bus_status_code = 408

    return bus_status_code


def init(session):
    session.head(BUS_URL)
    script_content = session.get(BUS_SCRIPT_URL, headers=headers).text

    js = execjs.compile(js_function + script_content)

    return js


def login(session, username, password):
    """Login to KUAS Bus system.

    :param session: requests session object
    :type session: class requests.sessions.Session
    :param username: username of kuas bus system, actually your kuas student id
    :type username: str or int
    :param password: password of kuas ap system.
    :type password: str or int

    :return: login status
    :rtype: bool
    """

    data = {'account': username, 'password': password}

    try:
        js = init(session)
        data['n'] = js.call('loginEncryption', str(username), str(password))
    except:
        return False

    content = session.post(BUS_LOGIN_URL,
                           data=data,
                           headers=headers,
                           timeout=BUS_TIMEOUT
                           ).text

    resp = json.loads(content)

    return resp['success']


def query(session, y, m, d, operation="全部"):
    """
    Query kuas bus timetable

    :param session: requests session object
    :type session: class requests.sessions.Session
    :param y: year, using common era
    :type y: int
    :param m: month
    :type m: int
    :param d: day
    :type d: int
    :param operation: choosing bus start from yanchao or jiangong, or all.
    :type operation: str

    >>> s = requests.Session()
    >>> login(s, "1102108133", "111")
    True

    >>> type(query(s, "2015", "6", "15"))
    <class 'list'>

    >>> type(query(s, *'2014-10-08'.split("-")))
    <class 'list'>

    """
    data = {
        'data': '{"y": "%s","m": "%s","d": "%s"}' % (y, m, d),
        'operation': operation,
        'page': 1,
        'start': 0,
        'limit': 90
    }

    resp = session.post(BUS_FREQ_URL, data=data, headers=headers)

    resource = json.loads(resp.text)
    returnData = []

    if not resource['data']:
        return []

    for i in resource['data']:
        Data = {}
        Data['EndEnrollDateTime'] = _get_real_time(i['EndEnrollDateTime'])
        Data['runDateTime'] = _get_real_time(i['runDateTime'])
        Data['Time'] = Data['runDateTime'][-5:]
        Data['endStation'] = i['endStation']
        Data['busId'] = i['busId']
        Data['reserveCount'] = i['reserveCount']
        Data['limitCount'] = i['limitCount']
        Data['isReserve'] = int(i['isReserve']) + 1
        Data['SpecialTrain'] = i['SpecialTrain']
        Data['SpecialTrainRemark'] = i['SpecialTrainRemark']

        returnData.append(Data)

    return returnData


def reserve(session):
    """Query user reserve bus.
    """

    data = {
        'page': 1,
        'start': 0,
        'limit': 90
    }

    content = session.post(BUS_RESERVE_URL, data=data, headers=headers).text

    resource = json.loads(content)

    rd = []
    for i in resource['data']:
        data = {}
        data['time'] = _get_real_time(i['time'])
        data['endTime'] = _get_real_time(i['endTime'])
        data['cancelKey'] = i['key']
        data['end'] = i['end']
        rd.append(data)

    result = sorted(rd, key=lambda k: k['time'])

    return result


def book(session, kid, action=None):
    if not action:
        res = session.post(BUS_BOOK_URL,
                           data="{busId: %s}" % (kid),
                           headers=headers,
                           )
    else:
        # Then compare users reserve bus,
        # if kid is same as time, then found the correct bus,
        # then we can unbook this bus.

        res = session.post(BUS_UNBOOK_URL,
                           data="{reserveId: %d}" % (kid) + "}",
                           headers=headers,
                           )

    resource = json.loads(str(res.content, "utf-8"))

    return resource


if __name__ == '__main__':
    #import doctest
    #doctest.testmod()
    #exit()

    session = requests.session()
    init(session)
    login(session, '1102108133', '111')

    t = time.time()
    print(query(session, *'2014-10-08'.split("-")))
    print(time.time() - t)
    exit()
    #book(session, '22868', '')

    print("---------------------")
    print(reserve(session))
    book(session, '741583', 'un')
    print(reserve(session))
    """
    result = query('2014', '6', '27')
    for i in result:
        if book(i['busId']) :
            print "Book Success"
    result = reserve()
    for i in result:
        if book(i['key'], "Un") :
            print "UnBook Success"
    """
