"""Detects lucky numbers"""
import os
import re
from errbot import BotPlugin, botcmd

DEFAULT_LUCKY_NUMBERS = '77777977,777797777,777'
DEFAULT_MINIMUM_NUMBERS = '4'
DEFAULT_PREFIX_TO_MONITOR = '!'


class Luckynumberdetector(BotPlugin):
    """Detects responses where the numbers add up to the lucky number(s)"""
    def callback_message(self, mess):
        """Runs on every message"""
        env_lucky_numbers = os.getenv('lucky_numbers', DEFAULT_LUCKY_NUMBERS).split(',')
        map_lucky_numbers = map(int, env_lucky_numbers)
        lucky_numbers = list(map_lucky_numbers)
        minimum_numbers = int(os.getenv('minimum_numbers', DEFAULT_MINIMUM_NUMBERS))
        match = re.findall('[0-9]+', mess.body)
        reply = ''
        total = 0
        count = 0
        for item in match:
            reply = reply + item + ' + '
            total = total + int(item)
            count = count + 1
        reply = reply[:-3]
        reply = reply + ' = ' + str(total)
        match = [int(i) for i in match]
        if sum(match) in lucky_numbers and count >= minimum_numbers:
            prefix_to_monitor = os.getenv('prefix_to_monitor', DEFAULT_PREFIX_TO_MONITOR)
            prefix = os.getenv('BOT_PREFIX', '!')
            if prefix == prefix_to_monitor:
                self.send_card(in_reply_to=mess, body=reply,
                               title='The numbers in your message add up to the lucky number: ' + str(total))

    @botcmd()
    def luckynumber(self, msg, args):
        """ Return what the luck number is """
        self.log.info('msg=%s args=%s', msg, args)
        lucky_numbers = os.getenv('lucky_numbers', DEFAULT_LUCKY_NUMBERS).split(',')
        minimum_numbers = int(os.getenv('minimum_numbers', DEFAULT_MINIMUM_NUMBERS))
        return str(lucky_numbers) + ' in a minimum of ' + str(minimum_numbers) + ' numbers'
