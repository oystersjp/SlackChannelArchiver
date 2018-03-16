import json
import logging
import urllib.request
import os
from datetime import datetime
import time

print('Loading function... ')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class PostJson(object):
    def __init__(self):
        #self.BOT_TOKEN =  os.environ['BOT_TOKEN']
        #self.OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
        self.BOT_MESSAGE = os.environ['BOT_MESSAGE']
        self.BOT_ICON = os.environ['BOT_ICON']
        self.BOT_NAME = os.environ['BOT_NAME']
        self.LEGACY_TOKEN = os.environ['LEGACY_TOKEN']

    def headers(self):
        return {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer {0}'.format(self.LEGACY_TOKEN)
        }

    def data_list(self):
        return {'token': self.LEGACY_TOKEN, 'exclude_archived': 'true'}

    def data_hist(self, channel):
        return {'token': self.LEGACY_TOKEN, 'channel': channel, 'count': 1}

    def data_message(self, channel):
        return {
            'token': self.LEGACY_TOKEN,
            'channel': channel,
            'text': self.BOT_MESSAGE,
            'username': self.BOT_NAME,
            'icon_emoji': self.BOT_ICON
        }

    def headers_archive(self):
        return {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer {0}'.format(self.LEGACY_TOKEN)
        }

    def data_archive(self, channel):
        return {'token': self.LEGACY_TOKEN, 'channel': channel}


def handler(event, context):
    # Output the received event to the log
    #logging.info(json.dumps(event))
    ARCHIVE_AFTER_DAYS = os.environ['ARCHIVE_AFTER_DAYS']
    # list channel
    url = 'https://slack.com/api/channels.list'
    post_head = PostJson().headers()
    post_body = PostJson().data_list()
    req = urllib.request.Request(
        url,
        data=json.dumps(post_body).encode('utf-8'),
        method='POST',
        headers=post_head)
    res = urllib.request.urlopen(req)
    logger.info('post result: %s', res.msg)
    channels = json.loads(res.read().decode('utf8'))

    # get channels info / require scope :channels:history
    for channel in channels.get('channels'):
        logger.info('checl channel: %s ', channel.get('name', ''))
        url = "https://slack.com/api/channels.history"  # does not support application/json
        post_body = PostJson().data_hist(channel.get('id'))
        req = urllib.request.Request(
            url,
            urllib.parse.urlencode(post_body).encode('utf-8'))
        res = urllib.request.urlopen(req)
        channelhist = json.loads(res.read().decode('utf-8'))
        #print(channelhist)
        messages = channelhist.get('messages')
        message = messages.pop(0) if messages else {}
        ts = message.get('ts', '1000000000')  # epoch 2001/9/9 10:46:40
        ts_datetime = datetime.fromtimestamp(float(ts))
        now_datetime = datetime.now()
        diff_datetime = now_datetime - ts_datetime
        # check old channels
        if (int(diff_datetime.days) > int(ARCHIVE_AFTER_DAYS)):
            logger.info('target channel to archive: %s', channel.get(
                'name', ''))
            # message to target channel / require scope : chat:write:user
            post_data = PostJson().data_message(channel.get('id'))
            url = 'https://slack.com/api/chat.postMessage'
            req = urllib.request.Request(
                url,
                data=json.dumps(post_data).encode('utf-8'),
                method='POST',
                headers=post_head)
            res = urllib.request.urlopen(req)
            logger.info('message result: %s', res.msg)
            # archive target channel / require scope : LEGACY TOKEN
            post_head = PostJson().headers_archive()
            post_data = PostJson().data_archive(channel.get('id'))
            url = 'https://slack.com/api/channels.archive'
            req = urllib.request.Request(
                url,
                data=json.dumps(post_data).encode('utf-8'),
                method='POST',
                headers=post_head)
            res = urllib.request.urlopen(req)
            logger.info('archive result: %s', res.msg)
            #load = json.loads(res.read().decode('utf8'))
            #print (load)
            return 'ok'  # archive 1 channel and exit function, comment-out if you want archive every old channel

    return 'ok'
