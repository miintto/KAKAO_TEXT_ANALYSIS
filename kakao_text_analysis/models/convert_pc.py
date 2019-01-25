# -*- coding: utf-8 -*-

import datetime as dt


class ConvertorPC:
    '''
    카카오톡 채팅 내용이 담긴 텍스트파일을 raw_text에 입력받아
    dataframe 형태로 변환한 후, dat_chat 에 저장
    (PC버전만 유효)
    '''
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.dat_chat = []
        self.convert_table()


    def split_by(self, line):
        try:
            split_1 = line.find(']')
            split_2 = line.find(':')
            name = line[1:split_1]
            time = line[(split_1+3):split_2+3]
            time = time.replace('오전', 'AM').replace('오후', 'PM')
            time = dt.datetime.strftime(dt.datetime.strptime(time, "%p %I:%M"), "%H:%M")
            datetime = self.date+' '+time
            return [datetime, name, line[split_2+5:]]
        except:
            return ['', '', line]


    def fix_table(self, data):
        for i in range(1, len(data))[::-1]:
            if not data[i][0]:
                data[i-1][2] = data[i-1][2]+data[i][2]
                del data[i]
        del data[0]


    def convert_table(self):
        '''
        [datetime, name, chat]
        dim : (N×3)
        '''
        self.date = ''
        for line in self.raw_text:
            try:
                date = line.replace('---------------', '')[1:-6]
                self.date = dt.datetime.strftime(dt.datetime.strptime(date, "%Y년 %m월 %d일"), "%Y-%m-%d")
            except:
                self.dat_chat.append(self.split_by(line))
        self.fix_table(self.dat_chat)
