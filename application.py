from flask import Flask, render_template, request, url_for, redirect
import random
app = Flask(__name__)

@app.route("/")
def index():
    stock = random.randint(0, 15)
    quote = random.randint(0, 15)
    return render_template("index.html", stock=stock, quote=quote)

