import random
import json
import pickle
import numpy as np

import nltk
from nltk import WordNetLemmatizer

from keras.models import load_model

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('gabut-chatbot.model')

def clean_up_sentence(sentence):
    sentence_word = nltk.word_tokenize(sentence)
    sentence_word = [lemmatizer.lemmatize(word) for word  in sentence_word]
    return sentence_word

def bag_of_word(sentence):
    sentence_word = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_word:
        for i,word in enumerate(words):
            if word  == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_word(sentence)
    r = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    result = [[i, r] for i,r in enumerate(r) if r > ERROR_THRESHOLD]
    result.sort(key = lambda x : x[1], reverse=True)
    return_list = []
    for r in result:
        return_list.append({'intent':classes[r[0]], 'probability':str(r[1])})
    return return_list

def get_response(intents_list,intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
        else:
            result = "Unfortunately your promnt is too advance, my biggest apologies, i'm not handle that question, sorry:)"
    return result

print("Bot is running....")
print("")

print
while True:
    pesan = input("prompt : ")
    ints = predict_class(pesan)
    res = get_response(ints,intents)
    print("respons : " + res)
    print(" ")