from decimal import Decimal
from datetime import datetime
import json

import requests


SCORE_URL = "https://55pz4ifq59.execute-api.us-east-1.amazonaws.com/prod/score"


class Score(object):
    
    def __init__(self, name, time, ghost):
        self.name = name
        self.time = time
        self.ghost = ghost


def post_score(score):
    now = datetime.utcnow().strftime('%Y-%m-%d')

    requests.post(SCORE_URL, json={
        'date' : now, 
        'time' : score.time, 
        'name' : score.name if score.name != '' else '*nobody*',
        'ghost' : score.ghost})   

def get_hi_scores(count):
    now = datetime.utcnow().strftime('%Y-%m-%d')

    response = requests.get(SCORE_URL)
    # print response.json()
    scores = []
    for score in response.json():
        scores.append(Score(
            score['name'],
            score['time'],
            score['ghost']
        ))
        
    return scores

