from flask import Flask,request, render_template
import requests
from config import secret_key
import pyttsx3
import os

labels=[]
def text_to_speech(message):
    engine = pyttsx3.init()
    engine.setProperty('rate',125)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.save_to_file(message,'static/test.mp3')
    engine.runAndWait()

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html',label=[])

@app.route('/result',methods=['POST'])
def reply():
    query=request.form.get('message')
    condition=request.form.get('condition')
    severity=request.form.get('severity')
    url="https://api.openai.com/v1/chat/completions"

    header={
    'Authorization':'Bearer '+secret_key,
    'Content-Type':'application/json'
    }

    payload={
    'model':'gpt-3.5-turbo',
    'messages':[
        {'role':'system','content':f'You are experiencing {condition} with severity {severity}.'},
        {'role':'user','content':query}
    ]}

    response=requests.post(url,json=payload,headers=header)

    # message=response.json()['choices'][0]['message']['content']
    message=response.json()['error']['message']
    
    text_to_speech(message)
    labels.append([query,message])
    return render_template('index.html',label=labels)

if __name__=='__main__':
    app.run(debug=True)