import os
from flask import Flask, redirect, render_template, request, url_for
from diy import create_diy_response
import json
app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        thingy = request.form["thingy"]
        result = create_diy_response(thingy)
        print(result)
        return render_template("index.html", data=result)
    else:
        return render_template("index.html", data=None)