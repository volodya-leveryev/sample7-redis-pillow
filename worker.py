import json
from time import sleep
 
from redis import Redis
 
redis = Redis(host='localhost', port=6379)
pubsub = redis.pubsub()
pubsub.subscribe('queries')
 
while True:
    msg = pubsub.get_message()
    if msg and isinstance(msg['data'], bytes):
        # sleep(30)
        print(msg['data'])
        query = msg['data'].decode('utf-8')
        try:
            answers = json.loads(redis.get('answers'))
        except (ValueError, TypeError):
            answers = []
        answers.append({
            'query': query,
            'value': query[::-1],
        })
        redis.set('answers', json.dumps(answers))
    sleep(1)
