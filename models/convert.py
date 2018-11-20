import datetime as dt


class Convertor(object):
    '''
    카카오톡 채팅 내용이 담긴 텍스트파일을 raw_text에 입력받아
    dataframe 형태로 변환한 후, dat_chat 에 저장
    (모바일버전만 유효)
    '''
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.dat_chat = []
        self.convert_table()
        
    def make_datetime(self, line):
        line = line.replace('오전', 'AM').replace('오후', 'PM')
        try:
            return dt.datetime.strftime(dt.datetime.strptime(line, "%Y년 %m월 %d일 %p %I:%M"), "%Y-%m-%d %H:%M")
        except:
            return ''
        
    def split_by(self, line):
        split_1 = line.find(',')
        split_2 = line.find(' : ')
        date = self.make_datetime(line[:split_1])
        name = line[(split_1+2):split_2]
        chat = line[(split_2+3):]
        if date == '':  ### 날짜가 없는 경우 -> 윗줄의 유저의 말풍선
            return ['', '', line]
        elif split_1 == -1:  ### ,가 없는 경우 -> 매 날짜 시작일
            return [date, '', '']
        elif split_2 == -1:  ###
            return [date, '', line[(split_1+2):]]
        else:
            return [date, name, chat]
        
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
        for line in self.raw_text:
            self.dat_chat.append(self.split_by(line))
        self.fix_table(self.dat_chat)
