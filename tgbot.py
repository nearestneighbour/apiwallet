import requests
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.delegate import pave_event_space, per_chat_id, create_open
import time
import os.path

class tgbot(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(tgbot, self).__init__(*args, **kwargs)
        self.chid = None
        self.wallet = None

    def showchoice(self):
        keyboard = ReplyKeyboardMarkup(keyboard=[
                   [KeyboardButton(text='Get total BTC')],
                   [KeyboardButton(text='Get total EUR')],
                   [KeyboardButton(text='Get total USD')]])
        self.sender.sendMessage('Get balance', reply_markup=keyboard)

    def on_chat_message(self, msg):
        content_type, chat_type, self.chid = telepot.glance(msg)
        self.chid = str(self.chid)
        if content_type == 'file':

        if self.wallet == None and os.path.isfile('data/'+self.chid):
            with open('data/'+self.chid) as f:
                self.wallet = wallet.load(f)
        if content_type=='location':
            self.location = str(msg['location']['latitude'])+','+str(msg['location']['longitude'])
            print('Got location as object: '+self.location)
            self.showchoice()
        else:
            if self.location!='':
                if msg['text']=='Temperatuur':
                    data = getweather(self.location)
                    print('Temperature button')
                    self.sender.sendMessage('Temperatuur: '+data['temp']+' C')
            else:
                self.location = msg['text']
                print('Set location to '+self.location)
                self.showchoice()


    def on_close(self, dd):
        with open('data/'+self.chid,'wb') as f:
            self.wallet.save(f)

with open('data/token') as f:
    token = f.read()[:-1]

bot = telepot.DelegatorBot(token, [
    pave_event_space()(
        per_chat_id(), create_open, weatherguy, timeout=10
    ),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')
while 1:
    time.sleep(10)
