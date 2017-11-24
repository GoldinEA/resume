# usr/bin/python3
from sys import argv
from urllib.request import urlopen
from lxml.html import fromstring
import shutil
import re

# для того чтобы корректно произвести поиск, необходимо ввести имя исполнителя (cостоящее из одного слова)
#  и название трека
# например "madonna girl gone wild" - без кавычек

# название песни - по этому имени будем искать с помощью библиотеки re
SONG_NAME = argv[1::]



# получаем запрос из терминала и выводим URL для поиска
def get_url_search(arguments):
    search_data = '+'.join(arguments[1::])
    url = 'https://search.azlyrics.com/search.php?q='
    return '{0}{1}'.format(url, search_data)


# адрес поиска
url_search = get_url_search(argv)


# находим список ссылок и текст к ним в виде dict()
def parsing_data_links():
    url = urlopen(url_search)
    data_html = url.read().decode('utf-8')
    str_html = fromstring(data_html)
    # текст по которому будет произведен поиск с помошью SONG NAME
    texts = list()
    urls = list()
    # для удобства соединим переменные texts и urls в dict
    data_parse_song = dict()
    #Первый этап поиска - ищем ссылки
    for item in str_html.iter('a'):
        if item.text is None:
            urls.append(item.get("href"))
    #Второй этап поиска - ищем текст
    try:
        for i in range(100):
            text1 = str_html.cssselect('td.text-left')[i]
            texts.append(text1.text_content())
    except IndexError:
#записываем все найденное нами в словарь data_parse_song
        for txts, ur in zip(texts, urls[1:]):
            data_parse_song[txts] = ur
        return data_parse_song


# все ссылки из результатов поиска
links_list = parsing_data_links()


#ищем ссылку
def search_true_link(links):
    #число элементов поиска
    len_song_part = len(SONG_NAME)
    #число совпадений в тексте (который идет к ссылкам)
    sont_part_true = list()
    for key, val in links.items():
        for song_part in SONG_NAME:
            match = re.search(song_part, str(key))
            if match is not None:
                sont_part_true.append(1)
        #Если число совпадений в найденном тексте равно числу элементов поиска, то эта сссылка нам и нужна.
        if len(sont_part_true) == len_song_part:
            return val

#достаем ссылку с помощью search_true_link
true_song_link = search_true_link(links_list)

#фунцкия позволяет вытащить текст песни
def parsing_song_text(song_url):
    url = urlopen(song_url)
    data_html = url.read().decode('utf-8')
    str_html = fromstring(data_html)
    texts = list()
    try:
        for i in range(100):
            text1 = str_html.cssselect('div:nth-child(8)')[i]
            texts.append(text1.text_content())
    except IndexError:
        #для более удобного представления превращаем текст в список (делим по строкам)
        return str(texts).split(r'\n')

#список состоящий из строк песни
song_text = parsing_song_text(true_song_link)

#Записываем строки песни в файл и выводим в терминал
def rec_song_in_file(text):
    file = open('{}.txt'.format(' '.join(SONG_NAME)), 'w')
    # c помощью функции shutil возвращаем размер окна терминала (для красивого вывода текста)
    option = shutil.get_terminal_size().columns
    #посредством цикла выводим на экран и записываем файл построчно
    for index in song_text[2:len(text) - 1:]:
        # В некоторых случаях в строках остаются символы "\r" поэтому дополнительно фильтруем их
        index_clear = re.sub(r'\\r', u'', index)
        # выводим строку песни в терминале (командной строке)
        print(index_clear.center(option))
        # записываем строку песни в файл
        file.write(index_clear + '\n')


rec_song_in_file(song_text)
