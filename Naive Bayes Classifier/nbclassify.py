import sys
import os
import math

spam = {}
ham = {}
output = {}


def main():
    with open("nbmodel.txt", "r", encoding="latin1") as infile:
        model = infile.readlines()
    infile.close()

    for data in model:
        words = data.split(",")
        if words[1] == "Total probability":
            if words[0] == "Spam":
                spam_count = float(words[2].strip())
            else:
                ham_count = float(words[2].strip())
        else:
            if words[2].strip()!='':
                val = words[2]
                if words[0] == "Spam":
                    spam[words[1]] = float(val)
                else:
                    ham[words[1]] = float(val)
        if words[0] == "Unique" and words[1] == "words":
            distinct = float(words[2])
        if words[0] == "Total" and words[1] == "vocabulary":
            total = float(words[2])
    return {'spam':spam_count,'ham':ham_count,'distinct':distinct,'total':total}


def writeOutput():
    with open('nboutput.txt','w',encoding="latin1") as out:
        for data in output:
            out.write(output[data] + " " + data + "\n")
    out.close()
    return


def classify(args,spam_count,ham_count,distinct,total):
    for subdir, dirs, files in os.walk(args[0]):
        for file in files:
            if (file.endswith('.txt')):
                with open(os.path.join(subdir, file), "r", encoding="latin1") as infile:
                    words = infile.read().split()
                infile.close()
                msgspam = 0
                msgham = 0
                for data in words:
                    if data in spam and data in ham:
                        msgspam += math.log(((spam.get(data))+1),math.e) - math.log((distinct + spam_count),math.e)
                        msgham += math.log(((ham.get(data)+1)),math.e) - math.log((distinct + ham_count),math.e)
                    elif data not in spam and data in ham:
                        msgspam += (math.log((1), math.e) - math.log((distinct + spam_count), math.e))
                        msgham += math.log(((ham.get(data) + 1)), math.e) - math.log((distinct + ham_count), math.e)
                    elif data not in ham and data in spam:
                        msgspam += math.log(((spam.get(data)) + 1), math.e) - math.log((distinct + spam_count), math.e)
                        msgham += (math.log(1, math.e) - math.log((distinct + ham_count), math.e))
                    else:
                        pass
                pspam = float(spam_count)/float(total)
                pham = float(ham_count)/float(total)
                spamprob = math.log(pspam,math.e) + msgspam
                hamprob = math.log(pham,math.e) + msgham

                if spamprob >= hamprob:
                    output[os.path.join(subdir, file)] = "Spam"
                else:
                    output[os.path.join(subdir, file)] = "Ham"
    return


if __name__ == "__main__":
    if len(sys.argv)!=2:
        print('Usage: python nbclassify.py <path>')
        sys.exit(1)

    ans = main()
    classify(sys.argv[1:],ans['spam'] , ans['ham'],ans['distinct'],ans['total'])
    writeOutput()
