from flask import render_template, flash, redirect, url_for, request, jsonify, send_from_directory
from app import app

@app.route('/')
@app.route('/index')
def landing_page():
    return "Hello"
    # return render_template("landing-page.html", title="Welcome")