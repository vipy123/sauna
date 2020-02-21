
from flask import render_template, request, Flask, session, redirect, url_for, escape

from application import app

app.secret_key = b'\xf9\x0bn\xe2[M\x80\xdf\xcdVV\x04\x04\x8e\xf5\xc0'

@app.route('/')
def index():

    return render_template("index.html")


