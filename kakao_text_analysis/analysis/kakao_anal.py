# -*- coding: utf-8 -*-

import os
import inspect
from  . import BaseAnal
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

### matplotlib에 한글 폰트 설정
fpath = os.path.dirname(inspect.getabsfile(BaseAnal))+'/fonts/NanumGothicBold.ttf'
font = lambda fsize : fm.FontProperties(fname=fpath, size=fsize)


class KakaoAnal(BaseAnal):
    '''
    가공된 Dataframe을 바탕으로 차트를 출력
    '''
    def __init__(self, raw_text):
        super().__init__(raw_text)


    def analysis(self):
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


    def chart_count_by_month(self):
        '''
        월 별로 이용자의 말풍선 개수를 출력
        '''
        fig, ax = plt.subplots(figsize = (12, 7))
        ax.imshow(self.dat_month_chat, cmap='GnBu', aspect='auto')

        ax.set_xticks(range(len(self.Month)))
        ax.set_yticks(range(len(self.user_names)))
        ax.set_xticklabels([str(month[2:]) for month in self.Month])
        ax.set_yticklabels(self.user_names, fontproperties=font(10))
        ax.set_xlabel('월 (Month)', fontproperties=font(12))

        for i in range(len(self.user_names)):
            for j in range(len(self.Month)):
                ax.text(j, i, self.dat_month_chat[i][j], ha="center", va="center", color="black")

        for edge, spine in ax.spines.items():
            spine.set_visible(False)

        ax.set_title('월별 이용자 채팅 ('+self.dat_chat[0][0][:11]+' ~ '+self.save_date[:10]+')', fontproperties=font(16))
        plt.show()


    def chart_count_by_month_rate(self):
        '''
        월 별로 이용자의 말풍선 비율을 출력
        '''
        cmap = plt.get_cmap("Set3")
        colors = cmap(range(len(self.user_names)))
        yy_month = [str(month[2:]) for month in self.Month]

        fig, ax = plt.subplots(figsize = (12, 7))
        ax.stackplot(yy_month, self.dat_month_chat_per[::-1], labels=self.user_names[::-1], colors=colors[::-1])
        ax.set_xticklabels(yy_month, fontproperties=font(10))
        ax.set_xlabel('월 (Month)', fontproperties=font(12))
        ax.set_ylabel('점유율 (%)', fontproperties=font(12))

        chartBox = ax.get_position()
        ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.9, chartBox.height])
        handles, labels = ax.get_legend_handles_labels()
        plt.legend(reversed(handles), reversed(labels), prop=font(12), loc='center', bbox_to_anchor=(1.1, 0.5))

        for edge, spine in ax.spines.items():
            spine.set_visible(False)

        ax.set_title('월별 이용자 점유율 ('+self.dat_chat[0][0][:11]+' ~ '+self.save_date[:10]+')', fontproperties=font(16))
        plt.show()


    def chart_pie(self):
        '''
        이용자별 톡방 점유율 출력
        (0 ~ 100, 단위 : %)
        '''
        cmap = plt.get_cmap("Set3")
        colors = cmap(range(len(self.user_names)))

        fig, ax = plt.subplots(figsize = (8, 7))
        wedges, texts, autotexts = ax.pie(self.user_chat, labels=self.user_names, autopct='%1.2f%%', colors=colors)
        plt.setp(texts, fontproperties=font(12))

        ax.set_title('톡방 점유율 (%) ('+self.dat_chat[0][0][:11]+' ~ '+self.save_date[:10]+')', fontproperties=font(16))
        plt.show()


    def chart_count_by_weekdays(self):
        '''
        요일×시간 별 말풍선 개수 출력
        '''
        fig, ax = plt.subplots(figsize = (12, 7))
        ax.imshow(self.dat_by_wkday, cmap='GnBu', aspect='auto')

        ax.set_xticks(range(24))
        ax.set_yticks(range(7))
        ax.set_xticklabels(range(24))
        ax.set_yticklabels(['월', '화', '수', '목', '금', '토', '일'], fontproperties=font(10))
        ax.set_xlabel('시간 (Hour)', fontproperties=font(12))
        ax.set_ylabel('요일 (Weekday)', fontproperties=font(12))

        for i in range(7):
            for j in range(24):
                ax.text(j, i, self.dat_by_wkday[i][j], ha="center", va="center", color="black")

        for edge, spine in ax.spines.items():
            spine.set_visible(False)

        ax.set_title('요일 시간별 채팅 ('+self.dat_chat[0][0][:11]+' ~ '+self.save_date[:10]+')', fontproperties=font(16))
        plt.show()


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
                ggtitle('"'+user_name+'" 이용자의 요일, 시간별 채팅 ('+self.dat_chat[0][0][:11]+' ~ '+self.save_date[:10]+')')+
                scale_fill_gradient2(high = 'steelblue', low = 'white')+
                theme(figure_size = (12, 5), plot_title = element_text(size=20), text = element_text(fontproperties=font))
               )


    def chart_all(self):

        cmap = plt.get_cmap("Set3")
        colors = cmap(range(len(self.user_names)))
        yy_month = [str(month[2:]) for month in self.Month]
        fig, axs = plt.subplots(2, 2, figsize = (18, 10))
        plt.suptitle(self.title+' 종합 분석 ('+self.dat_chat[0][0][:11]+' ~ '+self.save_date[:10]+')', fontproperties=font(20))

        ### chart_count_by_month
        im1 = axs[0, 0].imshow(self.dat_month_chat, cmap='GnBu', aspect='auto')
        axs[0, 0].set_xticks(range(len(self.Month)))
        axs[0, 0].set_yticks(range(len(self.user_names)))
        axs[0, 0].set_xticklabels(yy_month, fontproperties=font(10))
        axs[0, 0].set_yticklabels(self.user_names, fontproperties=font(10))
        fig.colorbar(im1, ax=axs[0, 0], orientation='vertical', shrink=0.5)


        #### chart_count_by_month_rate
        axs[1, 0].stackplot(yy_month, self.dat_month_chat_per[::-1], labels=self.user_names[::-1], colors=colors[::-1])
        axs[1, 0].set_xticklabels(yy_month, fontproperties=font(10))
        chartBox = axs[1, 0].get_position()
        axs[1, 0].set_position([chartBox.x0, chartBox.y0, chartBox.width*0.9, chartBox.height])
        handles, labels = axs[1, 0].get_legend_handles_labels()
        axs[1, 0].legend(reversed(handles), reversed(labels), prop=font(10), loc='center', bbox_to_anchor=(1.1, 0.5))

        ### chart_pie
        wedges, texts, autotexts = axs[0, 1].pie(self.user_chat, labels=self.user_names, autopct='%1.2f%%', colors=colors)
        plt.setp(texts, fontproperties=font(10))

        ### chart_count_by_weekdays
        im2 = axs[1, 1].imshow(self.dat_by_wkday, cmap='GnBu', aspect='auto')
        axs[1, 1].set_xticks(range(24))
        axs[1, 1].set_yticks(range(7))
        axs[1, 1].set_xticklabels(range(24), fontproperties=font(10))
        axs[1, 1].set_yticklabels(['월', '화', '수', '목', '금', '토', '일'], fontproperties=font(10))
        fig.colorbar(im2, ax=axs[1, 1], orientation='horizontal', fraction=.1, shrink=0.5)

        for ax in [axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]]:
            for edge, spine in ax.spines.items():
                spine.set_visible(False)

        axs[0, 0].set_title('월별 이용자 채팅', fontproperties=font(15))
        axs[1, 0].set_title('월별 이용자 점유율', fontproperties=font(15))
        axs[0, 1].set_title('톡방 점유율 (%)', fontproperties=font(15))
        axs[1, 1].set_title('요일 시간별 채팅', fontproperties=font(15))

        plt.show()
