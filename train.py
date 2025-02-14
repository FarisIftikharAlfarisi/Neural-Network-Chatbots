import random
import json
import pickle
import numpy as np

import nltk 
from nltk.stem import WordNetLemmatizer

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers.legacy import SGD
from keras.preprocessing.sequence import pad_sequences

from colorama import Fore

lemmatizier = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []

ignore_letters = ['?','!',';',':','.',',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend([lemmatizier.lemmatize(w) for w in word_list if w not in ignore_letters])
        documents.append((word_list, intent['tag']))
        
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

unique_words = sorted(set(words)) 

classes = sorted(set(classes))

pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_pattern = document[0]
    word_pattern = [lemmatizier.lemmatize(word.lower()) for word in word_pattern]
    for word in words:
        bag.append(1) if word in word_pattern else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag,output_row])

random.shuffle(training) 

train_x = pad_sequences([x[0] for x in training])
train_y = pad_sequences([x[1] for x in training])

model = Sequential()
model.add(Dense(128,input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax'))

sgd = SGD(learning_rate=0.01,decay=1e-6,momentum=0.9,nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(np.array(train_x),np.array(train_y),epochs=200,batch_size=5,verbose=1)

model.save('gabut-chatbot.model')

print(Fore.GREEN + 'MODEL BUILD SUCCEEDED')