import os
import pickle
 
from flask import Flask, redirect, render_template, request
from redis import Redis
 
app = Flask(__name__)
redis = Redis(host='localhost', port=6379)


@app.route('/')
def input_data():
    try:
        answers = pickle.loads(redis.get('answers'))
    except (ValueError, TypeError, pickle.UnpicklingError):
        answers = []
    
    image_files = os.listdir('static')
    for ans in answers:
        if 'image' in ans:
            if ans['image'] not in image_files:
                ans['value'].save(os.path.join('static', ans['image']))

    return render_template('input.html', answers=answers)
 

@app.route('/send', methods=['POST'])
def send():
    redis.publish('queries', request.form.get('input_text'))
    return redirect('/')


@app.route('/transform_image', methods=['POST'])
def transform_image():
    file = request.files.get('image')
    redis.publish('images', pickle.dumps({
        'data': file.stream,
        'name': file.filename,
    }))
    return redirect('/')
