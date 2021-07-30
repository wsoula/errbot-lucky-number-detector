from errbot import BotPlugin, botcmd, arg_botcmd, re_botcmd
import re

lucky_numbers = [77777977, 777797777, 7777777797777]
minimum_numbers = 4


class Luckynumberdetector(BotPlugin):
    """Detects responses where the numbers add up to the lucky number(s)"""
    def callback_message(self, mess):
        """Runs on every message"""
        match = re.findall('[0-9]+', mess.body)
        reply = ''
        total = 0
        count = 0
        for item in match:
            reply = reply + item + ' + '
            total = total + int(item)
            count = count + 1
        reply = reply[:-1]
        reply = reply + ' = ' + str(total)
        match = [int(i) for i in match]
        if sum(match) in lucky_numbers and count >= minimum_numbers:
            self.send_card(
                  in_reply_to=mess,
                  body=reply,
                  title='The numbers in your message add up to the lucky number: ' + str(total)
              )

    @botcmd()
    def luckynumber(self, msg, args):
        return str(lucky_numbers) + ' in ' + str(minimum_numbers) + ' numbers'
