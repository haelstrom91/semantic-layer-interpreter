import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import pandas as pd

from Persona import Persona
from Connector import Connector

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
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
        "index.html",
        table = table,
        query= query
        )

@app.route('/semantics')
def about():
    return render_template('semantics.html')

@app.route('/sources')
def contact():
    return render_template('sources.html')