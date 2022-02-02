import json
 
from flask import Flask, redirect, render_template, request
from redis import Redis
 
app = Flask(__name__)
redis = Redis(host='localhost', port=6379)
 
@app.route('/')
def input_data():
    try:
        answers = json.loads(redis.get('answers'))
    except (ValueError, TypeError):
        answers = []
    print(answers)
    return render_template('input.html', answers=answers)
 
@app.route('/send', methods=['POST'])
def send():
    redis.publish('queries', request.form.get('input_text'))
    return redirect('/')


@app.route('/transform_image', methods=['POST'])
def transform_image():
    file = request.files.get('image')
    file.save(file.filename)
    return redirect('/')
