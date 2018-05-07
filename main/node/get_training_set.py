import numpy
import textblob
import os
import re

pos = []
neg = []
for filename in os.listdir('txt_sentoken/pos'):
    fp = open('txt_sentoken/pos/'+filename, 'r')
    doc = fp.read()
    doc = re.sub(r"\n", " ", doc) + '\n'
    pos.append(doc)
    fp.close()
print('finish reading pos data')
for filename in os.listdir('txt_sentoken/neg'):
    fp = open('txt_sentoken/neg/'+filename, 'r')
    doc = fp.read()
    doc = re.sub(r"\n", " ", doc) + '\n'
    neg.append(doc)
    fp.close()
print('finish reading neg data')
fp_pos = open('pos.txt', 'w')
for doc in pos:
    fp_pos.write(doc)
fp_pos.close()
print('finish writing pos data')
fp_neg = open('neg.txt','w')
for doc in neg:
    fp_neg.write(doc)
fp_neg.close()
print('finish writing neg data')
print('done')
