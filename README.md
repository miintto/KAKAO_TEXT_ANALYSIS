# KAKAO TEXT ANALYSIS - 카카오톡 대화 분석

## 1. 개요
카카오톡 대화 내용을 입력받아 각 유저마다 요일별, 시간별, 월별 대화 횟수 및 빈도를 차트로 출력하는 python3 패키지 입니다.  
대화 내용이 담겨 있는 텍스트파일이 필요하며, 모바일 버전과 PC버전 어느것을 사용해도 무방합니다.

* 다음 라이브러리 설치가 요구됩니다.
~~~
pip install pandas #dataframe 가공 및 편집
pip install plotnine #그래프 생성
apt-get install python-tk #그래픽 출력
~~~
  pandas : <https://pandas.pydata.org>  
  plotnine : <https://plotnine.readthedocs.io/en/stable/>  
  tkinter : <https://tkdocs.com/index.html>

## 2. 예제
### 2.1 패키지 및 텍스트 파일 불러오기
먼저 메인 프로그램을 실행합니다.
~~~
python3 main.py
...
카카오톡 텍스트 파일의 경로를 입력해주세요 
 : 
~~~
위와 같은 창이 뜨면 카카오톡 대화 내용이 담긴 텍스트 파일의 경로를 입력합니다.  
ex) /home/minjae/다운로드/KakaoTalkChats(3).txt 

~~~ 
[시작할 날짜를 입력해주십시오. (ex. 2018-01-01)]  
~~~
그 후 분석을 시작할 날짜를 입력합니다.


### 2.2 차트 출력
* 월별 이용자 채팅
~~~python
kakao.chart_count_by_month()
~~~
<img src="./img/kakao_text_analysis_img_1.png">

* 월별 이용자 점유율
~~~python
kakao.chart_count_by_month_rate()
~~~
<img src="./img/kakao_text_analysis_img_2.png">

* 전체기간 이용자 점유율
~~~python
kakao.chart_pie()
~~~
<img src="./img/kakao_text_analysis_img_3.png">

* 요일 시간별 채팅
~~~python
kakao.chart_count_by_weekdays()
~~~
<img src="./img/kakao_text_analysis_img_4.png">

* 해당 이용자의 요일 시간별 채팅
~~~python
kakao.chart_count_by_weekdays_by_user()
~~~
<img src="./img/kakao_text_analysis_img_5.png">
