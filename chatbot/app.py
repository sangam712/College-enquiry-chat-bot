import re
import sqlite3
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, render_template, request
from flask import Blueprint


app = Flask(__name__)

botname='Chitti'
chatbot = ChatBot(botname, 
	#storage_adapter='chatterbot.storage.SQLStorageAdapter',
	logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.8
        },
        {
            "import_path": "chatterbot.logic.MathematicalEvaluation",

        },
        {
            "import_path": "chatterbot.logic.UnitConversion",

        },
        {
            "import_path": "profanity_adapter.ProfanityAdapter",

        },
        {
            "import_path": "covid19_adapter.Covid19Adapter",

        },
    ],
 )

@app.route("/")
def home():
    return render_template("index.html", botname=botname)

@app.route("/get")
def get_bot_response():
	userInput=request.args.get('msg')
	return str(chatbot.get_response(userInput))

# our main blueprint
main = Blueprint('main', __name__,template_folder='templates')

@app.route("/hello") # home page that return 'index'
def feed():
    if request.method == 'GET':
        return render_template("feeds.html")

@app.route("/back",methods=['POST']) # home page that return 'index'
def backs():
    name1 = request.form["name"]
    print(name1)
    emails1 = request.form["email"]
    cont1 = request.form["subject"]
    connection = sqlite3.connect('feedback.db')
    cursor = connection.cursor()
    params = (name1,emails1,cont1)
    #query1 = "INSERT INTO  feedback VALUES({n1},{e1},{c1})".format(n1=name1,e1=emails1,c1=cont1)
    #query1 = ("INSERT INTO  feedback VALUES(?,?,?)",params)
    print('ok')
    cursor.execute("INSERT INTO feedback (username,email,content) VALUES(?,?,?)",(name1,emails1,cont1))
    #cursor.execute(query1)
    connection.commit()
    print('ok2')
    return render_template("back.html")

@app.route("/hello") # saving data
def savedata():
    name = request.form["username"]
    emails = request.form["email"]
    cont = request.form["content"]
    connection = sqlite3.connect('feedback.db')
    cursor = connection.cursor()
    query1 = "INSERT INTO  feedback VALUES(?,?,?)"
    cursor.execute(query1)
    connection.commit()

if __name__ == '__main__':
	app.run(debug=True)
