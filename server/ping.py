#!/usr/bin/env python3

import re
import ssl
import json
import random
import datetime
import http.client
from bs4 import BeautifulSoup
from contextlib import closing
from urllib.parse import parse_qsl, urlencode

class SubwayForm:

    dummy_post = 'submitSet=%3CSurvey+surveyId%3D%22315%22+customerEmail+%3D%22mercisubway%40gmail.com%22+storeId%3D%2253994-0%22+customerValue%3D%2210%22+hostId%3D%22%22+optIn%3D%22No%22+receiptDate%3D%222018%7C1%7C20%7C16%7C0%7C0%7C0%7C-60%22+clientDate%3D%222018%7C1%7C20%7C16%7C6%7C13%7C726%7C-60%22+URL%3D%22https%3A%2F%2Fwww.parleznousdesubway.fr%2FContentManager%2FController.aspx%3Fpage%3DCustomerExperience%2FSurveyNew%26amp%3BsurveyId%3D315%26amp%3BstoreId%3D53994-0%22+timeFrecuency%3D%221%22+everyFrecuency%3D%22DAYLY%22+mobile%3D%22false%22+contactMe%3D%22%22+categoryId%3D%2257%22+lang%3D%2217%22%3E%3CAnswer+answer%3D%2253994-0%22+finalValue%3D%2253994-0%22+questionListId%3D%22null%22+questionId%3D%228079%22+type%3D%22STORE_ID%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%222018%7C1%7C20%7C16%7C0%7C0%7C0%7C-60%22+finalValue%3D%222018%7C1%7C20%7C16%7C0%7C0%7C0%7C-60%22+questionListId%3D%22null%22+questionId%3D%228081%22+type%3D%22DATETIME_CALENDAR_PICKER%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22369%22+finalValue%3D%22369%22+questionListId%3D%22null%22+questionId%3D%228146%22+type%3D%22TEXTBOX%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%2210%22+finalValue%3D%2210%22+questionListId%3D%22null%22+questionId%3D%228083%22+type%3D%22CUSTOMER_VALUE%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22null%22+finalValue%3D%2210%22+questionListId%3D%2238329%22+questionId%3D%228084%22+type%3D%22RADIO%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22null%22+finalValue%3D%2210%22+questionListId%3D%2238341%22+questionId%3D%228086%22+type%3D%22MATRIX_WITH_RADIOBUTTON%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22null%22+finalValue%3D%2210%22+questionListId%3D%2238352%22+questionId%3D%228087%22+type%3D%22MATRIX_WITH_RADIOBUTTON%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22null%22+finalValue%3D%2210%22+questionListId%3D%2238363%22+questionId%3D%228088%22+type%3D%22MATRIX_WITH_RADIOBUTTON%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22null%22+finalValue%3D%2210%22+questionListId%3D%2238374%22+questionId%3D%228089%22+type%3D%22MATRIX_WITH_RADIOBUTTON%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22null%22+finalValue%3D%2210%22+questionListId%3D%2238385%22+questionId%3D%228090%22+type%3D%22MATRIX_WITH_RADIOBUTTON%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22null%22+finalValue%3D%2210%22+questionListId%3D%2238396%22+questionId%3D%228091%22+type%3D%22MATRIX_WITH_RADIOBUTTON%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22null%22+finalValue%3D%22Non%22+questionListId%3D%2238442%22+questionId%3D%228104%22+type%3D%22DROPDOWN%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22null%22+finalValue%3D%22Non%22+questionListId%3D%2238445%22+questionId%3D%228106%22+type%3D%22DROPDOWN%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22null%22+finalValue%3D%2220%22+questionListId%3D%2238467%22+questionId%3D%228108%22+type%3D%22DROPDOWN%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22null%22+finalValue%3D%2220%22+questionListId%3D%2238499%22+questionId%3D%228109%22+type%3D%22DROPDOWN%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22mercisubway%40gmail.com%22+finalValue%3D%22mercisubway%40gmail.com%22+questionListId%3D%22null%22+questionId%3D%228110%22+type%3D%22EMAIL%22%3E%3C%2FAnswer%3E%3CAnswer+answer%3D%22No%22+finalValue%3D%22Non%22+questionListId%3D%22No%22+questionId%3D%228111%22+type%3D%22OPT_IN%22%3E%3C%2FAnswer%3E%3C%2FSurvey%3E&sid=0.14954957184748618'

    @staticmethod
    def generate_post(
            surveyId, storeId, ticketNb,
            sid, email, customerValue,
            recommendConf, recommend,
            eatSubwayConf, eatSubway,
            aspects
    ):
        #DATETIME_CALENDAR_PICKER
        d = UrlArgs.args2dict(SubwayForm.dummy_post)
        soup = JoliSoup(d['submitSet'])

        datetimeFmt = '%Y|%-m|%-d|%-H|%-M|%-S|0|-60'
        now = datetime.datetime.now()
        past = now - datetime.timedelta(seconds=1)
        now_str = now.strftime(datetimeFmt)
        past_str = past.strftime(datetimeFmt)

        #typed questions
        for t, v in [
                ('EMAIL', email),
                ('STORE_ID', storeId),
                ('TEXTBOX', ticketNb),
                ('DATETIME_CALENDAR_PICKER', past_str)
        ]:
            ask = soup.find(type=t)
            ask['answer'] = v
            ask['finalValue'] = v

        def saveconf(conf, value):
            ask = soup.find(questionId=conf['id'])
            ask['finalValue'] = value
            ask['questionListId'] = conf['values'][value]

        #all others
        saveconf(recommendConf, recommend)
        for conf in eatSubwayConf:
            saveconf(conf, eatSubway)
        for conf, value in aspects:
            saveconf(conf, value)

        #header
        soup['customerEmail'] = email
        soup['customerValue'] = customerValue
        soup['surveyId'] = surveyId
        soup['storeId'] = storeId
        soup['clientDate'] = now_str
        soup['receiptDate'] = past_str

        #url
        url, args  = soup['URL'].split('?')
        ud = UrlArgs.args2dict(args)
        ud['surveyId'] = surveyId
        ud['storeId'] = storeId
        soup['URL'] = f'{url}?{UrlArgs.dict2args(ud)}'

        #params
        d['submitSet'] = str(soup)
        d['sid'] = sid
        return UrlArgs.dict2args(d)

