import os
import inspect
from  . import BaseAnal
import pandas as pd
import datetime as dt
from plotnine import *
import matplotlib.font_manager as fm

### matplotlib에 한글 폰트 설정
fpath = os.path.dirname(inspect.getabsfile(BaseAnal))+'/fonts/NanumGothicBold.ttf'
font = fm.FontProperties(fname=fpath, size=15)


class KakaoAnal(BaseAnal):
    '''
    가공된 Dataframe을 바탕으로 차트를 출력
    '''
    def chart_count_by_month(self):
        '''
        월 별로 이용자의 말풍선 개수를 출력
        '''
        Month = [] ### 월별 간격 계산
        Month_idx = []
        for i in range(len(self.dat_chat)):
            if not self.dat_chat[i][0][0:7] in Month:
                Month.append(self.dat_chat[i][0][0:7])
                Month_idx.append(i)
                
        Month_idx.append(len(self.dat_chat))
        dat_month_chat = [] ### 월별 채팅 계산
        for j in range(len(Month)):
            names = []
            for i in range(Month_idx[j], Month_idx[j+1]):
                names.append(self.dat_chat[i][1])
            for name in self.user_names:
                dat_month_chat.append([name, Month[j], names.count(name)])

        dat_month_chat = pd.DataFrame(dat_month_chat)
        dat_month_chat.columns = ['Name', 'Month', 'Chat']
        dat_month_chat['Name'] = pd.Categorical(dat_month_chat['Name'], categories=self.user_names, ordered=True)
        
        return (ggplot(dat_month_chat)+
                geom_tile(aes('Month', 'Name', fill = 'Chat'))+
                geom_text(aes('Month', 'Name', label = 'Chat'))+
                ggtitle('월별 이용자 채팅 ('+self.dat_chat[0][0][:11]+' ~ '+self.save_date[:11]+')')+
                scale_fill_gradient2(high = 'steelblue', low = 'white')+
                theme(figure_size = (15, 7), plot_title = element_text(size=20), text = element_text(fontproperties=font))
               )
    
    def chart_count_by_month_rate(self):
        '''
        월 별로 이용자의 말풍선 비율을 출력
        '''
        Month = [] ### 월별 간격 계산
        Month_idx = []
        for i in range(len(self.dat_chat)):
            if not self.dat_chat[i][0][0:7] in Month:
                Month.append(self.dat_chat[i][0][0:7])
                Month_idx.append(i)
                
        Month_idx.append(len(self.dat_chat))
        dat_month_chat = [] ### 월별 채팅 계산
        for j in range(len(Month)):
            names = []
            for i in range(Month_idx[j], Month_idx[j+1]):
                names.append(self.dat_chat[i][1])
            for name in self.user_names:
                dat_month_chat.append([name, Month[j], names.count(name)])

        dat_month_chat = pd.DataFrame(dat_month_chat)
        dat_month_chat.columns = ['Name', 'Month', 'Chat']
        dat_month_chat['Name'] = pd.Categorical(dat_month_chat['Name'], categories=self.user_names[::-1], ordered=True)
        
        return (ggplot(dat_month_chat)+
                geom_bar(aes('Month', 'Chat', fill='Name'), stat = 'identity', position = 'fill')+
                ggtitle('월별 점유율 ('+self.dat_chat[0][0][:11]+' ~ '+self.save_date[:11]+')')+
                scale_fill_brewer(type='qual', palette="Set3")+
                theme(figure_size = (15, 7), plot_title = element_text(size=20), text = element_text(fontproperties=font))
               )

    def chart_pie(self):
        '''
        이용자별 톡방 점유율 출력
        (0 ~ 100, 단위 : %)
        '''
        dat_per = [i/sum(self.user_chat)*100 for i in self.user_chat]
        dat_user_chat = pd.DataFrame({'Name':self.user_names, 'Per':dat_per})
        dat_user_chat['Per'] = dat_user_chat['Per'].round(2)
        dat_user_chat['Per_ctr'] = pd.Series.cumsum(dat_user_chat['Per'])-dat_user_chat['Per']/2
        dat_user_chat['Name'] = pd.Categorical(dat_user_chat['Name'], categories=self.user_names[::-1], ordered=True)

        return (ggplot(dat_user_chat)+
                geom_bar(aes('0', 'Per', fill = 'Name'), stat = 'identity')+
                geom_text(aes('0', 'Per_ctr', label = 'Per'))+
                ggtitle('잉여력 (%) ('+self.dat_chat[0][0][:11]+' ~ '+self.save_date[:11]+')')+
                scale_fill_brewer(type='qual', palette="Set3")+
                theme(figure_size = (7, 7), plot_title = element_text(size=20), text = element_text(fontproperties=font))
               )

    def chart_count_by_weekdays(self):
        '''
        요일×시간 별 말풍선 개수 출력
        '''
        week_days=[]
        for line in self.dat_chat:
            week_days.append(dt.datetime.weekday(dt.datetime.strptime(line[0], '%Y-%m-%d %H:%M')))
        dat_by_wkday = []
        for j in range(7):
            time_set = []
            for i in range(len(self.dat_chat)):
                if week_days[i] == j:
                    time_set.append(self.dat_chat[i][0][11:13])
            wkdays = ['월', '화', '수', '목', '금', '토', '일']
            hours = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
            for hour in hours:
                dat_by_wkday.append([wkdays[j], hour, time_set.count(hour)])

        dat_by_wkday = pd.DataFrame(dat_by_wkday)
        dat_by_wkday.columns = ['Weekdays', 'Hours', 'Chats']
        dat_by_wkday['Weekdays'] = pd.Categorical(dat_by_wkday['Weekdays'], categories=wkdays, ordered=True)
        
        return (ggplot(dat_by_wkday)+
                geom_tile(aes('Hours', 'Weekdays', fill = 'Chats'))+
                geom_text(aes('Hours', 'Weekdays', label = 'Chats'))+
                ggtitle('요일, 시간별 채팅 ('+self.dat_chat[0][0][:11]+' ~ '+self.save_date[:11]+')')+
                scale_fill_gradient2(high = 'steelblue', low = 'white')+
                theme(figure_size = (15, 7), plot_title = element_text(size=20), text = element_text(fontproperties=font))
               )
    
    def chart_count_by_weekdays_by_user(self):
        '''
        원하는 이용자를 입력받아서
        요일×시간 별 말풍선 개수 출력
        '''
        user_check = False
        print('[이름을 입력하시오]')
        while(not user_check):
            user_name = input()
            if user_name in self.user_names:
                user_check = True
            else:
                print('[목록에 없습니다. 다시 한번 입력해주십시오.]')
        print('[입력되었습니다.]')

        week_days=[]
        for line in self.dat_chat:
            week_days.append(dt.datetime.weekday(dt.datetime.strptime(line[0], '%Y-%m-%d %H:%M')))
        dat_by_wkday = []
        for j in range(7):
            time_set = []
            for i in range(len(self.dat_chat)):
                if (week_days[i] == j) & (self.dat_chat[i][1] == user_name):
                    time_set.append(self.dat_chat[i][0][11:13])
            wkdays = ['월', '화', '수', '목', '금', '토', '일']
            hours = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
            for hour in hours:
                dat_by_wkday.append([wkdays[j], hour, time_set.count(hour)])

        dat_by_wkday = pd.DataFrame(dat_by_wkday)
        dat_by_wkday.columns = ['Weekdays', 'Hours', 'Chats']
        dat_by_wkday['Weekdays'] = pd.Categorical(dat_by_wkday['Weekdays'], categories=wkdays, ordered=True)

        return (ggplot(dat_by_wkday)+
                geom_tile(aes('Hours', 'Weekdays', fill = 'Chats'))+
                geom_text(aes('Hours', 'Weekdays', label = 'Chats'))+
                ggtitle('"'+user_name+'" 이용자의 요일, 시간별 채팅 ('+self.dat_chat[0][0][:11]+' ~ '+self.save_date[:11]+')')+
                scale_fill_gradient2(high = 'steelblue', low = 'white')+
                theme(figure_size = (15, 7), plot_title = element_text(size=20), text = element_text(fontproperties=font))
               )