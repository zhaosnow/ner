# encoding: utf-8
import sys
import codecs
import re
import random

movie_set = set()


def deal():
    pass


def g_random(num, length):
    rand = random.sample(range(0, length), num)
    rand.sort()
    return rand


def extract(raw_fp, train_fp, num):
    readlines = raw_fp.readlines()
    rand = g_random(num, len(readlines))
    i = 0
    j = 0
    for ln in readlines:
        if j >= num:
            break
        if i == rand[j]:
            train_fp.write(ln.decode('utf-8')+'\n')
            j += 1
        i += 1


def add_row_number(filename, output_filename):
    in_fp = codecs.open(filename, 'rU', 'utf-8')
    out_fp = codecs.open(output_filename, 'wU', 'utf-8')
    i = 0
    for ln in in_fp.readlines():
        out_fp.write(str(i) + '\001' + ln)
        i += 1
    out_fp.close()


def movie_rule(key, ln):
    ticket_pattern = re.compile(unicode('(' + key + '|《' + key + '》).*?票房', 'utf-8'), re.S)
    how_pattern = re.compile(unicode('如何.*?' + key + '.*?电影', 'utf-8'), re.S)
    class_pattern = re.compile(unicode(key + '.*?是.*?的?电影', 'utf-8'), re.S)
    look_pattern = re.compile(unicode('((点映|上映)|观影).*?(' + key + '|《' + key + '》)', 'utf-8'), re.S)
    look_pattern1 = re.compile(unicode('(' + key + '|《' + key + '》).*?((点映|上映)|观影)', 'utf-8'), re.S)
    movie_pattern = re.compile(unicode('(' + key + '|《' + key + '》).*?的?((片子|影片)|(烂片|好片))', 'utf-8'), re.S)
    lines_pattern = re.compile(unicode('(' + key + '|《' + key + '》).*?台词', 'utf-8'), re.S)
    role_pattern = re.compile(unicode('(' + key + '|《' + key + '》).*?[男女]主角', 'utf-8'), re.S)
    role_pattern1 = re.compile(unicode('(' + key + '|《' + key + '》).*?([中里]|这[一个]).*?(主角|角色)', 'utf-8'), re.S)
    end_pattern = re.compile(unicode('(' + key + '|《' + key + '》).*?的?结尾', 'utf-8'), re.S)
    guillement_pattern = re.compile(unicode('电影.*?《' + key + '》.*?', 'utf-8'), re.S)
    guillement_pattern1 = re.compile(unicode('《' + key + '》.*?电影', 'utf-8'), re.S)
    temp_pattern = re.compile(unicode('《' + key + '》', 'utf-8'), re.S)
    guillement_pattern2 = re.compile(unicode('电影.*?' + key + '.*?', 'utf-8'), re.S)
    guillement_pattern3 = re.compile(unicode(key + '.*?电影', 'utf-8'), re.S)
    if len(re.findall(guillement_pattern, unicode(ln, 'utf-8'))) > 0 or len(
            re.findall(guillement_pattern1, unicode(ln, 'utf-8'))) > 0 or len(re.findall(temp_pattern,
                                                                                         unicode(ln, 'utf-8'))) > 0:
        return True
    elif len(re.findall(temp_pattern, unicode(ln, 'utf-8'))) == 0 and (
            len(re.findall(guillement_pattern2, unicode(ln, 'utf-8'))) > 0 or len(
                re.findall(guillement_pattern3, unicode(ln, 'utf-8'))) > 0):
        return True
    elif len(re.findall(ticket_pattern, unicode(ln, 'utf-8'))) > 0:
        return True
    elif len(re.findall(how_pattern, unicode(ln, 'utf-8'))) > 0:
        return True
    elif len(re.findall(class_pattern, unicode(ln, 'utf-8'))) > 0:
        return True
    elif len(re.findall(look_pattern, unicode(ln, 'utf-8'))) > 0 or len(
            re.findall(look_pattern1, unicode(ln, 'utf-8'))) > 0:
        return True
    elif len(re.findall(movie_pattern, unicode(ln, 'utf-8'))) > 0:
        return True
    elif len(re.findall(lines_pattern, unicode(ln, 'utf-8'))) > 0:
        return True
    elif len(re.findall(role_pattern, unicode(ln, 'utf-8'))) > 0 or len(
            re.findall(role_pattern1, unicode(ln, 'utf-8'))) > 0:
        return True
    elif len(re.findall(end_pattern, unicode(ln, 'utf-8'))) > 0:
        return True
    else:
        return False


