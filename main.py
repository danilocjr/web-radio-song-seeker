import requests
from html.parser import HTMLParser
from datetime import datetime
import json

td_founded = False
b_founded = False
a_founded = False
music_founded = False
radio_founded = False

last_music = ""
last_radio = ""


class Music:
    def __init__(self, name, radio_url):
        self.name = name
        self.radio_url = radio_url
        self.datetime = datetime.now().strftime("%Y/%m/%d %H:%M")


class MusicParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global a_founded, b_founded, td_founded
        if tag == 'td':
            td_founded = True
        if tag == 'b':
            b_founded = True
        if tag == 'a':
            a_founded = True

    def handle_endtag(self, tag):
        global a_founded, b_founded, td_founded
        if tag == 'b':
            b_founded = False
        if tag == 'a':
            a_founded = False
        if tag == 'td':
            td_founded = False

    def handle_data(self, data):
        global a_founded, b_founded, td_founded, music_founded, last_music, music_list

        if len(data) > 5:
            if td_founded and b_founded:
                # print("Music: ", data)
                last_music = data
                music_founded = True

            if td_founded and a_founded and music_founded:
                # print("Radio: ", data)
                music = Music(name=last_music, radio_url=data)
                music_list.append(music)
                music_founded = False
                b_founded = False
                a_founded = False
                td_founded = False


music_list = []

music_list_parser = MusicParser()

styles = ['rock', 'classic rock', 'blues']
page_max = 100

for style in styles:
    print(">>> Radio Genre:", style)
    for page in range(1, page_max):
        print("* Page:", page)
        scrap_url = str.format('https://www.internet-radio.com/stations/{0}/page{1}', style, page)
        r = requests.get(scrap_url)
        if r.status_code == 200:
            music_list_parser.feed(r.text)
        else:
            pass

json_string = json.dumps([obj.__dict__ for obj in music_list])

text_file = open("result.json", "w")
text_file.write(json_string)
text_file.close()
