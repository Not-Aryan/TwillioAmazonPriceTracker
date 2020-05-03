import requests
import os
from bs4 import BeautifulSoup
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask import Flask, request, session
import time

app = Flask("Amazon-Twillio Price Tracker")
app.config['SECRET_KEY'] = os.urandom(24)

def get_info(URL):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
    amazon = [{'id':'productTitle'}
              {'price':'productTitle'}]
    
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id="").get_text()
    title = title.strip()
    curr = soup.find(id="priceblock_ourprice").get_text()
    return title, curr


@app.route('/price', methods=['POST'])
def price():
    incoming_msg = request.values.get('Body', '').lower()
    uinput = session.get('uinput', [])
    uinput.append(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    counter = session.get('counter', 0)
    counter += 1
    ask = 0
    r = ""
    session['counter'] = counter
    if (session['counter'] == 1):
        session['uinput'] = uinput
    if (session['counter']==2):
        ask = session['uinput'][1]
        print("THIS IS THIS USER INPUT", ask)
        URL = session['uinput'][0]
        title, curr = get_info(URL)
        curr_price = curr[1:]
        print(title)
        print(curr)
        r = "Got it. Will inform when the price is right!"
        # msg.body(r)
        # return str(resp)
        while (curr_price > ask):
            title, curr = get_info(URL)
            curr_price = curr[1:]
            time.sleep(60*60*24)
        r = "Hey, your product's price has fallen! Check it out: " + URL

    msg.body(r)
    return str(resp)


if __name__ == '__main__':
    app.run()





