from tkinter import *
from tkinter import messagebox
from . import KakaoAnal


class KakaoTkinter():
    def __init__(self, root):
        self.root = root
        self.is_open_text_file = False
        self.run()
        
    def run(self):
        self.root.title('kakao text analysis')
        self.root.geometry('500x500')

        self.label_0 = Label(self.root, text = 'kakao text analysis')
        self.label_0.grid(row=0, column=1)

        self.file_root = StringVar(self.root, value='')
        self.start_date = StringVar(self.root, value='')

        self.label_1 = Label(self.root, text = '텍스트 파일 경로')
        self.label_1.grid(row=1, column=0)
        self.text_1 = Entry(self.root, width=40, textvariable = self.file_root)
        self.text_1.grid(row=1, column=1)
        self.buttun_0 = Button(self.root, text = '확인', command = self.open_file)
        self.buttun_0.grid(row=2, column=1)

        self.label_2 = Label(self.root, text = '파일 경로 : ')
        self.label_2.grid(row=3, column=1)

        self.label_3 = Label(self.root, text = '시작할 날짜')
        self.label_3.grid(row=4, column=0)
        self.text_2 = Entry(self.root, width=40, textvariable = self.start_date)
        self.text_2.grid(row=4, column=1)
        self.buttun_1 = Button(self.root, text = '확인', command = self.analysis)
        self.buttun_1.grid(row=5, column=1)

        self.buttun_2 = Button(self.root, text = '분석1', width=25, command = self.chart_count_by_month)
        self.buttun_2.grid(row=6, column=1)
        self.buttun_3 = Button(self.root, text = '분석2', width=25, command = self.chart_count_by_month_rate)
        self.buttun_3.grid(row=7, column=1)
        self.buttun_4 = Button(self.root, text = '분석3', width=25, command = self.chart_pie)
        self.buttun_4.grid(row=8, column=1)
        self.buttun_5 = Button(self.root, text = '분석4', width=25, command = self.chart_count_by_weekdays)
        self.buttun_5.grid(row=9, column=1)
        self.buttun_6 = Button(self.root, text = '분석5', width=25, command = self.chart_count_by_weekdays_by_user)
        self.buttun_6.grid(row=10, column=1)

        self.root.mainloop()
    
    def open_file(self):
        file_root = self.file_root.get()
        try:
            f = open(file_root, 'r', encoding='utf-8-sig')
            self.raw_text = f.readlines()
            self.label_2.configure(text=file_root+'을 불러왔습니다.')
            self.is_open_text_file = True
        except:
            messagebox.showinfo('Error', '파일을 열 수 없습니다.')

    def analysis(self):
        if self.is_open_text_file == False:
            messagebox.showinfo('Error', '먼저 파일을 열어주세요.')
        else:
            self.kakao = KakaoAnal(self.raw_text)

    def chart_count_by_month(self):
        return self.kakao.chart_count_by_month()

    def chart_count_by_month_rate(self):
        return self.kakao.chart_count_by_month_rate()

    def chart_pie(self):
        return self.kakao.chart_pie()

    def chart_count_by_weekdays(self):
        return self.kakao.chart_count_by_weekdays()

    def chart_count_by_weekdays_by_user(self):
        return self.kakao.chart_count_by_weekdays_by_user()