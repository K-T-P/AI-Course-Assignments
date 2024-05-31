from pandas import read_csv
from template import NaiveBayesClassifier
from filtering_word import invalid_words
from time import time


def extract_words(tok: str):
    res = []

    if not "http" in tok:
        tmp = ""

        for i in range(len(tok)):
            char = tok[i]

            if char.isalpha():
                if i > 0 and char == tok[i - 1]:
                    continue
                tmp += char
            else:
                if tmp != "" and tmp not in invalid_words:
                    res.append(tmp)
                tmp = ""

        if tmp != "" and tmp not in invalid_words:
            res.append(tmp)

    return res


def preprocess(tweet):
    tweet = str(tweet)
    toks = tweet.lower().split()

    words = []
    for tok in toks:
        words.extend(extract_words(tok))

    return words


def load_data(data_path):
    # load the csv file and return the data
    data = []
    df = read_csv(data_path)
    for index, row in df.iterrows():
        data.append((preprocess(row["text"]), row["label_text"]))
    return data


def eval_model(model, eval_path):
    df = read_csv(eval_path)
    correct, total = 0, 0

    for index, row in df.iterrows():
        total += 1
        prep = preprocess(row["text"])
        cl = model.classify(prep)

        if cl == row["label_text"]:
            correct += 1

    print(f"Model precision at evaluation:\t{correct/total}")


def test_model(model, test_data_path, output_file):
    df = read_csv(test_data_path)

    with open(output_file, "w") as f:
        for index, row in df.iterrows():
            prep = preprocess(row["text"])
            cl = model.classify(prep)

            f.write(f"{cl}\n")


def report_time(title: str, start, end):
    elapsed = int(end - start)
    print(f"{title} took {elapsed // 60} minutes and {elapsed % 60} seconds")


# train your model and report the duration time
train_data_path = "./train_data.csv"
classes = ["positive", "negative", "neutral"]
nb_classifier = NaiveBayesClassifier(classes)

a = time()
nb_classifier.train(load_data(train_data_path))
b = time()
report_time("Training the model", a, b)

eval_path = "./eval_data.csv"
eval_model(nb_classifier, train_data_path)
eval_model(nb_classifier, eval_path)

test_path = "./test_data_nolabel.csv"
test_model(nb_classifier, test_path, "result.txt")

test_string = "I love playing football"
# print(nb_classifier.classify(preprocess(test_string)))
