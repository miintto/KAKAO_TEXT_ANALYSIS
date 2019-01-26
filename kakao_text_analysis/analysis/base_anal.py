# -*- coding: utf-8 -*-

from ..models import *
import datetime as dt


class BaseAnal:
    '''
    분석을 시작하기 전 Dataframe을 전처리
    raw_text에 원본 텍스트파일을 입력받아 
    Dateframe형태로 가공 후 dat_chat에 저장
    '''
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.user_names = []


    def initialize(self):
        self.title = self.raw_text[0][:-1]
        self.classify_type()
        self.convert()


    def classify_type(self):
        '''
        모바일 버전인지 PC버전인지 판별
        '''
        if self.raw_text[3]=='\n':
            self.types = 'Mobile'
        else:
            self.types = 'PC'


    def convert(self):
        if self.types=='Mobile':
            self._set_save_date_mobile()
            convert = Convertor(self.raw_text)
        elif self.types=='PC':
            self._set_save_date_PC()
            convert = ConvertorPC(self.raw_text)
        self.dat_chat = convert.dat_chat


    def _set_save_date_mobile(self):
        save_date = self.raw_text[1][(self.raw_text[1].find(':')+2):-1]
        save_date = save_date.replace('오전', 'AM').replace('오후', 'PM')
        self.save_date = dt.datetime.strftime(dt.datetime.strptime(save_date, "%Y년 %m월 %d일 %p %I:%M"), "%Y-%m-%d %H:%M")


    def _set_save_date_PC(self):
        self.save_date = self.raw_text[1][(self.raw_text[1].find(':')+2):-4]


    def analysis(self):
        self._find_names()
        self._sort_names()

        Month = []
        for date, _, _ in self.dat_chat:
            if date[:7] not in Month:
                Month.append(date[:7])
        self.Month = Month

        dat_month_chat = []
        for user_name in self.user_names:
            month_by_name = [date[:7] for date, name, _ in self.dat_chat if name==user_name]
            dat_month_chat.append([month_by_name.count(month) for month in Month])
        self.dat_month_chat = dat_month_chat

        sum_by_month = [sum(dat_month_chat[i][j] for i in range(len(self.user_names))) for j in range(len(Month))]
        dat_month_chat_per = []
        for j in range(len(self.user_names)):
            dat_month_chat_per.append([dat_month_chat[j][i] / sum_by_month[i] * 100 for i in range(len(Month))])
        self.dat_month_chat_per = dat_month_chat_per

        wkdays = ['월', '화', '수', '목', '금', '토', '일']
        hours = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
        week_days=[]
        for line in self.dat_chat:
            week_days.append(dt.datetime.weekday(dt.datetime.strptime(line[0], '%Y-%m-%d %H:%M')))

        dat_by_wkday = []
        for j in range(7):
            time_set = []
            for i in range(len(self.dat_chat)):
                if week_days[i] == j:
                    time_set.append(self.dat_chat[i][0][11:13])
            dat_by_wkday.append([time_set.count(hour) for hour in hours])
        self.dat_by_wkday = dat_by_wkday


    def _find_names(self):
        '''
        사용자의 이름 가져오기
        '''
        names = []
        for line in self.dat_chat:
            names.append(line[1])
        for name in names:
            if not (name in self.user_names):
                self.user_names.append(name)
        try:
            self.user_names.remove('')
        except:
            pass


    def _sort_names(self):
        '''
        사용자 이름을 전체 말풍선개수 순으로 sorting
        '''
        names = []
        for i in range(len(self.dat_chat)):
            names.append(self.dat_chat[i][1])
        user_chat = []
        for name in self.user_names:
            user_chat.append(names.count(name))
        self.user_names = sorted(self.user_names, key = lambda i : user_chat[self.user_names.index(i)], reverse=True)
        user_chat.sort(reverse=True)
        self.user_chat = user_chat
