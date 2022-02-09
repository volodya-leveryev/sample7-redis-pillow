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
    return render_template('input.html', answers=answers)


@app.route('/reverse_text', methods=['POST'])
def reverse_text():
    redis.publish('queries', request.form.get('input_text'))
    return redirect('/')


@app.route('/pics/')
def pictures():
    try:
        answers = pickle.loads(redis.get('answers'))
    except (ValueError, TypeError, pickle.UnpicklingError):
        answers = []
    
    image_files = os.listdir('static')
    for ans in answers:
        if 'image' in ans:
            if ans['image'] not in image_files:
                ans['value'].save(os.path.join('static', ans['image']))

    return render_template('pictures.html', answers=answers)


@app.route('/transform_image', methods=['POST'])
def transform_image():
    file = request.files.get('image')
    redis.publish('images', pickle.dumps({
        'data': file.stream,
        'name': file.filename,
    }))
    return redirect('/')


@app.route('/equations/')
def equations():
    error = request.args.get('error')
    try:
        answers = pickle.loads(redis.get('equation_answers'))
    except (ValueError, TypeError, pickle.UnpicklingError):
        answers = []
    return render_template('equations.html', error=error, answers=answers)


@app.route('/solve_equation/', methods=['POST'])
def solve_equation():
    try:
        a = float(request.form.get('a'))
        b = float(request.form.get('b'))
        c = float(request.form.get('c'))
    except ValueError:
        return redirect('/equations/?error=1')

    equation = f'({a})*x**2 + ({b})*x + ({c})'
    redis.publish('equations', equation)
    return redirect('/equations/')
