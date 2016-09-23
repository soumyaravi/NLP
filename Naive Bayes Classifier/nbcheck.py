import os

def main(file_name):
    lines = []

    with open(file_name,'r',encoding="latin1") as infile:
        lines = infile.readlines()
    infile.close()

    spam = 0
    ham = 0
    inspam = 0
    inham = 0
    for data in lines:
        words = data.split()
        if words[0] == "Spam" and words[1].__contains__("spam"):
            spam +=1
        elif words[0] == "Spam" and words[1].__contains__("ham"):
            inspam +=1
        elif words[0] == "Ham" and words[1].__contains__("ham"):
            ham +=1
        else:
            inham +=1

    precision_spam = float(spam)/float(spam+inspam)
    precision_ham = float(ham)/float(ham+inham)

    recall_spam = float(spam)/3675
    recall_ham = float(ham)/1500

    f1_spam = float(2*precision_spam*recall_spam) / float(precision_spam+recall_spam)
    f1_ham = float(2*precision_ham*recall_ham) / float(precision_ham+recall_ham)

    avg = ((f1_ham*1500) + (f1_spam*3675))/float(1500+3675)
    task = {'nboutput.txt':'1','nboutput2.txt':'2','nboutput3.txt':'3'}

    print('For task ' + task.get(file_name))
    print('File\tPrecision\tRecall\tF1')
    print('Spam\t%.2f\t%.2f\t%.2f'%(precision_spam,recall_spam,f1_spam))
    print('Ham\t%.2f\t%.2f\t%.2f'%(precision_ham,recall_ham,f1_ham))
    print('Weighted Avg %.2f' %(avg))
    print('')

    return

if __name__ == '__main__':
    files = ['nboutput.txt','nboutput2.txt','nboutput3.txt']
    for data in files:
        if os.path.exists(data):
            main(data)