class JoliSoup(BeautifulSoup):
    def __new__(cls, txt):
        soup = super().__new__(cls)
        if isinstance(txt, bytes):
            txt = txt.decode()
        soup.__init__(txt, 'lxml')
        ltxt = txt.lower()
        obj = soup.html.body.find_all(recursive=False)[0]
        def get_old_case(s, before='', after=''):
            match = re.compile(f'{before}{s}{after}').search(ltxt)
            if match is None:
                raise RuntimeError(f'"{s}" not found in soup')
            begin, end = match.span()
            zone = txt[begin:end]
            idx = zone.lower().index(s)
            if idx < 0:
                raise RuntimeError(f'"{s}" not found in soup')
            return zone[idx:len(before)+len(s)]

        old_tags = {}
        def get_tag_case(s):
            if not s in old_tags:
                old_tags[s] = get_old_case(s, before='< *')
            return old_tags[s]

        old_attrs = {}
        def get_attr_case(s):
            if not s in old_attrs:
                old_attrs[s] = get_old_case(s, after=' *=')
            return old_attrs[s]

        def change(item):
            item.name = get_tag_case(item.name)
            attrs = dict(item.attrs)
            for attr, value in attrs.items():
                del item.attrs[attr]
                item.attrs[get_attr_case(attr)] = value
            for child in item.find_all(recursive=False):
                change(child)
        change(obj)
        return obj

class UrlArgs:

    @staticmethod
    def args2dict(s):
        return { key: value for key, value in parse_qsl(s) }

    @staticmethod
    def dict2args(d):
        return urlencode(list(d.items()))

class Cooker(http.client.HTTPSConnection):
    def __init__(self, *ag, **kw):
        super().__init__(*ag, **kw)
        self.cookies = {}
    def request(self, method, url, body=None, headers={}, decode=lambda i:i):
        headers = { k:v for k,v in headers.items() }
        handle_cookie = not 'Cookie' in headers
        if handle_cookie:
            headers['Cookie'] = '; '.join((f'{key}={value}' for key, value in self.cookies.items()))
        if isinstance(body, dict):
            body = UrlArgs.dict2args(body)
        super().request(method, url, body, headers)
        resp = self.getresponse()
        resp.data = decode(resp.read())
        new_cookies = resp.getheader('Set-Cookie')
        if new_cookies and handle_cookie:
            for cookie in new_cookies.split(','):
                key, value = cookie.split(';')[0].strip().split('=')
                self.cookies[key] = value
        return resp

r = random.randint(0, 10000)

email = f'mercisubway{r}@gmail.com'
storeNumber = '53994'
tickerNb = r
customerValue = 10
recommend = 10
eatSubway = 15
aspects = [10, 10, 10, 10, 10, 10]

with closing(Cooker(
        'www.parleznousdesubway.fr',
        context=ssl._create_unverified_context()
)) as conn:
    resp = conn.request('GET', '/')
    conn.request('GET', resp.getheader('Location'))
    sid = str(random.random())
    resp = conn.request('POST', '/WebServices/CE/Survey.asmx/SearchSurvey', {
        'LangId': '17',
        'sid': sid,
        'storeNumber': storeNumber
    }, {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }, decode=JoliSoup)
    url = resp.data.RecomendedPage.text
    d = UrlArgs.args2dict(url)
    surveyId = d['surveyId']
    storeId = d['storeId']
    resp = conn.request(
        'GET',
        "/WebServices/CE/survey.asmx/GetSurveyById?"
        f"surveyId={surveyId}&"
        f"storeId={storeId}&"
        f"sid={sid}",
        decode=JoliSoup
    )
    questions = json.loads(resp.data.string)['CESurveyService']['Question']['CEQuestion']
    eatSubwayConf = []
    aspectsConf = []
    for question in questions:
        try:
            answers = question['QuestionListAnswer']['CEQuestionListAnswer']
        except TypeError as e:
            try:
                subquestions = question['ChildQuestionList']['CEQuestion']
            except TypeError as e:
                pass
            else:
                for question in subquestions:
                    answers = question['QuestionListAnswer']['CEQuestionListAnswer']
                    values = [answer['Id'] for answer in answers]
                    aspectsConf.append({ 'id': question['Id'], 'values': values })
        else:
            values = [answer['Id'] for answer in answers]
            if len(answers) == 11:
                recommendConf = { 'id': question['Id'], 'values': values }
            elif len(answers) == 31:
                eatSubwayConf.append({ 'id': question['Id'], 'values': values })
    s = SubwayForm.generate_post(
        surveyId, storeId, tickerNb,
        sid, email, customerValue,
        recommendConf, recommend,
        eatSubwayConf, eatSubway,
        zip(aspectsConf, aspects)
    )
    resp = conn.request('POST', '/WebServices/CE/survey.asmx/SaveSurvey', s, {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }, decode=JoliSoup)
    txt = resp.data.Description.text
    if resp.data.Status.text == 'OK':
        resp = conn.request('POST', f'/ContentManager/{txt}')
        code = resp.data.split(b'<span id="ctl03_lblTag">')[1].split(b'</span>')[0].strip().decode()
        print(code)
    else:
        print(txt)
