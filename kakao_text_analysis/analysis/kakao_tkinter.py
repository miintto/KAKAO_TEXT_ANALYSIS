# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from . import KakaoAnal


class KakaoTkinter:
    def __init__(self, root):
        self.root = root
        self.is_open_text_file = False
        self.is_find_date = False
        self.run()


    def run(self):
        self.root.title('kakao text analysis')

        self.file_root = StringVar(self.root, value='')
        self.start_date = StringVar(self.root, value='')

        self.label_0 = Label(self.root, text = 'Kakao Talk 대화 분석', height=2)
        self.label_0.config(font=('', 20))
        self.label_0.grid(row=0, column=1)
        self.label_blk0 = Label(self.root, text = '', width=8)
        self.label_blk0.grid(row=0, column=0)
        self.label_blk1 = Label(self.root, text = '', width=8)
        self.label_blk1.grid(row=0, column=2)

        self.label_1 = Label(self.root, text = '텍스트 파일 경로 : ')
        self.label_1.grid(row=1, column=1, sticky='w')
        self.text_1 = Entry(self.root, width=50, textvariable = self.file_root)
        self.text_1.grid(row=2, column=1)
        self.buttun_0 = Button(self.root, text = '확인', command = self.open_file)
        self.buttun_0.grid(row=3, column=1)

        self.label_2 = Label(self.root, text = '')
        self.label_2.grid(row=4, column=1)

        self.label_3 = Label(self.root, text = '시작할 날짜 :  ex) 2018-01-01')
        self.label_3.grid(row=5, column=1, sticky='w')
        self.text_2 = Entry(self.root, width=50, textvariable = self.start_date)
        self.text_2.grid(row=6, column=1)
        self.buttun_1 = Button(self.root, text = '확인', command = self.analysis)
        self.buttun_1.grid(row=7, column=1)

        self.label_4 = Label(self.root, text = '')
        self.label_4.grid(row=8, column=1)

        self.buttun_2 = Button(self.root, text = '종합 분석', width=25, command = self.chart_all, height=2)
        self.buttun_2.grid(row=9, column=1)
        self.buttun_3 = Button(self.root, text = '월별 이용자 채팅', width=25, command = self.chart_count_by_month)
        self.buttun_3.grid(row=10, column=1)
        self.buttun_4 = Button(self.root, text = '월별 이용자 점유율', width=25, command = self.chart_count_by_month_rate)
        self.buttun_4.grid(row=11, column=1)
        self.buttun_5 = Button(self.root, text = '전체기간 이용자 점유율', width=25, command = self.chart_pie)
        self.buttun_5.grid(row=12, column=1)
        self.buttun_6 = Button(self.root, text = '요일 시간별 채팅', width=25, command = self.chart_count_by_weekdays)
        self.buttun_6.grid(row=13, column=1)
        self.label_blk2 = Label(self.root, text = '', height=2)
        self.label_blk2.grid(row=14, column=2)

        self.root.mainloop()


    def open_file(self):
        file_root = self.file_root.get()
        ######## --DELETE -- ########
        file_root = '/home/minjae/다운로드/KakaoTalkChats (2).txt'
        ###############################
        try:
            f = open(file_root, 'r', encoding='utf-8-sig')
            self.raw_text = f.readlines()
            self.label_1.configure(text='텍스트 파일 경로 :  - 파일을 성공적으로 불러왔습니다.')
            self.is_open_text_file = True
        except:
            messagebox.showinfo('Error', '파일을 열 수 없습니다.')


    def analysis(self):
        if not self.is_open_text_file:
            messagebox.showinfo('Error', '먼저 텍스트 파일을 불러와주세요.')
        else:
            self.kakao = KakaoAnal(self.raw_text)
            start_line = -1
            start_date = self.start_date.get()
            for i in range(len(self.kakao.dat_chat)):
                if start_date in self.kakao.dat_chat[i][0][0:10]:
                    start_line = i
                    break
            if start_line == -1:
                messagebox.showinfo('Error', '해당 날짜를 찾을 수 없습니다.')
            else:
                self.is_find_date = True
                self.kakao.dat_chat = self.kakao.dat_chat[start_line:]
                self.kakao.find_names()
                self.kakao.sort_names()
                self.kakao.analysis()
                self.label_3.configure(text='시작할 날짜 :  - 분석 완료!')


    def chart_count_by_month(self):
        if not self.is_open_text_file:
            messagebox.showinfo('Error', '먼저 텍스트 파일을 불러와주세요.')
        elif not self.is_find_date:
            messagebox.showinfo('Error', '먼저 분석을 시작할 날짜를 입력해주세요.')
        else:
            return self.kakao.chart_count_by_month()


    def chart_count_by_month_rate(self):
        if not self.is_open_text_file:
            messagebox.showinfo('Error', '먼저 텍스트 파일을 불러와주세요.')
        elif not self.is_find_date:
            messagebox.showinfo('Error', '먼저 분석을 시작할 날짜를 입력해주세요.')
        else:
            return self.kakao.chart_count_by_month_rate()


    def chart_pie(self):
        if not self.is_open_text_file:
            messagebox.showinfo('Error', '먼저 텍스트 파일을 불러와주세요.')
        elif not self.is_find_date:
            messagebox.showinfo('Error', '먼저 분석을 시작할 날짜를 입력해주세요.')
        else:
            return self.kakao.chart_pie()


    def chart_count_by_weekdays(self):
        if not self.is_open_text_file:
            messagebox.showinfo('Error', '먼저 텍스트 파일을 불러와주세요.')
        elif not self.is_find_date:
            messagebox.showinfo('Error', '먼저 분석을 시작할 날짜를 입력해주세요.')
        else:
            return self.kakao.chart_count_by_weekdays()


    def chart_all(self):
        if not self.is_open_text_file:
            messagebox.showinfo('Error', '먼저 텍스트 파일을 불러와주세요.')
        elif not self.is_find_date:
            messagebox.showinfo('Error', '먼저 분석을 시작할 날짜를 입력해주세요.')
        else:
            return self.kakao.chart_all()
