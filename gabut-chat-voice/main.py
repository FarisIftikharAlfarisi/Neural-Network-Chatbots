import sys
import threading
import tkinter as tk

import speech_recognition
import pyttsx3 as tts

from neuralintents.assistants import BasicAssistant

class Assistant:
    
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate", 150)
        
        self.assistant = BasicAssistant('intents.json', model_name='voice-assistant-model')
        self.assistant.fit_model()
        self.assistant.save_model()
        
        self.root = tk.Tk()
        self.label = tk.Label(text="🤖", font=("Arial",120,"bold"))
        self.label.pack()
        
        threading.Thread(target=self.run_assistant()).start()
        
        self.root.mainloop()
        
    def create_file(self):
        with open("test-file.txt","w") as f:
            f.write("Hai this file is a test file")
    
    def run_assistant(self):
        while True:
            try :
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)
                    
                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()
                    
                    if "hey bot" in text:
                        self.label.config(fg="red")
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        if text == "stop":
                            self.speaker.say("Goodbye, pleasure to help you")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            self.root.destroy()
                            sys.exit(0)
                        else :
                            if text is not None:
                                response = self.assistant.request(text)
                                if response is not None:
                                    self.speaker.say(response)
                                    self.speaker.runAndWait()
                            self.label.config(fg="black")
                                
            except :
                self.label.config(fg="black")
                continue
            
Assistant()
Assistant.run_assistant()