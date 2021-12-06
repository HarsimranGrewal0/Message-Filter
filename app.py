import pickle
from flask import Flask, render_template, request
import string
#import mysql.connector
#from mysql.connector import Error

app = Flask(__name__)
loadedModel = pickle.load(open('Model1.pkl', 'rb'))

def textFilerting(message):
    noPum = [char for char in message if char not in string.punctuation]
    noPum = ''.join(noPum)
    return [word for word in noPum.split() if word.lower() not in string.punctuation]
 
#def create_db_connection(hostname, username, password, database):
    connection = None
    try:
        connection = mysql.connector.connect(host=hostname, user=username, passwd=password, database=database)
        print("connection successful")
    except Error as e:
        print("Error: "+ str(e))
        
    return connection

#def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query Successful")
    except Error as e:
        print("Error:" + str(e))

@app.route("/")
def home():
    return render_template('form.html')
    

@app.route("/predict", methods=["POST"])
def predict():
    name = request.form['name']
    message = request.form['message']

    prediction = loadedModel.predict([message])[0]
    
    if prediction == 'Ham':
        prediction = "Genuine Message"
    else:
        prediction = 'Spam Message'

    #connection = create_db_connection('localhost', 'root', '', 'harsimran')
    #query = f"insert into grewal values(null, '{name}', '{message}', '{prediction}')"
    #execute_query(connection,query)

    return render_template('form.html', api_message=message, api_output=prediction)

if __name__ == '__main__':
    app.run(debug=True)