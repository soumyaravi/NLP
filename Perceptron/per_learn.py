import sys, os
import collections
import random


def main(args):
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
                infile.close()

    for num in range(0,20):
        keys = filelist.keys()
        #random.shuffle(list(keys))
        for key in keys:
            if key.__contains__('spam'):
                y = 1
            else:
                y = -1
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
