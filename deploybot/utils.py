import requests
import os
import sys

import contextlib

from constants import SLACK_WEBHOOK_URL, SLACK_TOKEN


if sys.version_info[0] < 3:
    @contextlib.contextmanager
    def redirect_stdout(target):
        original = sys.stdout
        sys.stdout = target
        yield
        sys.stdout = original
else:
    redirect_stdout = contextlib.redirect_stdout

terminal = sys.stdout


class CustomIO():
    def __init__(self):
        self.messages = []

    def write(self, message):
        terminal.write(message)
        self.messages.append(message)

    def getvalue(self):
        return ''.join(self.messages)

    def flush(self):
        pass


class SlackPost():
    def __init__(self, message, channel='opsys-updates', base_msg=''):
        self.channel = channel
        self.slack_user = os.environ.get('SLACKHANDLE')
        self.base_msg = base_msg
        self._post_to_slack(message)

    def post(self, url, payload):
        """ Helper function to make requests to slack """
        response = requests.post(SLACK_WEBHOOK_URL + url, data=payload)
        response.raise_for_status()
        return response.json()

    def _post_to_slack(self, message):
        """ Post a message to slack, this is called when this class is instantiated """
        payload = {
            'token': SLACK_TOKEN,
            'channel': self.channel,
            'text': self.base_msg + message,
            'icon_emoji': ':robot:',
            'pretty': True
        }
        response = self.post('chat.postMessage', payload)
        self.channel = response['channel']
        self.ts = response['ts']

    def update(self, message):
        """ Update message text """
        payload = {
            'token': SLACK_TOKEN,
            'channel': self.channel,
            'text': self.base_msg + message,
            'icon_emoji': ':robot:',
            'ts': self.ts,
            'pretty': True
        }
        self.post('chat.update', payload)

    @contextlib.contextmanager
    def threading(self):
        """ when used as a context manager, commands run will output to the message thread instead of stdout

            Usage example:
            msg = SlackPost("hi")
            with msg.threading():
                do_something()
        """
        f = CustomIO()
        with redirect_stdout(f):
            yield
        self.thread(f.getvalue())

    def thread(self, message, mention=False):
        """ Create a threaded message on this post

            If mention is true, this function will attempt to mention the slack user defined by the env var SLACKHANDLE
        """
        text = message
        if mention:
            if self.slack_user:
                text += ' <@{}>'.format(self.slack_user)
            else:
                # If you're using mention I assume you don't want this thread unless a slack_user is defined.
                return
        payload = {
            'token': SLACK_TOKEN,
            'channel': self.channel,
            'text': text,
            'icon_emoji': ':robot:',
            'thread_ts': self.ts,
            'pretty': True
        }
        self.post('chat.postMessage', payload)

    def react(self, emoji):
        """ React to this post """
        payload = {
            'token': SLACK_TOKEN,
            'channel': self.channel,
            'name': emoji,
            'timestamp': self.ts,
        }
        self.post('reactions.add', payload)

    def unreact(self, emoji):
        """ Remove a reaction on this post """
        payload = {
            'token': SLACK_TOKEN,
            'channel': self.channel,
            'name': emoji,
            'timestamp': self.ts,
        }
        self.post('reactions.remove', payload)
