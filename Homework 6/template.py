# Naive Bayes 3-class Classifier 
# Authors: Baktash Ansari - Sina Zamani 

# complete each of the class methods  
from math import log

class NaiveBayesClassifier:

    def __init__(self, classes):
        # initialization: 
        # inputs: classes(list) --> list of label names
        # class_word_counts --> frequency dictionary for each class
        # class_counts --> number of instances of each class
        # vocab --> all unique words  
        self.classes = classes
        self.class_word_counts = None
        self.class_counts = None
        self.vocab = None
        self.words_probability = {}
        self.classes_prob = {}

    def train(self, data):
        # training process:
        # inputs: data(list) --> each item of list is a tuple 
        # the first index of the tuple is a list of words and the second index is the label(positive, negative, or neutral)
        self.vocab = []
        self.class_word_counts = {}
        self.class_counts = {
            self.classes[0]:0,
            self.classes[1]:0,
            self.classes[2]:0
                             }
        
        #create frequency table
        for features, label in data:
            for feature in features:
                if feature not in self.vocab:
                    self.class_word_counts[feature] = {}
                    self.class_word_counts[feature][self.classes[0]] = 0
                    self.class_word_counts[feature][self.classes[1]] = 0
                    self.class_word_counts[feature][self.classes[2]] = 0
                    self.vocab.append(feature)

                self.class_word_counts[feature][label] += 1
                self.class_counts[label] += 1
        
        for word in self.vocab:
            self.words_probability[word] = {}
            self.words_probability[word][self.classes[0]] =\
                self.calculate_likelihood(word, self.classes[0])
            self.words_probability[word][self.classes[1]] =\
                self.calculate_likelihood(word, self.classes[1])
            self.words_probability[word][self.classes[2]] =\
                self.calculate_likelihood(word, self.classes[2])
        
        self.calculate_prior()

    def calculate_prior(self):
        # calculate log prior
        # you can add some attributes to this method
        
        for classs in self.classes:
            self.classes_prob[classs] = log(self.class_counts[classs])

    def calculate_likelihood(self, word, label):
        # calculate likelihhood: P(word | label)
        # return the corresponding value
        prob = (self.class_word_counts[word][label] + 1) \
            / (self.class_counts[label] + len(self.vocab))
        return log(prob)

    def classify(self, features):
        # predict the class
        # inputs: features(list) --> words of a tweet 
        best_class = None 
        best_class_score = float("-inf")
        if features:
            for single_class in self.classes:
                score = self.classes_prob[single_class]
                for word in features:
                    if word not in self.vocab:
                        continue
                    score += self.words_probability[word][single_class]
                
                if score > best_class_score:
                    best_class = single_class
                    best_class_score = score
        else:
            best_class = 'neutral'
        return best_class
    

# Good luck :)
