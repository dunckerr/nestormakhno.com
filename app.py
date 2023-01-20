#https://twdown.net/?error=nolink
#https://cloudconvert.com/mov-to-mp4
from flask import Flask, render_template, request

import os
import sys
import logging
import re

# https://twdown.net/download.php

WORDLEN = 5

if sys.platform == 'win32':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path='/home/x1lcedpr5zdi/WebSite1')

app.debug = True

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# copy vars for global website
_disallowed = set()
_mask = '.....'
global _word5
_word5 = list()

def set_2_regex(s):
    r = '[^'
    for c in s:
        r = r + c
    r = r + ']'
    return r

def dk_input(prompt, default, maxlen):

    while True:
        logger.warning(prompt)
        r = input(prompt+'('+default+'):')
        if default is not None and r == '':
            return default
        elif len(r) == maxlen:
            return r
        else:
            pass

def gen_possibles(mask, nots):
    #print("got args mask {mask} nots {nots}")
    if len(nots) == 0:
        nots_bracket = "."
    else:
        nots_bracket = "[^"+nots+"]"
    newmask = ""
    for i in range(0,5):
        # TODO blank entry in form needs to be nadled here
        #print(f"processing {i} {mask} len {len(mask)}")
        if mask[i] == ".":
            newmask += nots_bracket
        else:
            newmask += mask[i]

    print("generated mask"+newmask)
    r = re.compile('^' + newmask + '$')
    fp = open('EN-UNIX-99171', 'r')
    wtmp = fp.read()
    words = wtmp.split('\n')
    word5 = list(filter(r.match, words))
    print('words list len '+str(len(words)))
    print('possibles list len '+str(len(word5)))

    return word5


def main_test():
    mask = '.....'
    r = re.compile('^'+mask+'$')
    fp = open('EN-UNIX-99171', 'r')
    wtmp = fp.read()
    words = wtmp.split('\n')
    word5 = list(filter(r.match, words))
    logger.warning('words list len '+str(len(words)))
    logger.warning(str(WORDLEN)+' letter words '+str(len(word5)))

    # these will come from url
    disallowed = set()
    while True:
        logger.warning('current mask '+mask)
        logger.warning('disallowed '+disallowed)

        mask = dk_input('mask:', mask, WORDLEN)
        ch = dk_input('bad char:', None, 1)
        disallowed.add(ch)

        # now were in business we have regex mask and disallowed
        # generate a regex
        r2 = '^'
        for i in range(0, 5):
            if mask[i] == '.':
                r2 = r2 + set_2_regex(disallowed)
            else:
                r2 = r2 + mask[i]

        r2 = r2 +'$'
        logger.warning('made regex '+r2)

        r3 = re.compile(r2)
        poss = list(filter(r3.match, word5))
        logger.warning('possibilities '+str(len(poss))+poss[0] + ' ' + poss[1])

def _init():
    _mask = '[A-Za-z][A-Za-z][A-Za-z][A-Za-z][A-Za-z]'
    r = re.compile('^'+_mask+'$')
    fp = open('EN-UNIX-99171', 'r')
    wtmp = fp.read()
    words = wtmp.split('\n')
    global _word5
    _word5 = list(filter(r.match, words))
    return '<H3>' + str(len(_word5)) + '</H3>'


HELP = '<H1>HELP v1.1<p>CASE SENSITIVE DICT. /words word count<p>/str 1par<p>/str/str mask/allowed<p>/init initialise words</H1>'

def dkrender(html, img):
    if sys.platform == 'win32':
        return render_template(html, user_image=img, path="\\static\\")
    else:
        return render_template(html, user_image=img, path="/home/x1lcedpr5zdi/WebSite1/")


@app.route("/zz1")
def show_indexz1():
    return dkrender("index.html", "IMG_0021.jpg")

@app.route("/zz2")
def show_indexz2():
    return dkrender("index2.html", "IMG_0021.jpg")

@app.route("/zz3")
def show_indexz3():
    return dkrender("zz3.html", "IMG_0021.jpg")

@app.route("/cat")
def show_cat():
    return dkrender("cat.html", "IMG_1820.mp4")


# use to get info to user from godaddy
@app.route("/pwd")
def show_index2():
    return os.getcwd()

@app.route("/")
def hello():
    return dkrender("main.html", "pic1.png")

@app.route("/words")
def test():
    global _word5
    return '<H2>len words ' + str(len(_word5)) + '</H2>'

@app.route("/session")
def test_session():
    global _word5
    return 'len session[words] ' + str(len(_word5))

@app.route("/init")
def init():
    #app.logger.error('app logging init called')
    return _init()


#@app.route("/<string:name>/")
#def say_hello(name):
    #return 'called with ' +name


@app.route("/<string:mask>/<string:disallowed>")
def say_hello2(mask, disallowed):
    # now were in business we have regex mask and disallowed
    # generate a regex
    r2 = '^'
    for i in range(0, WORDLEN):
        if mask[i] == '.':
            r2 = r2 + set_2_regex(disallowed)
        else:
            r2 = r2 + mask[i]

    r2 = r2 + '$'

    r3 = re.compile(r2)
    poss = list(filter(r3.match, _word5))
    #if len(poss) < 30:
    return '<H3>' + str(poss[0: min(100, len(poss))]) + '</H3>'
    #else:
        #return '<H3>' + str(len(poss))+'/'+str(len(_word5)) + '</H3>'

#################  new ###################
@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return "The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        #calling render with ImmutableMultiDict([('c1', 'r'), ('c2', 'a'), ('c3', 'm')])
        poss = gen_possibles(form_data['c1']+ form_data['c2']+ form_data['c3']+ form_data['c4']+ form_data['c5'], form_data['nn'])
        #print(f'got possibles {poss}')
        #print(f'calling render with {form_data}')
        return render_template('data.html', form_data=form_data, words=poss)

if __name__ == "__main__":
    app.run()
