# encoding: utf-8
import codecs
import jieba.posseg as pseg


word_count = {}
word_lc = {}
ste_lc = {}


def delete_guillement():
    input_fp = codecs.open('test_res_movie33.data', 'rU', 'utf-8')
    guillement_fp = codecs.open('movie/guillement.data', 'wU', 'utf-8')
    no_guillement_fp = codecs.open('movie/raw_no_guillement.data', 'wU', 'utf-8')
    lt = []
    flag = False
    for line in input_fp.readlines():
        lt.append(line)
        print line[0]
        if line[0] == u'《':
            flag = True
        if len(line) == 1:
            if flag:
                for l in lt:
                    guillement_fp.write(l)
            else:
                for l in lt:
                    no_guillement_fp.write(l)
            lt = []
            flag = False
    input_fp.close()
    guillement_fp.close()


def pre_segment(ste):
    texts = ste.split('\001')
    if len(texts) > 2:
        return texts[0], texts[2]
    else:
        return "", ""


def movie_segment(filename, out_filename, is_train):
    fp = codecs.open(filename, 'rU', 'utf-8')
    fp_out = codecs.open(out_filename, 'wU', 'utf-8')
    for line in fp.readlines():
        index, text = pre_segment(line.strip())
        fp_out.write('#' + '@' + '#' + index + '\n')
        words = pseg.cut(text)
        if is_train:
            for word in words:
                if word.word == ' ':
                    fp_out.write('@#@' + '\t' + word.flag + '\t' + 'O' + '\n')
                else:
                    fp_out.write(word.word+'\t'+word.flag+'\t'+'O'+'\n')
            fp_out.write('\n')
        else:
            for word in words:
                if word.word == ' ':
                    fp_out.write('@#@' + '\t' + word.flag + '\n')
                else:
                    fp_out.write(word.word + '\t' + word.flag + '\n')
            fp_out.write('\n')


def search_ne(words_list):
    ne_list = []
    flag, i = 0, 0
    while i < len(words_list):
        if words_list[i][2] == 'NM':
            ne_list.append(words_list[i][0])
        elif words_list[i][2] == 'B_NM':
            word = ''
            while i < len(words_list) and words_list[i][2] != 'O':
                word += words_list[i][0]
                i += 1
            if words_list[i-1][2] == 'E_NM':
                ne_list.append(word)
            else:
                flag = 1
        else:
            flag = 1
        i += 1
    return ne_list, flag


def calculate_lc(py1, py2, parameter):
    lc = 1 - (parameter * py1 + (1 - parameter) * (py1 - py2))
    return lc


def select_ne(k):
    global word_lc
    # lenght =len(word_lc)
    max_kne = []
    if word_lc:
        wlc = sorted(word_lc.items(), key=lambda d: d[1], reverse=True)
        i = 0
        # print wlc
        for w in wlc:
            max_kne.append(w[0])
            i += 1
            if i >= k:
                break
    return max_kne


def select_sentence(max_kne, k):
    global ste_lc
    max_ksentence = set()
    for ne in max_kne:
        dt = sorted(ste_lc[ne].items(), key=lambda d1: d1[1], reverse=True)
        i = 0
        print ne, ' ', ste_lc[ne]
        for d in dt:
            i += 1
            max_ksentence.add(d[0])
            if i >= k:
                break
    print len(max_kne), ' '.join(max_kne).encode('utf-8')
    print len(max_ksentence)
    return max_ksentence


def sentence(ls_sentence, res_fp, ne_fp):
    res_fp.seek(0)
    j = 0
    flag = False
    for line in res_fp.readlines():
        list_line = line.strip().split('\t')
        if len(list_line) < len(line.strip().split(' ')):
            list_line = line.strip().split(' ')
        # print len(ls_sentence), ' ', ls_sentence
        if len(list_line) == 1 and len(list_line[0]) > 0 and int(list_line[0][3:]) in ls_sentence:
            j += 1
            flag = True
        elif len(list_line) == 1 and list_line[0] == '':
            if flag:
                ne_fp.write('\n')
            if j >= len(ls_sentence):
                break
            flag = False
        if flag:
            if len(list_line) == 1 or \
                    (list_line[1] != '0' and list_line[1] != '1'):
                ne_fp.write(line)


def modeling(res_fp, parameter, ne_fp, max_k_ne, max_k_sentence):
    py1 = 0.0
    py2 = 0.0
    sentence_number = 0
    flag = -1
    words_list = []
    global word_count
    global word_lc
    global ste_lc
    for line in res_fp.readlines():
        list_line = line.strip().split('\t')
        if len(list_line) < len(line.strip().split(' ')):
            list_line = line.strip().split(' ')
        if len(list_line) == 1 and len(list_line[0]) > 0:
            # print list_line, len(list_line)
            sentence_number = int(line[3:])
        elif len(list_line) >= 3:
            # print list_line, len(list_line)
            if list_line[1] == '0':
                py1 = float(list_line[2])
                flag = 0
            elif list_line[1] == '1':
                py2 = float(list_line[2])
                flag = 1
            elif flag == 0:
                word_list = []
                for l in list_line:
                    word_list.append(l)
                words_list.append(word_list)
        elif len(list_line) == 1 and len(list_line[0]) == 0 and flag == 1:
            # print py1, words_list
            ne_list, flag = search_ne(words_list)
            words_list = []
            lc = calculate_lc(py1, py2, parameter)
            for ne in ne_list:
                if ne in word_count:
                    word_count[ne] += 1
                    word_lc[ne] += lc
                    ste_lc[ne][sentence_number] = lc
                else:
                    word_count[ne] = 1
                    word_lc[ne] = lc
                    ste_lc[ne] = {}
                    ste_lc[ne][sentence_number] = lc

    for key in word_count:
        word_lc[key] /= word_count[key]
    ls_sentence = select_sentence(select_ne(max_k_ne), max_k_sentence)
    # ls_sentence.sort()
    sentence(ls_sentence, res_fp, ne_fp)
    # ne_fp.write(str(sentence_number) + '\t' + str(py1) + '\t' + str(py2)
    #             + '\t' + '\t'.join(ne_list))


if __name__ == '__main__':
    delete_guillement()
    # rand_validate('re_model/res_raw_no_guillement.data', 're_model/res_part_raw_no_guillement.data', 3780, 3780, 300)
    # test_segment('movie/no_guillement.txt', 'movie/test_no_guillement.data')
    # res_fp1 = codecs.open('test_res_movie3.data', 'rU', 'utf-8')
    # ne_fp1 = codecs.open('trm3.data', 'wU', 'utf-8')
    # modeling(res_fp1, 0.8, ne_fp1)
# fp = codecs.open('seg_train.txt', 'rU', 'utf-8')
# fp_out = codecs.open('train.data', 'wU', 'utf-8')
# i = 1
# fp_out.write('#' + '@' + '#' + str(i) + '\n')
# for line in fp.readlines():
#     words = line.strip().split(' ')
#     print words,i
#     if len(words)==3:
#         fp_out.write(words[0]+'\t'+words[1]+'\t'+words[2]+'\n')
#     elif len(words)==2:
#         fp_out.write('@#@' + '\t' + words[0] + '\t' + words[1] + '\n')
#     else:
#         i += 1
#         fp_out.write('\n')
#         fp_out.write('#' + '@' + '#' + str(i) + '\n')
# fp_out.close()
# test_segment('movie_question.txt', 'test.data')
