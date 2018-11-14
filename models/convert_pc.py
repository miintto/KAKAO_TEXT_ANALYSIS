import datetime as dt


class ConvertorPC(object):
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
            return [line, '', '']
        
    def convert_table(self):
        self.date = ''
        for line in self.raw_text:
            try:
                date = line.replace('---------------', '')[1:-6]
                self.date = dt.datetime.strftime(dt.datetime.strptime(date, "%Y년 %m월 %d일"), "%Y-%m-%d")
            except:
                self.dat_chat.append(self.split_by(line))