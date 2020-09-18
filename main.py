import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True
dict_raw= open("en_dict.csv")
dict_text = dict_raw.readlines()

def en_2_cz(query):
    # sign by sign difference
    def hum_distance(a,b):
        dst = 0
        if(len(a) > len(b)):
            dst += len(a) - len(b)
            a = a[:len(b)]
        if(len(b) > len(a)):
            dst  += len(b) - len(a)
        for i in range(len(a)):
            if(a[i] != b[i]):
                dst += 1
        return dst

    def byHum(elem):
        return elem[1]

    def binary_search(arr, num, start, end):
        if start == end:
            if arr[start][2] > num:
                return start
            else:
                return start+1

        if start > end:
            return start

        mid = (start + end) // 2
        if arr[mid][2] < num:
            return binary_search(arr, num, mid+1, end)
        elif arr[mid][2] > num:
            return binary_search(arr, num, start, mid-1)
        else:
            return mid

    def binary_insert(possible_words, val):
        i = len(possible_words) - 1
        j = binary_search(possible_words, val[2], 0, i) 
        possible_words = possible_words[:j] + [val] + possible_words[j:i] + possible_words[i+1:] 
        return possible_words

    def stack_possible_words(possible_words, val):
        if(len(possible_words) < 300):
            return binary_insert(possible_words, val)
        else:
            if(possible_words[-1][2] > val[2]):
                possible_words = binary_insert(possible_words, val)
            return possible_words
            
    # max 30 elements

    possible_words = [] 
    pos = []
    for x in dict_text:
        word = x.split(";")
        en = word[0]
        cs = word[1]
        hum_dis = hum_distance(en, query)
        if(hum_dis > len(en)/2):
            continue
        val = [en, cs, hum_dis]
        if(len(possible_words) == 0):
            possible_words.append(val)
        possible_words  = stack_possible_words(possible_words, val)

    return possible_words
@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('./index.html')


@app.route('/api/en2cz/<word>', methods=['GET'])
def translate_to_cz(word):
    return jsonify(en_2_cz(word))

app.run()
