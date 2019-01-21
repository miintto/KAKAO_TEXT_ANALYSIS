from kakao_text_analysis import *


file_root = input('카카오톡 텍스트 파일의 경로를 입력해주세요 \n : ')

f = open(file_root, 'r', encoding = 'utf-8-sig')
Text = f.readlines()

kakao = KakaoAnal(Text)

print(kakao.chart_count_by_month())
print(kakao.chart_count_by_month_rate())
print(kakao.chart_pie())
print(kakao.chart_count_by_weekdays())
print(kakao.chart_count_by_weekdays_by_user())