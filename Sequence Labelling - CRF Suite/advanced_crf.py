import pycrfsuite
import hw3_corpus_tool as tool
import sys


def train_model(xtrain, ytrain):
    trainer = pycrfsuite.Trainer(verbose=False)
    trainer.append(xtrain, ytrain)
    trainer.set_params({
        'c1': 1.0,  # coefficient for L1 penalty
        'c2': 0.00115,  # coefficient for L2 penalty
        'max_iterations': 75,  # stop earlier

        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })
    trainer.train('advanced')
    return


def test_data(args):
    data = tool.get_data(args[1])
    tagger = pycrfsuite.Tagger()
    tagger.open('advanced')
    features = create_features(data)
    output = tagger.tag(features['feature'])
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
                utterance_list.append('SC=0')
                prev_speaker = curr_speaker
            elif prev_speaker == curr_speaker:
                utterance_list.append('SC=0')
            else:
                utterance_list.append('SC=1')

                # feature to check for first utterance
            if count == 0:
                utterance_list.append('FU=1')
            else:
                utterance_list.append('FU=0')
            count += 1

            #feature to store length of text
            text_length = len(utterance[3])
            utterance_list.append('length_' + str(text_length))
            question = 'no'
            if '?' in utterance[3]:
                question = 'yes'
            utterance_list.append('question_' + question)
            # feature for every token and pos tag in utterance
            try:
                i = 0
                token_list = []
                pos_list = []
                bigram = []
                bigram_pos = []
                position = []
                for tags in utterance[2]:
                    token_list.append('token_' + tags[0])
                    pos_list.append('pos_' + tags[1])
                    position.append('position_' + tags[0] + '=' + str(i))
                    i += 1
            except TypeError:
                token_list.append('token_')
                pos_list.append('pos_')
                position.append('position_' + str(i))
                i += 1
            try:
                for i in range(1,len(utterance[2])):
                    token = 'bigram_'
                    pos = 'bigrampos_'
                    tags = utterance[2][i-1]
                    tags_next = utterance[2][i]
                    token += tags[0] + '_' + tags_next[0]
                    pos += tags[1] + '_' + tags_next[1]
                    bigram.append(token)
                    bigram_pos.append(pos)
            except TypeError:
                bigram.append('bigram_')
                bigram_pos.append('bigrampos_')

            utterance_list.extend(token_list)
            utterance_list.extend(pos_list)
            utterance_list.extend(bigram)
            utterance_list.extend(bigram_pos)
            utterance_list.extend(position)
            featurelist.append(utterance_list)
            try:
                label = utterance[0].rstrip()
                labellist.append(label)
            except AttributeError:
                labellist.append('')

        feature_len.append(len(value))
    print(utterance_list)
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
            total =length
            out.write("\n")
    return


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python advanced_crf.py INPUTDIR TESTDIR OUTPUTFILE')
        sys.exit(1)
    train = read_data(sys.argv[1:])
    train_model(train['xtrain'], train['ytrain'])
    output = test_data(sys.argv[1:])
    write_output(sys.argv[1:], output)