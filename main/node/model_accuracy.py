from textblob import TextBlob
import csv

def check_accuracy(test_set):
    prediction = []
    label = [1]*1000 + [0]*1000
    for doc in test_set:
        b = TextBlob(doc)
        if b.polarity >= 0:
            prediction.append(1)
        else:
            prediction.append(0)
    total = 0
    count = 0
    for i in range(2000):
        if prediction[i] == label[i]:
            count += 1
        total += 1
    return count / total

pos = []
neg = []
fp_pos = open('pos.txt')
for line in fp_pos:
    pos.append(line)
fp_pos.close()

fp_neg = open('neg.txt')
for line in fp_neg:
    neg.append(line)
fp_neg.close()

test_set = pos + neg
accuracy = check_accuracy(test_set)
    
print('the accuracy of sentiment model using long text is '+ str(accuracy))

sentiment140 = open('testdata.manual.2009.06.14.csv')
data = csv.reader(sentiment140)
label = []
test_set = []
for row in data:
    label.append(row[0])
    test_set.append(row[-1])

prediction = []
for i in test_set:
    b = TextBlob(i)
    if b.polarity <0:
        prediction.append(0)
    elif b.polarity == 0:
        prediction.append(2)
    else:
        prediction.append(4)

count = 0
total = 0
for i in range(len(prediction)):
    if prediction[i] == int(label[i]):
        count += 1
    total += 1

result = count / total
print('the accuracy of sentiment model using tweets is '+ str(result))
