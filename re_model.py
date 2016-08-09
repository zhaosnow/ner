# encoding: utf-8
import codecs
import random


def split_parameter(parameter, total_num):
    pt = int(parameter * total_num)
    rand = random.sample(range(0, total_num), pt)
    rand.sort()
    return rand


def search_ne(words_list, pos):
    ne_list = []
    flag, i = 0, 0
    while i < len(words_list):
        if words_list[i][pos] == 'NM':
            ne_list.append(words_list[i][0])
        elif words_list[i][pos] == 'B_NM':
            word = ''
            while i < len(words_list) and words_list[i][2] != 'O':
                word += words_list[i][0]
                i += 1
            if words_list[i-1][pos] == 'E_NM':
                ne_list.append(word)
            else:
                flag = 1
        else:
            flag = 1
        i += 1
    return ne_list, flag


def split_guillement(input_filename, filename1, filename2, parameter, flag):
    input_fp = codecs.open(input_filename, 'rU', 'utf-8')
    fp = codecs.open(filename1, 'wU', 'utf-8')
    fp1 = codecs.open(filename2, 'wU', 'utf-8')
    rd_lines = input_fp.readlines()
    total_num = len(rd_lines)
    print total_num
    rand = split_parameter(parameter, total_num)
    i = 0
    j = 0
    for line in rd_lines:
        if i == rand[j]:
            if flag:
                if line[0] != u'《' and line[0] != u'》':
                    fp1.write(line)
            else:
                fp1.write(line)
        else:
            fp.write(line)
        if len(line) == 1:
            if i == rand[j]:
                j += 1
            i += 1
    fp.close()
    fp1.close()


def calculate(filename):
    fp = codecs.open(filename, 'rU', 'utf-8')
    words = []
    c_correct, c_error, e_correct, e_error = 0, 0, 0, 0
    for line in fp.readlines():
        line_list = line.strip().split('\t')
        if len(line_list) == 1:
            if len(line_list[0]) == 0:
                true_ne, flag = search_ne(words, 2)
                predict_ne, flag1 = search_ne(words, 3)
                if len(true_ne) == 0 and len(predict_ne) == 0:
                    e_error += 1
                elif len(true_ne) > 0 and len(predict_ne) == 0:
                    c_error += len(true_ne)
                elif len(true_ne) == 0 and len(predict_ne) > 0:
                    e_correct += len(predict_ne)
                    print '\n'.join(predict_ne)
                else:
                    for ne in predict_ne:
                        if ne in true_ne:
                            c_correct += 1
                        else:
                            e_correct += 1
                            print ne
                    for ne in true_ne:
                        if ne not in predict_ne:
                            c_error += 1
                words = []
        else:
            words.append(line_list)
    return c_correct, c_error, e_correct, e_error


def rand_validate(input_filename, output_filename, total_len, num):
    input_fp = codecs.open(input_filename, 'rU', 'utf-8')
    output_fp = codecs.open(output_filename, 'wU', 'utf-8')
    j = 0
    k = 0
    rand = random.sample(range(0, total_len), num)
    rand.sort()
    for line in input_fp.readlines():
        print str(j)+' '+str(k)
        if k == num:
            break
        if j == rand[k]:
            output_fp.write(line)
        if len(line) == 1:
            if j == rand[k]:
                k += 1
            j += 1
    output_fp.close()

if __name__ == '__main__':
    # split_guillement('re_model/raw_no_guillement.data', 're_model/train_no_guillement.data', 're_model/predict_no_
    # guillement.data', 0.3, False)
    # rand_validate('re_model/res_raw_no_guillement.data', 're_model/res_part_raw_no_guillement.data', 3787, 300)
    c_correct, c_error, e_correct, e_error = calculate('optimalize_model/res_test_test11.data')
    print c_correct, c_error, e_correct, e_error