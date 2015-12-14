from decimal import Decimal
from datetime import datetime
import json

import boto3
from boto3.dynamodb.conditions import Key


AWS_ACCESS_KEY_ID = 'AKIAJ3WXJ6XEWAKF3HBQ'
AWS_SECRET_ACCESS_KEY = '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' # Hello github scanners. Sadly, these credentials are useless to you.
REGION = 'us-east-1'
boto3.setup_default_session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)


class Score(object):
    
    def __init__(self, name, time, ghost):
        self.name = name
        self.time = time
        self.ghost = ghost


def post_score(score):
    now = datetime.utcnow().strftime('%Y-%m-%d')

    dynamodb = boto3.resource('dynamodb')
    hi_score_table = dynamodb.Table('winterwizardjam_hiscore')
    hi_score_table.put_item(Item={
        'date' : now, 
        'time' : Decimal(str(score.time)), 
        'name' : score.name if score.name != '' else '*nobody*',
        'ghost' : json.dumps(score.ghost)
    })
    

def get_hi_scores(count):
    now = datetime.utcnow().strftime('%Y-%m-%d')

    dynamodb = boto3.resource('dynamodb')
    hi_score_table = dynamodb.Table('winterwizardjam_hiscore')
    
    response = hi_score_table.query(Limit=count, KeyConditionExpression=Key('date').eq(now))
    scores = []
    for item in response['Items']:
        scores.append(Score(
            item['name'],
            float(item['time']),
            json.loads(item['ghost'])
        ))
        
    return scores