def movie_filter(data=None, out=None):
    if data is None:
        stdin = codecs.getreader("utf-8")(sys.stdin)
    else:
        stdin = codecs.open(data, "rU", "utf-8")
    if out is None:
        stdout = codecs.getwriter('utf-8')(sys.stdout)
    else:
        stdout = codecs.open(out, "wU", 'utf-8')
    if data is not None:
        # error_stdout = codecs.open(error_out, "wU", "utf-8")
        for ln in stdin.readlines():
            # for key in movie_set:
            ln = ln.strip().encode('utf-8')
            pos = ln.find('\001')
            index = ln[0: pos]
            ln = ln[pos+1:]
            pos = ln.find('\001')
            key = ln[0: pos]
            ln = ln[pos+1:]
            # print key+'asd', unicode('如何.*?'+key+'.*?电影', 'utf-8')
            if movie_rule(key, ln):
                stdout.write(u"{0}\n".format(u"\001".join([index.decode("utf-8"), key.decode("utf-8"),
                                                           ln.decode("utf-8")])))
    else:
        for obj in stdin:
            text = obj.strip().split('\001')
            if len(text) > 2:
                for key in movie_set:
                    if text[1].encode('utf-8').find(key) != -1:
                        stdout.write(u"{0}\n".format(u"\001".join([text[0].decode("utf-8"), key.decode("utf-8"),
                                                                   text[1]])))


if __name__ == '__main__':
    fp = codecs.open('re_model/some_sample/res.txt', 'rU', 'utf-8')
    for line in fp.readlines():
        movie_set.add(line.strip().encode('utf-8'))
    movie_filter("re_model/some_sample/some.txt", "re_model/some_sample/test.data")
    # pre_train_fp = codecs.open('pre_train.txt', 'wU', 'utf-8')
    # train_fp = codecs.open('train.txt', 'wU', 'utf-8')
    # extract('re', pre_train_fp, train_fp)
    # train_fp.close()
    # pre_train_fp.close()
    # add_row_number('re_model/total/movie_question.txt', 're_model/total/total.data')


#     # how_pattern = re.compile('.*?如何.*?一一.*?这.*?电影', re.S)
#     # good_pattern = re.compile('.*?一一.*?是.*?的?电影', re.S)
#     # # find(key) and find('点映' or '上映'or 观影)
#     # # find(key) and find('片子','烂片','好片','影片')
#     # lines_pattern = re.compile('.*?一一.*?台词', re.S)
#     # roles_pattern1 = re.compile('.*?他是龙.*?[中里].*?主角', re.S)
#     # roles_pattern2 = re.compile('.*?他是龙.*?[男女].*?主角', re.S)
#     # roles_pattern3 = re.compile('.*?东邪西毒(.*?[中里].*?|.*?这[一个])角色', re.S)
#     # res = '龙猫 有哪些和《龙猫》风格类似的快乐、纯真、美好、充满想象力的电影或动画？'
#     # pos = res.find(' ')
#     # keys = res[0: pos]
#     # res = res[pos+1: ]
#     # end_pattern = re.compile(unicode('('+ keys +'|《'+ keys +'》).*?的?((片子|影片)|(烂片|好片))', 'utf-8'), re.S)
#     # items = re.findall(end_pattern, unicode(res, 'utf-8'))
#     # print res,len(items), items[0]
