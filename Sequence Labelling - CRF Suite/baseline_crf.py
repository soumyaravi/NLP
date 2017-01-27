import pycrfsuite
import hw3_corpus_tool as tool
import sys


def train_model(xtrain, ytrain):
    trainer = pycrfsuite.Trainer(verbose=False)
    trainer.append(xtrain, ytrain)
    trainer.set_params({
        'c1': 1.00,  # coefficient for L1 penalty
        'c2': 0.00138
        ,  # coefficient for L2 penalty
        'max_iterations': 100,  # stop earlier

        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })
    trainer.train('baselinecrf')
    return


def test_data(args):
    data = tool.get_data(args[1])
    tagger = pycrfsuite.Tagger()
    tagger.open('baselinecrf')
    features = create_features(data)
    output = tagger.tag(features['feature'])
    print(len(output))
    return {'label': output, 'feature': features}


def read_data(args):
    data = tool.get_data(args[0])
    features = create_features(data)
    return {'xtrain': features['feature'], 'ytrain': features['label'], 'file': features['file'],
            'length': features['length']}


def create_features(data):
    featurelist = []
    labellist = []
    filename = []
    feature_len = []
    for datas in data.__iter__():
        key = datas['file']
        filename.append(key)
        value = datas['dialog']
        prev_speaker = ''
        count = 0
        for utterance in value:
            utterance_list = []

            # feature to check if speaker has changed
            curr_speaker = utterance[1].rstrip()
            if prev_speaker == '':
                utterance_list.append('SC=no')
                prev_speaker = curr_speaker
            elif prev_speaker == curr_speaker:
                utterance_list.append('SC=no')
            else:
                utterance_list.append('SC=yes')

            # feature to check for first utterance
            if count == 0:
                utterance_list.append('FU=yes')
            else:
                utterance_list.append('FU=no')
            count += 1  # feature for every token and pos tag in utterance
            try:
                for tags in utterance[2]:
                    utterance_list.append('token=' + tags[0])
                    utterance_list.append('pos=' + tags[1])
            except TypeError:
                utterance_list.append('token=')
                utterance_list.append('pos=')
            featurelist.append(utterance_list)
            try:
                label = utterance[0].rstrip()
                labellist.append(label)
            except AttributeError:
                labellist.append('')

        feature_len.append(len(value))
    return {'feature': featurelist, 'label': labellist, 'file': filename, 'length': feature_len}


def write_output(args, output):
    features = output['feature']
    count = features['length']
    label = output['label']
    total = 0
    length = 0
    with open(args[2],'w') as out:
        for i in range(0,len(features['file'])):
            out.write('Filename = "' + features['file'][i] + '"\n')
            length += count[i]
            for j in range(total,length):
                try:
                    out.write(label[j]+"\n")
                except IndexError:
                    print("index" + str(j))
            total = length
            out.write("\n")
    return



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python baseline_crf.py INPUTDIR TESTDIR OUTPUTFILE')
        sys.exit(1)
    train = read_data(sys.argv[1:])
    train_model(train['xtrain'], train['ytrain'])
    output = test_data(sys.argv[1:])
    write_output(sys.argv[1:], output)
