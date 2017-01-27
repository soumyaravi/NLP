import sys
import os
import collections

predict = {}


def main():
    with open("per_model.txt", "r", encoding="latin1") as infile:
        model = infile.readlines()
    infile.close()
    wd = {}
    ud = {}
    if model[0].__contains__("StandardPerceptronBias"):
        for data in model:
            words = data.split(",")
            if words[0] == "StandardPerceptronBias":
                bias = words[1].strip()
            else:
                wd[words[0].strip()] = words[1].strip()
        return {'weight':wd,'bias':bias, 'model':'std', 'avgweight':''}
    else:
        for data in model:
            words = data.split(",")
            if words[0] == "AveragePerceptronBias":
                bias = words[1].strip()
            elif words[0] == "Length":
                length = int(words[1])
            else:
                if length>0:
                    wd[words[0].strip()] = words[1].strip()
                    length -=1
                else:
                    ud[words[0].strip()] = words[1].strip()
        return {'weight':wd,'bias':bias, 'model':'avg', 'avgweight': ud}


def classify(args, wd, bias,model,ud):
    for subdir, dirs, files in os.walk(args[0]):
        for file in files:
            if (file.endswith('.txt')):
                with open(os.path.join(subdir, file), "r", encoding="latin1") as infile:
                    words = infile.read().split()
                infile.close()
                total = 0
                xd = collections.Counter(words)
                if model == 'std':
                    for x in xd:
                        if x in wd:
                            total += int(wd[x]) * int(xd[x])
                    total += int(bias)
                else:
                    for x in xd:
                        if x in ud:
                            total += float(xd[x]) * float(ud[x])
                    total += float(bias)
                if total>0:
                    predict[os.path.join(subdir, file)] = 'spam'
                else:
                    predict[os.path.join(subdir, file)] = 'ham'
    return


def writeOutput(args):
    with open(args[1],'w',encoding="latin1") as out:
        for data in predict:
            out.write(predict.get(data)+" " + data +"\n")
    out.close()
    return


if __name__ == "__main__":
    if len(sys.argv)!=3:
        print('Usage: python per_classify.py <input_path> <output_filename>')
        sys.exit(1)
    print(sys.argv[1:])
    ans = main()
    classify(sys.argv[1:],ans['weight'] , ans['bias'],ans['model'], ans['avgweight'])
    writeOutput(sys.argv[1:])