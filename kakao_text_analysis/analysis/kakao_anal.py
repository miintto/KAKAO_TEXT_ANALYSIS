# -*- coding: utf-8 -*-

import os
from  . import BaseAnal, KakaoKoNLPy
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

### matplotlib에 한글 폰트 설정
fpath = os.path.dirname(__file__)+'/fonts/NanumGothicBold.ttf'
font = lambda fsize : fm.FontProperties(fname=fpath, size=fsize)


class KakaoAnal(BaseAnal):
    '''
    가공된 Dataframe을 바탕으로 차트를 출력
    '''
    def __init__(self, raw_text):
        super().__init__(raw_text)


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

        ax.set_title('월별 이용자 채팅 ('+self.start_date+' ~ '+self.save_date[:10]+')', fontproperties=font(16))
        plt.show()


    def chart_count_by_month_rate(self):
        '''
        월 별로 이용자의 말풍선 비율을 출력
        '''
        cmap = plt.get_cmap("Set3")
        colors = cmap(range(len(self.user_names)))
        yy_month = [str(month[2:]) for month in self.Month]

        fig, ax = plt.subplots(figsize = (12, 7))
        if len(yy_month)==1:
            dat_month_chat_per = [per[0] for per in self.dat_month_chat_per]
            cumsum = [sum(dat_month_chat_per[i+1:]) for i in range(len(self.user_names))]
            for i in range(len(self.user_names)):
                ax.bar(yy_month, dat_month_chat_per[i], color = colors[i], bottom=cumsum[i])
            plt.legend(self.user_names, prop=font(12), loc='center', bbox_to_anchor=(1.1, 0.5))

        else:
            ax.stackplot(yy_month, self.dat_month_chat_per[::-1], labels=self.user_names[::-1], colors=colors[::-1])
            ax.set_xticklabels(yy_month, fontproperties=font(10))
            handles, labels = ax.get_legend_handles_labels()
            plt.legend(reversed(handles), reversed(labels), prop=font(12), loc='center', bbox_to_anchor=(1.1, 0.5))

        ax.set_xlabel('월 (Month)', fontproperties=font(12))
        ax.set_ylabel('점유율 (%)', fontproperties=font(12))

        chartBox = ax.get_position()
        ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.9, chartBox.height])

        for edge, spine in ax.spines.items():
            spine.set_visible(False)

        ax.set_title('월별 이용자 점유율 ('+self.start_date+' ~ '+self.save_date[:10]+')', fontproperties=font(16))
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

        ax.set_title('톡방 점유율 (%) ('+self.start_date+' ~ '+self.save_date[:10]+')', fontproperties=font(16))
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

        ax.set_title('요일 시간별 채팅 ('+self.start_date+' ~ '+self.save_date[:10]+')', fontproperties=font(16))
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
                ggtitle('"'+user_name+'" 이용자의 요일, 시간별 채팅 ('+self.start_date+' ~ '+self.save_date[:10]+')')+
                scale_fill_gradient2(high = 'steelblue', low = 'white')+
                theme(figure_size = (12, 5), plot_title = element_text(size=20), text = element_text(fontproperties=font))
               )


    def chart_count_word_by_user(self, word):
        user_set = []
        for _, name, chat in self.dat_chat:
            if word in chat:
                user_set.append(name)

        dat_count_user_by_word = [user_set.count(name) for name in self.user_names]
        user_names = sorted(self.user_names, key=lambda i : dat_count_user_by_word[self.user_names.index(i)], reverse=True)
        dat_count_user_by_word.sort(reverse=True)

        try:
            user_len = dat_count_user_by_word.index(0)
            dat_count_user_by_word = dat_count_user_by_word[:user_len]
            user_names = user_names[:user_len]
        except:
            pass

        cmap = plt.get_cmap("Set3")
        colors = cmap(range(len(user_names)))

        fig, ax = plt.subplots(figsize = (12, 7))
        ax.bar(range(len(user_names)), dat_count_user_by_word, color=colors)
        ax.set_xticks(range(len(user_names)))
        ax.set_xticklabels(user_names, fontproperties=font(12))

        rects = ax.patches
        for rect, label in zip(rects, dat_count_user_by_word):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2, height, label, ha='center')

        for edge, spine in ax.spines.items():
            spine.set_visible(False)

        ax.set_title('\''+word+'\' 단어 사용 빈도 ('+self.start_date+' ~ '+self.save_date[:10]+')', fontproperties=font(16))
        plt.show()


    def chart_all(self):

        cmap = plt.get_cmap("Set3")
        colors = cmap(range(len(self.user_names)))
        yy_month = [str(month[2:]) for month in self.Month]
        fig, axs = plt.subplots(2, 2, figsize = (18, 10))
        plt.suptitle(self.title+' 종합 분석 ('+self.start_date+' ~ '+self.save_date[:10]+')', fontproperties=font(20))

        ### chart_count_by_month
        im1 = axs[0, 0].imshow(self.dat_month_chat, cmap='GnBu', aspect='auto')
        axs[0, 0].set_xticks(range(len(self.Month)))
        axs[0, 0].set_yticks(range(len(self.user_names)))
        axs[0, 0].set_xticklabels(yy_month, fontproperties=font(10))
        axs[0, 0].set_yticklabels(self.user_names, fontproperties=font(10))
        fig.colorbar(im1, ax=axs[0, 0], orientation='vertical', shrink=0.5)

        #### chart_count_by_month_rate
        if len(yy_month)==1:
            dat_month_chat_per = [per[0] for per in self.dat_month_chat_per]
            cumsum = [sum(dat_month_chat_per[i+1:]) for i in range(len(self.user_names))]
            for i in range(len(self.user_names)):
                axs[1, 0].bar(yy_month, dat_month_chat_per[i], color = colors[i], bottom=cumsum[i])
            axs[1, 0].legend(self.user_names, prop=font(10), loc='center', bbox_to_anchor=(1.1, 0.5))
        else:
            axs[1, 0].stackplot(yy_month, self.dat_month_chat_per[::-1], labels=self.user_names[::-1], colors=colors[::-1])
            axs[1, 0].set_xticklabels(yy_month, fontproperties=font(10))
            handles, labels = axs[1, 0].get_legend_handles_labels()
            axs[1, 0].legend(reversed(handles), reversed(labels), prop=font(10), loc='center', bbox_to_anchor=(1.1, 0.5))

        chartBox = axs[1, 0].get_position()
        axs[1, 0].set_position([chartBox.x0, chartBox.y0, chartBox.width*0.9, chartBox.height])

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


    def word_cloud(self):
        konlpy = KakaoKoNLPy(self.dat_chat)
        array = konlpy.word_cloud()

        fig = plt.figure(figsize=(12, 7))
        plt.imshow(array, interpolation="bilinear")
        plt.axis("off")
        plt.suptitle('주 사용 단어 ('+self.start_date+' ~ '+self.save_date[:10]+')', fontproperties=font(16))
        plt.show()

    def _analysis_by_user(self, user_name):
        self.target_name = [name for name in self.user_names if name != user_name]
        month_by_user = []
        dat_user_chat_group = []
        user_dict = {name:0 for name in self.user_names}
        pre_date = date_1 = dt.datetime(1990, 1, 1, 0, 0)
        for date, name, _ in self.dat_chat:
            if name == user_name:
                month_by_user.append(date[:7])
            dt_date = dt.datetime.strptime(date, "%Y-%m-%d %H:%M")
            time_gap = (dt_date - pre_date)
            if ((time_gap.days>1) | (time_gap.seconds>60*10)):
                if user_dict[user_name]>0:
                    dat_user_chat_group.append(user_dict)
                user_dict = {name:0 for name in self.user_names}
            if name=='':
                pass
            else:
                user_dict[name]+=1
            pre_date = dt_date
        if user_dict[user_name]>0:
            dat_user_chat_group.append(user_dict)

        self.dat_month_chat_by_user = [month_by_user.count(month) for month in self.Month]

        self.sum_chat = []
        for name in self.target_name:
            self.sum_chat.append(sum([line[name] for line in dat_user_chat_group]))

        wkdays = ['월', '화', '수', '목', '금', '토', '일']
        hours = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
        week_days=[]
        for line in self.dat_chat:
            if line[1] == user_name:
                week_days.append([dt.datetime.weekday(dt.datetime.strptime(line[0], '%Y-%m-%d %H:%M')), line[0][11:13]])

        dat_by_wkday_by_user = []
        for j in range(7):
            time_set = []
            for wkd, time in week_days:
                if wkd == j:
                    time_set.append(time)
            dat_by_wkday_by_user.append([time_set.count(hour) for hour in hours])
        self.dat_by_wkday_by_user = dat_by_wkday_by_user


    def chart_all_by_user(self, user_name):
        self._analysis_by_user(user_name)
        konlpy = KakaoKoNLPy(self.dat_chat)
        array = konlpy.word_cloud_by_user(user_name)

        cmap = plt.get_cmap("Set3")
        colors = cmap(range(len(self.target_name)))

        fig, axs = plt.subplots(2, 2, figsize=(18, 10))
        plt.suptitle('\''+user_name+'\' 님 종합 분석 ('+self.start_date+' ~ '+self.save_date[:10]+')', fontproperties=font(20))

        axs[0, 0].bar(self.Month, self.dat_month_chat_by_user)
        axs[0, 0].set_xticks(range(len(self.Month)))
        axs[0, 0].set_xticklabels(self.Month, fontproperties=font(10))

        axs[0, 1].bar(self.target_name, self.sum_chat, color = colors)
        axs[0, 1].set_xticks(range(len(self.target_name)))
        axs[0, 1].set_xticklabels(self.target_name, fontproperties=font(10))

        axs[1, 0].imshow(array, interpolation="bilinear")

        im2 = axs[1, 1].imshow(self.dat_by_wkday_by_user, cmap='GnBu', aspect='auto')
        axs[1, 1].set_xticks(range(24))
        axs[1, 1].set_yticks(range(7))
        axs[1, 1].set_xticklabels(range(24), fontproperties=font(10))
        axs[1, 1].set_yticklabels(['월', '화', '수', '목', '금', '토', '일'], fontproperties=font(10))
        fig.colorbar(im2, ax=axs[1, 1], orientation='horizontal', fraction=.1, shrink=0.5)

        for ax in [axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]]:
            for edge, spine in ax.spines.items():
                spine.set_visible(False)

        axs[0, 0].set_title('\''+user_name+'\' 님의 월별 대화량', fontproperties=font(15))
        axs[0, 1].set_title('\''+user_name+'\' 님과 대화한 유저', fontproperties=font(15))
        axs[1, 0].set_title('\''+user_name+'\' 님의 주 사용 단어', fontproperties=font(15))
        axs[1, 1].set_title('\''+user_name+'\' 님의 요일 시간별 채팅', fontproperties=font(15))
        plt.show()
