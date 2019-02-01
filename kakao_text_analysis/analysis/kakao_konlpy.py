# -*- coding: utf-8 -*-

import os
from konlpy.tag import Okt
from wordcloud import WordCloud

### matplotlib에 한글 폰트 설정
fpath = os.path.dirname(__file__)+'/fonts/NanumGothicBold.ttf'


class KakaoKoNLPy:
    def __init__(self, dat_chat):
        self.dat_chat = dat_chat

    def word_cloud(self, user_name):
        word = ''
        for _, name, chat in self.dat_chat:
            if name == user_name:
                for w in chat.split():
                    word += w
                    word += ' '

        word = word.replace('사진', '')
        word = word.replace('이모티콘', '')
        word = word.replace('음성메시지', '')

        okt = Okt()
        noun_word = okt.nouns(word)

        word_dict = dict()
        for w in set(noun_word):
            if len(w)>1:
                word_dict[w] = word.count(w)

        wordcloud = WordCloud(font_path = fpath, width = 800, height = 800, background_color="white")
        wordcloud = wordcloud.generate_from_frequencies(word_dict)
        array = wordcloud.to_array()
        return array
