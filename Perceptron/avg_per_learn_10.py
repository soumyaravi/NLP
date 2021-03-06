import sys, os
import collections
import random


def initializeWeights(filelist, wd, ud):
    keys = filelist.keys()

    for key in keys:
        words = filelist[key].split()
        for x in words:
            x = x.lower()
            wd[x] = 0
            ud[x] = 0
    return


def main(args):
    spam_files = 0
    ham_files = 0
    wd = dict()  # weight of training words
    ud = dict()  # averaged weight of training words
    c = 1  # initialize counter
    beta = 0  # initialize average weighted bias
    b = 0  # initial bias

    filelist = {}
    for subdir, dirs, files in os.walk(args[0]):
        for file in files:
            if (file.endswith('.txt')):
                with open(os.path.join(subdir, file), "r", encoding="latin1") as infile:
                    value = ""
                    for line in infile:
                        value = (line.strip()) + " "
                    filelist[os.path.join(subdir, file)] = value
                infile.close()
                if "spam" in os.path.join(subdir, file):
                    spam_files += 1
                else:
                    ham_files += 1
    initializeWeights(filelist, wd, ud)
    spam_files = int(spam_files * 0.1)
    ham_files = int(ham_files * 0.1)
    print(spam_files)
    print(ham_files)
    scount = 0
    hcount = 0
    keys = filelist.keys()
    for num in range(0, 30):
        for key in keys:
            if key.__contains__('spam') and scount <= spam_files:
                y = 1
                scount += 1
            elif key.__contains__('ham') and hcount <= ham_files:
                y = -1
                hcount += 1
            else:
                continue
            words = filelist[key].split()
            xd = collections.Counter(words)
            total = 0
            for x in xd:
                x = x.lower()
                alpha = wd[x] * xd[x]
                total += alpha
            total += b
            total *= y
            if total <= 0:  # wrong prediction

                for x in xd:
                    x = x.lower()
                    wd[x] += (y * xd[x])
                    ud[x] += (y * c * xd[x])
                b += y
                beta += (y * c)
            c += 1
    for x in ud:
        x = x.lower()
        ud[x] = wd[x] - float(ud[x] / c)
    beta = b - float(beta / c)
    return {'weights': wd, 'avg': ud, 'beta': beta}


def writeOutput(wd, bias, ud):
    with open('per_model.txt', 'w', encoding="latin1") as out:
        out.write("AveragePerceptronBias," + str(bias) + "\n")
        out.write("Length," + str(len(wd)) + "\n")
        print("Length," + str(len(wd)) + "\n")
        for x in wd:
            out.write(x + "," + str(wd[x]) + "\n")
        for x in ud:
            out.write(x + "," + str(ud[x]) + "\n")
    out.close()
    pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python avg_per_learn.py <input_path>')
        sys.exit(1)

    ans = main(sys.argv[1:])
    wd = ans['weights']
    ud = ans['avg']
    writeOutput(wd, ans['beta'], ud)
