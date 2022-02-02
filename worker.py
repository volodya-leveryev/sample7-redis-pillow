import pickle
from time import sleep

from PIL import Image
from redis import Redis
 
redis = Redis(host='localhost', port=6379)
pubsub = redis.pubsub()
pubsub.subscribe('queries')
pubsub.subscribe('images')
 
while True:
    msg = pubsub.get_message()
    if msg and isinstance(msg['data'], bytes):
        ans = None
        print(msg)
        if msg['channel'] == b'queries':
            # sleep(30)
            print(msg['data'])
            query = msg['data'].decode('utf-8')
            ans = {
                'query': query,
                'value': query[::-1],
            }
        
        if msg['channel'] == b'images':
            file = pickle.loads(msg['data'])
            print('!!!!!!', type(file))
            # img = Image.open(file.stream)
            # ans = {
            #     'image': file.filename,
            #     'value': img.rotate(180),
            # }

        if ans:
            try:
                answers = pickle.loads(redis.get('answers'))
            except (ValueError, TypeError, pickle.UnpicklingError):
                answers = []
            answers.append(ans)
            redis.set('answers', pickle.dumps(answers))

    sleep(1)
