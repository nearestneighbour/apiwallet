import requests
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.delegate import pave_event_space, per_chat_id, create_open
import time
import os.path
from wallet import wallet

class tgbot(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(tgbot, self).__init__(*args, **kwargs)
        self.chid = None
        self.w = None
    def showchoice(self):
        keyboard = ReplyKeyboardMarkup(keyboard=[
                   [KeyboardButton(text='Get total BTC')],
                   [KeyboardButton(text='Get total EUR')],
                   [KeyboardButton(text='Get total USD')]])
        self.sender.sendMessage('Get balance', reply_markup=keyboard)

    def on_chat_message(self, msg):
        content_type, chat_type, self.chid = telepot.glance(msg)
        self.chid = str(self.chid)
        if self.w == None:
            if os.path.isfile('mywallet'):
                self.w = wallet.load('mywallet')
                #self.sender.sendMessage("Type 'get' for wallet balance.")
            else:
                self.sender.sendMessage('No wallet available.')
        if msg['text']=='get':
            print('showchoice')
            self.showchoice()
        #if content_type=='location':
        #    self.location = str(msg['location']['latitude'])+','+str(msg['location']['longitude'])
        #    print('Got location as object: '+self.location)
        #else:
        elif msg['text']=='Get total BTC':
                print('BTC')
                self.sender.sendMessage(str(self.w.total_btc()))
        elif msg['text']=='Get total EUR':
                print('EUR')
                self.sender.sendMessage(str(self.w.total_eur()))
        elif msg['text']=='Get total USD':
                print('USD')
                self.sender.sendMessage(str(self.w.total_usd()))
    def on_close(self, dd):
        pass

with open('keys/tgtoken') as f:
    token = f.read()[:-1]
bot = telepot.DelegatorBot(token, [
    pave_event_space()(
        per_chat_id(), create_open, tgbot, timeout=10
    ),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')
while 1:
    time.sleep(10)
