import click
import requests
import time
import json
import os
import logging
from parse_site import get_list_of_posts, filter_out
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s ::: %(name)s: %(message)s (%(filename)s:%(lineno)d)',
                                        datefmt='%Y-%m-%d %H:%M:%S')
TELEGRAM_URL = 'https://api.telegram.org/botBOT_TOKEN/sendMessage?'
TELEGRAM_URL_CHECK = 'https://api.telegram.org/botBOT_TOKEN/getUpdates'

BASE_URL = 'https://www.skisport.ru/'
FORUM = 'forum/22/'

@click.command()
@click.option('--t_token', help='telegramm bot token', required=True)
@click.option('--channel', help='channel name', required=True)
def main(t_token, channel):

    def bot_action(text, chat_id):
        if text == 'ping':
            requests.get(TELEGRAM_URL.replace('BOT_TOKEN', t_token), params = {'chat_id': chat_id, 'text': 'I am alive and full of health!'})

    if not os.path.isfile('log.txt'):
        logFile = open('log.txt','w')
        logFile.close()
    if not os.path.isfile('updates_log.txt'):
        updatesLogFile = open('updates_log.txt','w')
        updatesLogFile.close()
    #starting trace
    while True:
        #updates handle
        try:
            updatesLogFile = open('updates_log.txt','r+')
            updates_id = set(updatesLogFile.read().splitlines())
            updates_answer = requests.get(TELEGRAM_URL_CHECK.replace('BOT_TOKEN', t_token)).json()
            for upd in updates_answer['result']:
                if str(upd['update_id']) not in updates_id:
                    if 'message' in upd:
                        tmp_key = 'message'
                    elif 'channel_post' in upd:
                        tmp_key = 'channel_post'
                    else:
                        continue
                    bot_action(upd[tmp_key]['text'], upd[tmp_key]['chat']['id'])
                    updates_id.add(str(upd['update_id']))
                    updatesLogFile.write('{}\n'.format(upd['update_id']))
            updatesLogFile.close()
            #trace forum
            logFile = open('log.txt','r+')
            posts_id = set(logFile.read().splitlines())
            posts = get_list_of_posts(BASE_URL+FORUM)
            posts = filter_out(posts, 'палки')

            for example in posts[::-1]:
                unique_id = '{}_{}'.format(example['local_url'], example['date'])
                if unique_id not in posts_id:
                    requests.get(TELEGRAM_URL.replace('BOT_TOKEN', t_token), params = {'chat_id': channel, 
                                   'text': example['text']+'\n'+'{}{}'.format(BASE_URL,example['local_url'])})
                    posts_id.add(unique_id)
                    logFile.write('{}\n'.format(unique_id))
            logFile.close()
        except Exception as e:
            logging.info(str(e))
        time.sleep(300)

if __name__ == '__main__':
    main()

