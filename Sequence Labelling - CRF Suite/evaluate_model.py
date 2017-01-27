import sys
import os
import csv


def evaluate(path,filename):
    with open(os.path.join(path[0],filename),'r') as infile:
        lines = infile.readlines()
    labels = {}
    tags = []
    count = 0
    total = 0
    for data in lines:
        data = data.strip()
        if 'Filename' in data:
            name = data.split('\"')
            paths = path[0]+ 'test/' + name[1]
        elif data == '':
            labels[paths] = tags
            tags = []
        else:
            tags.append(data)
    for data in (labels):
        tags = labels[data]
        with open(data,'r') as infile:
            reader = csv.reader(infile)
            next(reader)
            i = 0
            for row in reader:
                if row[0].strip() == tags[i]:
                    count +=1
                total +=1
                i+=1
    accuracy = float(count / total) * 100
    print("Accuracy = " + str(accuracy) + "%")
    return


if __name__ == '__main__':
    path = sys.argv[1:2]
    filename = sys.argv[2:3]
    print("For " + filename[0] +" -->")
    evaluate(path,filename[0])