import pickle
import sys
from time import sleep

from PIL import Image
from redis import Redis, exceptions
from sympy import solveset, symbols

try:
    redis = Redis(host='localhost', port=6379)
    pubsub = redis.pubsub()
    pubsub.subscribe('queries')
    pubsub.subscribe('images')
    pubsub.subscribe('equations')
except exceptions.ConnectionError as e:
    print('Can\'t connect to Redis!')
    sys.exit(1)

print('Start listening queries')
while True:
    msg = pubsub.get_message()
    if msg and isinstance(msg['data'], bytes):
        ans = None
        if msg['channel'] == b'queries':
            query = msg['data'].decode('utf-8')
            ans = {
                'query': query,
                'value': query[::-1],
            }

        if msg['channel'] == b'images':
            file_dict = pickle.loads(msg['data'])
            img = Image.open(file_dict['data'])
            ans = {
                'image': file_dict['name'],
                'value': img.rotate(180),
            }

        if msg['channel'] == b'equations':
            equation = msg['data'].decode('utf-8')
            x = symbols('x')
            solution = eval(f'solveset({equation}, x)')
            try:
                answers = pickle.loads(redis.get('equation_answers'))
            except (ValueError, TypeError, pickle.UnpicklingError):
                answers = []
            answers.append({
                'query': str(equation),
                'value': str(solution),
            })
            redis.set('equation_answers', pickle.dumps(answers))

        if ans:
            try:
                answers = pickle.loads(redis.get('answers'))
            except (ValueError, TypeError, pickle.UnpicklingError):
                answers = []
            answers.append(ans)
            redis.set('answers', pickle.dumps(answers))

    sleep(1)
