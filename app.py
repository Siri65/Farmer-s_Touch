import nltk
import pickle
import numpy as np
import json
import random

from keras.models import load_model
from flask_cors import CORS
from nltk.stem import WordNetLemmatizer

from flask import Flask, render_template, request, redirect, url_for, session
from database import Database
from datetime import timedelta

nltk.download('popular')

lemmatizer = WordNetLemmatizer()
model = load_model('model.h5') 
intents = json.loads(open('data_crop.json').read())
words = pickle.load(open('texts.pkl', 'rb'))
classes = pickle.load(open('labels.pkl', 'rb'))
db = Database('crop') # using the database crop.

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)

def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = [{"intent": classes[r[0]], "probability": float(r[1])} for r in results]
    if len(return_list) == 0:
        return [{"intent": "unkown", "probability": 0}]
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    print(ints)
    if ints[0]['probability'] < 0.7:
        return "I'm sorry, I didn't understand that. Could you please rephrase your question?"
    else:
        res = getResponse(ints, intents)
        return res

app = Flask(__name__)
CORS(app)
app.static_folder = 'static'
app.secret_key = '@VMSIRI'
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route("/")
def home():
    return render_template("bloghtml.html")  # Adjust the path to the template folder

@app.route("/garden", methods=['GET'])
def garden():
    if 'username' in session:
        return render_template("garden.html")
    return redirect(url_for('login'))

@app.route("/fruits")
def fruits():
    return render_template("fruits.html")

@app.route("/flower")
def flower():
    return render_template("flower.html")

@app.route("/veg")
def veg():
    return render_template("veg.html")

@app.route("/bloghtml")
def bloghtml():
    return render_template("bloghtml.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for('garden'))
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        if(db.validate(table_name='users', data=(username, username, password))):
            print("Logged In")
            session['username'] = username
            return redirect(url_for('garden'))
        else:
            print("Not Logged In")
            return render_template('login.html', messageL="Please verify your username and password")
    else:
        return render_template("login.html")
    
@app.route("/signup", methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        email = request.form.get('Email')
        location = request.form.get('Location')

        if(not db.isExist(table_name='users', data=(username, email))):
            db.insert(tableName='users', data=(username, password, email, location))
            session['username'] = username
            return redirect(url_for('garden'))
        else:
            print("User already exists")
            return render_template('login.html', messageL="User already Exists", messageS="User already Exists")
    else:
        return redirect(url_for('login'))

@app.route("/contact", methods=['POST'])
def contact():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        number = request.form.get('number')
        subject = request.form.get('subject')
        message = request.form.get('msg')

        print(username)

        db.insert(tableName='contact', data=(username, email, number, subject, message))
    
    return redirect(url_for('bloghtml'))

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    print("Received message:", userText)
    return chatbot_response(userText)

@app.route("/soil")
def soil():
    return render_template("soil.html")

@app.route("/orders", methods=['GET', 'POST'])
def orderPage():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':    
        order_details = request.json
        session['order_details'] = order_details
        
        return redirect(url_for('payment'))
    
    return render_template("orderPage.html", username=session.get('username'))

@app.route("/payment", methods=['GET', 'POST'])
def payment():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('state')
        location = request.form.get('address')
        cardNo = request.form.get('card_number')
        cvv = request.form.get('CVV')
        order_details = session['order_details']
        
        # Process the order details as needed
        user_id = db.getId('users', order_details['username'])

        # Inserting data into the database.
        for product in order_details['products']:
            db.insert(tableName='orders', data=(product['name'], 
                                                product['quantity'], 
                                                product['price'], user_id, 
                                                name, location, cardNo, cvv))

        db.display(table_name='orders')
        return redirect(url_for('popup'))

    return render_template("payment.html")

@app.route("/popup")
def popup():
    return render_template("popup.html")

@app.route("/frusoil")
def frusoil():
    return render_template("frusoil.html")

@app.route("/fruseed")
def fruseed():
    return render_template("fruseed.html")

@app.route("/frusap")
def frusap():
    return render_template("frusap.html")

@app.route("/frupests")
def frupests():
    return render_template("frupests.html")

@app.route("/frufert")
def frufert():
    return render_template("frufert.html")

@app.route("/fruorg")
def fruorg():
    return render_template("fruorg.html")

@app.route("/fruirri")
def fruirri():
    return render_template("fruirri.html")

@app.route("/fruprod")
def fruprod():
    return render_template("fruprod.html")

@app.route("/frumark")
def frumark():
    return render_template("frumark.html")

@app.route("/flosoil")
def flosoil():
    return render_template("flosoil.html")

@app.route("/floseed")
def floseed():
    return render_template("floseed.html")

@app.route("/flosap")
def flosap():
    return render_template("flosap.html")

@app.route("/flopests")
def flopests():
    return render_template("flopests.html")

@app.route("/floirri")
def floirri():
    return render_template("floirri.html")

@app.route("/flofert")
def flofert():
    return render_template("flofert.html")

@app.route("/floorg")
def floorg():
    return render_template("floorg.html")

@app.route("/floprod")
def floprod():
    return render_template("floprod.html")

@app.route("/vegsoil")
def vegsoil():
    return render_template("vegsoil.html")

@app.route("/vegseed")
def vegseed():
    return render_template("vegseed.html")

@app.route("/vegsap")
def vegsap():
    return render_template("vegsap.html")

@app.route("/vegpests")
def vegpests():
    return render_template("vegpests.html")

@app.route("/vegirri")
def vegirri():
    return render_template("vegirri.html")

@app.route("/vegfert")
def vegfert():
    return render_template("vegfert.html")

@app.route("/vegorg")
def vegorg():
    return render_template("vegorg.html")

@app.route("/vegprod")
def vegprod():
    return render_template("vegprod.html")

if __name__ == "__main__":
    app.run(debug=True)
