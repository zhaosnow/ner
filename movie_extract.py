# encoding:utf-8
import sys
import codecs


movie_set = set()


def main(data=None, out=None):
    if data is None:
        stdin = codecs.getreader("utf-8")(sys.stdin)
    else:
        stdin = open(data, "rU")
    if out is None:
        stdout = codecs.getwriter('utf-8')(sys.stdout)
    else:
        stdout = codecs.open(out, "wU", 'utf-8')

    for obj in stdin:
        text = obj.strip().split('\001')
        if len(text) > 2:
            for key in movie_set:
                if text[1].encode('utf-8').find(key) != -1:
                    stdout.write(u"{0}\n".format(u"\001".join([text[0], key.decode("utf-8"), text[1]])))
if __name__ == '__main__':
    fp = codecs.open('result.txt', 'rU', 'utf-8')
    for line in fp.readlines():
        movie_set.add(line.strip().encode('utf-8'))
    main()