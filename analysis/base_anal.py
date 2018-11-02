from models.convert import Convertor
import datetime as dt


class BaseAnal(object):
    '''
    분석 시작전 대략적인 전처리 작업.
    카카오톡 채팅 파일 변환 및 분석 시작할 날짜부터 가공
    '''
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.user_names = []
        self.initialize()
        
    def initialize(self):
        self.title = self.raw_text[0][:-1]
        self.set_save_date()
        convert = Convertor(self.raw_text)
        self.dat_chat = convert.dat_chat
        self.find_start_line()
        self.find_names()
        self.sort_names()
        
    def set_save_date(self):
        save_date = self.raw_text[1][(self.raw_text[1].find(':')+2):-1]
        save_date = save_date.replace('오전', 'AM').replace('오후', 'PM')
        self.save_date = dt.datetime.strftime(dt.datetime.strptime(save_date, "%Y년 %m월 %d일 %p %I:%M"), "%Y-%m-%d %H:%M")
        
    def find_start_line(self):
        start_line = -1
        print('[시작할 날짜를 입력해주십시오. (ex. 2018-01-01)]')
        while(start_line == -1):
            start_date = input()
            for i in range(len(self.dat_chat)):
                if start_date in self.dat_chat[i][0][0:10]:
                    start_line = i
                    break
            if start_line == -1:
                print('[날짜를 찾을 수 없습니다. 다시 한번 입력해주십시오.]')
        self.dat_chat = self.dat_chat[start_line:]
            
    def find_names(self):
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
        
    def sort_names(self):
        names = []
        for i in range(len(self.dat_chat)):
            names.append(self.dat_chat[i][1])
        user_chat = []
        for name in self.user_names:
            user_chat.append(names.count(name))
        self.user_names = sorted(self.user_names, key = lambda i : user_chat[self.user_names.index(i)])
        user_chat.sort()
        self.user_chat = user_chat
     