from neuralintents.assistants import BasicAssistant

assistant = BasicAssistant('intents.json', model_name='voice-gabut')
assistant.fit_model(epochs=200)
assistant.save_model()