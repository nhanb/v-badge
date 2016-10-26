from flask import render_template
from vbadge import app


@app.route('/')
def index():
    return render_template('index.html')
