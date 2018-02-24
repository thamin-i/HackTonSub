#!/usr/bin/env python3

import ssl
import json
import random
import datetime
import http.client

from web import JoliSoup, UrlArgs, Cooker

class Form:

    class Question:
        def __init__(self, qid, values):
            self.qid = qid
            self.values = values
        def fill(self, soup, value):
            ask = soup.find(questionId=self.qid)
            ask['finalValue'] = value
            ask['questionListId'] = self.values[value]

    def _builder(f):
        def wrap(self, *ag, **kw):
            f(self, *ag, **kw)
            return self
        return wrap

    datetime_fmt = '%Y|%-m|%-d|%-H|%-M|%-S|0|-60'

    def _get_datetime(self, seconds=0):
        return (self.now + datetime.timedelta(seconds=seconds)).strftime(Form.datetime_fmt)

    def _set_by_type(self, t, v):
        ask = self.soup.find(type=t)
        ask['answer'] = v
        ask['finalValue'] = v

    def _set_questions(self, questions, value):
        for question in questions:
            question.fill(self.soup, int(value))

    def __init__(self, storeId, eat_questions, grade_questions):
        try:
            with open('sample/{}.post'.format(storeId), 'r') as f:
                dummy_post = f.read()
        except FileNotFoundError as e:
            raise RuntimeError('Invalid store "{}"'.format(storeId))
        self.args = UrlArgs.args2dict(dummy_post)
        self.soup = JoliSoup(self.args['submitSet'])
        self.url, args = self.soup['URL'].split('?')
        self.url_args = UrlArgs.args2dict(args)
        self.eat_questions = eat_questions
        self.grade_questions = grade_questions
        self.now = datetime.datetime.now()
        self._set_by_type('STORE_ID', storeId)
        self.soup['storeId'] = storeId
        self.url_args['storeId'] = storeId

    @_builder
    def set_surveyId(self, surveyId):
        self.soup['surveyId'] = surveyId
        self.url_args['surveyId'] = surveyId

    @_builder
    def set_ticket(self, ticket):
        self._set_by_type('TEXTBOX', ticket)

    @_builder
    def set_eatCount(self, count):
        self._set_questions(self.eat_questions, count)

    @_builder
    def set_grade(self, grade):
        self._set_by_type('CUSTOMER_VALUE', grade)
        self.soup['customerValue'] = grade
        self._set_questions(self.grade_questions, grade)

    @_builder
    def set_sid(self, sid):
        self.args['sid'] = sid

    @_builder
    def set_email(self, email):
        self._set_by_type('EMAIL', email)
        self.soup['customerEmail'] = email

    def to_post(self):
        now = self._get_datetime()
        past = self._get_datetime(-1)
        self._set_by_type('DATETIME_CALENDAR_PICKER', past)
        self.soup['clientDate'] = now
        self.soup['receiptDate'] = past
        self.soup['URL'] = '{}?{}'.format(self.url, UrlArgs.dict2args(self.url_args))
        self.args['submitSet'] = str(self.soup)
        return UrlArgs.dict2args(self.args)

    @staticmethod
    def from_api(api, storeNumber):
        questions = api.get_survey(storeNumber)['CESurveyService']['Question']['CEQuestion']
        eat_questions = []
        grade_questions = []
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
                        grade_questions.append(Form.Question(question['Id'], [
                            answer['Id']
                            for answer in
                            question['QuestionListAnswer']['CEQuestionListAnswer']
                        ]))
                    else:
                        values = [answer['Id'] for answer in answers]
                        if len(answers) == 11:
                            grade_questions.append(Form.Question(question['Id'], values))
                        elif len(answers) == 31:
                            eat_questions.append(Form.Question(question['Id'], values))
        return (
            Form(api.storeId, eat_questions, grade_questions)
            .set_surveyId(api.surveyId)
            .set_sid(api.sid)
        )

class ApiHandler:

    def __init__(self):
        self.conn = Cooker('www.parleznousdesubway.fr', context=ssl._create_unverified_context())
        resp = self.conn.request('GET', '/')
        self.conn.request('GET', resp.getheader('Location'))
        self.sid = str(random.random())

    def get_survey(self, storeNumber):
        resp = self.conn.request('POST', '/WebServices/CE/Survey.asmx/SearchSurvey', {
            'LangId': '17',
            'sid': self.sid,
            'storeNumber': storeNumber
        }, {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }, decode=JoliSoup)
        url = resp.data.RecomendedPage.text
        d = UrlArgs.args2dict(url)
        self.surveyId = d['surveyId']
        self.storeId = d['storeId']
        resp = self.conn.request(
            'GET',
            "/WebServices/CE/survey.asmx/GetSurveyById?" +
            "surveyId={}&".format(self.surveyId) +
            "storeId={}&".format(self.storeId) +
            "sid={}".format(self.sid),
            decode=JoliSoup
        )
        return json.loads(resp.data.string)

    def get_cookie_code(
            self, ticket,
            email='bunnypixelarray@gmail.com',
            storeNumber='53994',
            eatCount=15,
            grade=10
    ):
        form = (Form.from_api(self, storeNumber)
                .set_ticket(ticket)
                .set_email(email)
                .set_eatCount(eatCount)
                .set_grade(grade)
        )
        resp = self.conn.request('POST', '/WebServices/CE/survey.asmx/SaveSurvey', form.to_post(), {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }, decode=JoliSoup)
        txt = resp.data.Description.text
        if resp.data.Status.text != 'OK':
            raise RuntimeError(txt)
        resp = self.conn.request('POST', '/ContentManager/{}'.format(txt))
        return resp.data.split(b'<span id="ctl03_lblTag">')[1].split(b'</span>')[0].strip().decode()

    def close(self):
        self.conn.close()
