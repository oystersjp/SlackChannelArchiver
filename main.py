import json
import logging
import urllib.request
import os
import datetime
from datetime import datetime
import time

print('Loading function... ')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


#def event_to_json(event):
#    if 'body' in event:
#        body = json.loads(event.get('body'))
#        return body
#    elif 'token' in event:
#        body = event
#        return body
#    else:
#        logger.error('unexpected event format')
#        exit


#class ChallangeJson(object):
#    def data(self, key):
#        return {
#            'isBase64Encoded': 'true',
#            'statusCode': 200,
#            'headers': {},
#            'body': key
#        }


class PostJson(object):
    def __init__(self):
        self.BOT_TOKEN = os.environ['BOT_TOKEN']
        self.OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
    def headers(self):
        return {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer {0}'.format( self.BOT_TOKEN)
        }
    def data(self):
        return {
            'token': self.OAUTH_TOKEN,
            'exclude_archived': 'true'
        }


def handler(event, context):
    # Output the received event to the log
    logging.info(json.dumps(event))
    #body = event_to_json(event)
    BOT_MESSAGE = os.environ['BOT_MESSAGE']
    OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
    ARCHIVE_AFTER_DAYS = os.environ['ARCHIVE_AFTER_DAYS']
    BOT_ICON = os.environ['BOT_ICON']
    BOT_NAME = os.environ['BOT_NAME']
    BOT_TOKEN = os.environ['BOT_TOKEN']
    # return if it was challange-event
    #if 'challenge' in body:
    #    challenge_key = body.get('challenge')
    #    logging.info('return challenge key %s:', challenge_key)
    #    return ChallangeJson().data(challenge_key)

    # list channel
    url = 'https://slack.com/api/channels.list'
    post_head = PostJson().headers()
    post_body = PostJson().data()
    req = urllib.request.Request(url,data=json.dumps(post_body).encode('utf-8'), method='POST', headers=post_head)
    res = urllib.request.urlopen(req)
    logger.info('post result: %s', res.msg)
    channels = json.loads(res.read().decode('utf8'))

    #print(channels)
    # chekc old channel
    for channel in channels.get('channels'):
        url = "https://slack.com/api/channels.info"
        params = urllib.parse.urlencode({
                'token': BOT_TOKEN,
                'channel': channel.get('id')
            })
        params = params.encode('utf-8')
        req = urllib.request.Request(url, params)
        response = urllib.request.urlopen(req).read()
        channelsinfo = json.loads(response.decode('utf-8'))
        print(channelsinfo)
        channel = channelsinfo.get('channel',{})
        latest = channel.get('latest',{})
        ts = latest.get('ts','1000000000') # epoch 2001/9/9 10:46:40
        dt = datetime.fromtimestamp(float(ts))
        now = datetime.now()
        diff = now - dt 
        if ( int(diff.days) > int(ARCHIVE_AFTER_DAYS) ):
            logger.info('target channel: %s',  channel.get('name',''))
            # todo: message to target channel
            
            # todo: archive target channel

    return 'ok'


#if __name__ == '__main__':
#   handler('','')

