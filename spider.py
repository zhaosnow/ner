# encoding: utf-8;
import urllib
import urllib2
import re
import json
import codecs
import time


def get_movie_name(old_name):
    name = old_name.strip().split(' ')
    new_name = name[0]
    return new_name.strip()


def get_movie_alias(old_name):
    name = old_name.strip().split('/')
    return name


def douban_movie(name_fp, alias_fp):
    start_year = 1920
    sort_list = ['', 'S', 'R', 'O']
    base_url = 'https://movie.douban.com/tag/'
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/'
                      '23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    while start_year < 2017:
        for sl in sort_list:
            start = 0
            while start >= 0:
                url = base_url + str(start_year) + '?' + 'start=' + str(start) + '&type=' + sl
                request = urllib2.Request(url, headers=hdr)
                response = urllib2.urlopen(request)
                content = response.read().decode('utf-8')
                pattern = re.compile(u'<div class="pl2">\s.*?<a.*?>(.*?)<', re.S)
                pattern1 = re.compile(u'<div class="pl2">\s.*?<a.*?>.*?<span.*?>(.*?)</span>', re.S)
                items = re.findall(pattern, content)
                items1 = re.findall(pattern1, content)
                if len(items) == 0 and len(items1) == 0:
                    break
                for item in items:
                    name_fp.write(get_movie_name(item) + '\n')
                for item1 in items1:
                    lt = get_movie_alias(item1)
                    for l in lt:
                        l = l.strip()
                        if len(l) == 0:
                            continue
                        if l[-1] == ')':
                            j = len(l) - 1
                            while j >= 0:
                                if l[j] != '(':
                                    j -= 1
                                else:
                                    break
                            alias_fp.write(l[:j] + '\n')
                        else:
                            alias_fp.write(l + '\n')
                print str(start_year) + '-' + str(start)
                time.sleep(2)
                start += 20
        start_year += 1


def movie_name(filename, alias_filename):
    name_fp = codecs.open(filename, 'aU', 'utf-8')
    alias_fp = codecs.open(alias_filename, 'aU', 'utf-8')
    douban_movie(name_fp, alias_fp)
    name_fp.close()
    alias_fp.close()


def read_url(values, url):
    data = urllib.urlencode(values)
    geturl = url + '?' + data
    request = urllib2.Request(geturl)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    return content


def deal_movie250(fp):
    # top250 movie
    for i in range(10):
        try:
            values = {'start': i * 25, 'filter': ""}
            url = 'https://movie.douban.com/top250/'
            content = read_url(values, url)
            pattern = re.compile(
                '<div class="hd">.*?<a.*?<span class="title">(.*?)</span>.*?<span class="title">(.*?)</span>.*?</div>',
                re.S)
            items = re.findall(pattern, content)
            for item in items:
                fp.write(item[0]+"\n")
                # print item[0], item[1].replace("&nbsp;", "").replace("/", "")
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason


def hot_movie(fp):
    for i in range(15):
        try:
            sorts = ['recommend', 'time', 'rank']
            for s in sorts:
                values = {'type': 'movie', 'tag': '热门', 'sort': s, 'page_limit': '20', 'page_start': i*20}
                url = 'https://movie.douban.com/j/search_subjects'
                content = read_url(values, url)
                json_dict = json.loads(content)
                for lt in json_dict["subjects"]:
                    print type(lt["title"])
                    fp.write(lt["title"] + "\n")

        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason


def collect(filename):
    fp = codecs.open(filename, 'wU', 'utf-8')
    hot_movie(fp)
    fp.close()
