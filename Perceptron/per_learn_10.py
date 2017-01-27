import sys, os
import collections
import random


def main(args):
    spam_files = 0
    ham_files = 0
    wd = {}  # weight of training words
    b = 0  # initial bias
    filelist = {}
    for subdir, dirs, files in os.walk(args[0]):
        for file in files:
            if (file.endswith('.txt')):
                with open(os.path.join(subdir, file), "r", encoding="latin1") as infile:
                    value = ""
                    for line in infile:
                        value=(line.strip())+" "
                    filelist[os.path.join(subdir, file)] = value
                    if "spam" in os.path.join(subdir, file):
                        spam_files +=1
                    else:
                        ham_files+=1
                infile.close()

    spam_files = int(spam_files*0.1)
    ham_files = int(ham_files * 0.1)
    scount = 0
    hcount = 0
    keys = filelist.keys()
    for num in range(0,20):
        for key in keys:
            if key.__contains__('spam') and scount<=spam_files:
                y = 1
                scount+=1
            elif key.__contains__('ham') and hcount<=ham_files:
                y = -1
                hcount+=1
            else:
                continue
            words = filelist[key].split()
            xd = collections.Counter(words)
            total = 0
            for x in xd:
                if x in wd:
                    alpha= wd[x] * xd[x]
                    total += alpha
                else:
                    wd[x] = 0
            total += b
            total *= y
            if total <= 0:  # wrong prediction
                for x in xd:
                    wd[x] = wd[x] + (y * xd[x])
                b = b + y
    print(scount)
    print(hcount)
    return {'weights': wd, 'bias': b}


def writeOutput(wd, bias):
    with open('per_model.txt', 'w', encoding="latin1") as out:
        out.write("StandardPerceptronBias," + str(bias) + "\n")
        for x in wd:
            out.write(x + "," + str(wd[x]) + "\n")
    out.close()
    pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python per_learn.py <input_path>')
        sys.exit(1)

    ans = main(sys.argv[1:])
    wd = ans['weights']
    writeOutput(wd, ans['bias'])
