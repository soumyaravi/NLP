import nltk.metrics
from nltk.corpus import movie_reviews
import os
from nltk.corpus import stopwords


top_words = []


def word_feats(words):

    return dict([(word, True) for word in words])


def words_feats(words):
    return dict([(word, True) if word in top_words else (word,False) for word in words.split()])


def train():
    #get all negative movie ids
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')
    #convert into feature set
    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

    trainfeats = negfeats + posfeats
    classifier = nltk.NaiveBayesClassifier.train(trainfeats)

    return classifier


def find_top_words():
    #classifier.show_most_informative_features(10)
    all_words = [word for word in movie_reviews.words()]
    all_words = nltk.FreqDist(all_words)
    top_words = list(all_words.keys())[:50000]
    return top_words


def test(classifier):
    count = 0
    with open('Naive Bayes results.csv','w') as out:
        out.write('Actual,Classified\n')
    for dirs, subdir, files in os.walk('D:/Projects/NLP/amazon'):
        for file in files:
            path = os.path.join(dirs, file)
            if 'pos' in path:
                category = 'pos'
            else:
                category = 'neg'
            with open(path, 'r') as infile:
                for test_sentence in infile:
                    # Tokenize the line.
                    doc = test_sentence.lower().split()
                    featurized_doc = {i: (i in doc) for i in top_words}
                    tagged_label = classifier.classify(featurized_doc)
                    with open('Naive Bayes results.csv', 'a') as out:
                        out.write(category + "," + tagged_label + "\n")             
            count += 1
            if count%50 == 0:
                print(count)
    return

    #print("Maximum Entropy Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)


if __name__ == '__main__':
    top_words = find_top_words()
    classifiers = train()
    test(classifiers)