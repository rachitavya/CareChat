from flask import Flask,request, render_template
import requests
import pyttsx3
import os
from config import secret_key
# def create_app():
# secret_key = os.environ.get('secret_key')
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
        {'role':'system','content':f'I am experiencing {condition} with severity {severity}. Suggest cure .'},
        {'role':'user','content':query}
    ]}

    response=requests.post(url,json=payload,headers=header)

    try:
        message=response.json()['choices'][0]['message']['content']
    except:
        message=response.json()['error']['message']
    
    text_to_speech(message)
    def save_text_file(file_path, content):
        with open(file_path, 'w') as file:
            file.write(content)


    file_path = 'static/output.txt'
    content = 'This is the content of the file.'
    save_text_file(file_path, content)
    labels.append([query,message])
    return render_template('index.html',label=labels)

if __name__=='__main__':
     app.run(debug=True)