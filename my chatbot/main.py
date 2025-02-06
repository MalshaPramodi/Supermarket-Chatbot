import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)
    
#Load trained data
PATH = "data.pth"
data = torch.load(PATH)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot = "Chatbot"  

print(" Hello I am your chatbot. I am here to help you to find your groceries and others by providing the shelf number. Type 'quit' to end the conversation.")

goods_requested = {}  

def get_response(msg):
    global goods_requested
    
    sentence = tokenize(msg)
    N = bag_of_words(sentence, all_words)
    N = N.reshape(1, N.shape[0])
    N = torch.from_numpy(N).to(device)
    
    output = model(N)
    _, predicted = torch.max(output, dim=1)
    
    tag = tags[predicted.item()]
    
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])
                
                # Track goods and their associated shelf number
                if 'Shelf number' in response:
                    shelf_number = response.split("Shelf number ")[-1].split(".")[0].strip()
                    goods = ", ".join(sentence)  # Assuming sentence contains goods
                    if shelf_number not in goods_requested:
                        goods_requested[shelf_number] = []
                    goods_requested[shelf_number].append(goods)
                
                return response       
            
    return "I'm sorry. I cannot understand. Can you tell it again"        
    