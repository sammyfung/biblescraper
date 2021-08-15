import csv, jieba

with open('bible-scripture.csv', newline='') as csvfile:
    column = 4
    rows = csv.reader(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in rows:
        print("I: %s" % row[column])
        # Use big dictionary file instead of default dictionary.
        #jieba.set_dictionary('dict.txt.big')
        # Load additional user dictionary
        jieba.load_userdict('bible_dict.txt')
        # default mode
        #print('O: %s' % '|'.join(jieba.cut(row[column], cut_all=False, HMM=True)))
        #print('O: %s' % '|'.join(jieba.cut(row[column])))

        # Search Engine mode
        print('O: %s' % '|'.join(jieba.cut_for_search(row[column])))
