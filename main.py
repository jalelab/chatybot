# main.py
from . import chat
from autocorrect import Speller
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from datetime import datetime
import os
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    current_time = datetime.now()
    current_time = current_time.strftime("%H:%M")
    return render_template('index.html', current_time=current_time)

@main.route("/get")
def get_bot_response():
    spell = Speller()
    userText = request.args.get('msg')
    response= str(chat.chatbot_response(userText))
    if response in ["Sorry, can't understand you", "Please give me more info", "Not sure I understand"]:
        response= str(chat.chatbot_response(spell(userText)))
    return response

@main.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@main.route("/jsoneditor", methods=['GET','POST'])
@login_required
def jsoneditor():

    if request.method =='POST':
        JsonData=request.get_json()
        print(JsonData)
        intents_file=os.path.join(os.getcwd(),"project", "Model", "intents.json")
        intents = open(intents_file,"w+")
        json.dump(JsonData, intents)
        intents.close()
        trainer_file = os.path.join(os.getcwd(), "project", "train_chatbot.py")
        command = "python " + trainer_file
        os.system(command)
        return 'Modification submited'

    elif request.method=='GET':
        intents = json.loads(open(os.path.join(os.getcwd(),"project", "Model", "intents.json")).read())
        return render_template("jsoneditor.html",  intent=intents)
