from textblob import TextBlob

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
    
print('the accuracy of sentiment model is '+ str(accuracy))
