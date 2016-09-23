import sys, os

spam = {}
ham = {}
prob_spam = {}
prob_ham = {}
distinct = {}

# read the files and split it into tokens
# call the required functions from the main function
def main(args):
    spam_files = 0
    ham_files = 0

    for subdir, dirs, files in os.walk(args[0]):
        for file in files:
            if (file.endswith('.txt')):
                words = []
                with open(os.path.join(subdir, file), "r", encoding="latin1") as infile:
                    words = infile.read().split()
                infile.close()
                if file.__contains__('ham'):
                    ham_files += 1
                    for datas in words:
                        data = datas.rstrip()
                        if data in ham:
                            ham[data] = ham.get(data) + 1
                        else:
                            ham[data] = 1
                        if data not in distinct:
                            distinct[data] = 1
                else:
                    spam_files += 1
                    for data in words:
                        if data in spam:
                            spam[data] = spam.get(data) + 1
                        else:
                            spam[data] = 1
                        if data not in distinct:
                            distinct[data] = 1

    return


# Calculate the probability of each word
def findProbability():
    spam_count = 0
    ham_count = 0

    #calculate total number of words in each class
    for data in spam:
        spam_count += spam.get(data)
    for data in ham:
        ham_count += ham.get(data)

    return {'spam':spam_count,'ham':ham_count}


def writeOutput(spam_count,ham_count):
    with open('nbmodel.txt', 'w', encoding="latin1") as out:
        total =(len(spam) + len(ham))
        out.write("Spam,Total probability," + (str(spam_count)) + "\n")
        out.write("Ham,Total probability," + (str(ham_count)) + "\n")
        out.write("Unique,words," + str(len(distinct)) + "\n")
        out.write("Total,vocabulary," + str(total) + "\n")
        for data in spam:
            out.write("Spam," + data + "," + str(spam[data]) + "\n")
        for data in ham:
            out.write("Ham," + data + "," + str(ham[data]) + "\n")
    out.close()
    return


if __name__ == "__main__":
    if len(sys.argv)!=2:
        print('Usage: python nblearn.py <path>')
        sys.exit(1)

    main(sys.argv[1:])
    ans = findProbability()
    writeOutput(ans['spam'],ans['ham'])
