import os

import openai
from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
import pandas as pd
import yaml

from Persona import Persona
from Connector import Connector, write_yaml

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def welcome():

    return render_template(
        "index.html",
        )

@app.route("/chat", methods=["GET", "POST"])
def table():
    db = 'chinook'
    interpreter = Persona("interpreter")
    model = 'gpt-3.5-turbo'
    if request.method == "POST":
        question = request.form["question"]
        messages = interpreter.construct_messages(db, question)
        response = openai.ChatCompletion.create(
            model=model,
            # temperature=0.6,
            messages = messages
        )
        return redirect(url_for("table", result=response.choices[0].message.content))
    
    query = request.args.get("result")
    data = [{"": 0}]
    if query != "":
        con = Connector(db)
        print(query)
        data = con.query_SQLite(query)
        print(data)
    
    df = pd.DataFrame(data)
    table = df.to_html(index=False)

    return render_template(
        "chat.html",
        table = table,
        query = query
        )

@app.route('/semantics', methods=["GET", "POST"])
def semantics():
    if request.method == 'POST':
        # Process the form data
        name = request.form['name']
        table = request.form['table']
        calculation = request.form['calculation']
        dimensions = request.form['dimensions']

        # Save the data to the database
        data = {
            'metric': {
                'name': name, 
                'table': table,
                'calculation': calculation,
                'dimensions': dimensions
            }
            }

        filename = "semantics/test.yaml"
        write_yaml(data, filename)

        # Redirect to a success page or perform any other action
        return render_template('saved.html')
    
    return render_template('semantics.html')

@app.route('/sources')
def sources():
    return render_template('sources.html')