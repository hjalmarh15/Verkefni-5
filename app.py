import json
from flask import Flask, render_template, request, jsonify, make_response
import urllib.request as ur
import difflib
import random

from klasar import Game, Player

app = Flask(__name__)

game = Game()

@app.route('/')
def main():  # Render'ar main menu
    return render_template('mainMenu.html')


@app.route('/newGame')
def new_game():  # Render'ar html til að búa til nýjan leik
    return render_template('newGame.html')


@app.route('/playAgain')
def playAgain():    # Byrjar nýjan leik með sömu stillingum
    game = Game()
    return json.dumps(True)


@app.route('/game')
def play():  # Render'ar leiknum
    return render_template('index.html')


@app.route('/final')
def final_result():  # Render'ar úrslitum leiks
    return render_template('final.html')


@app.route('/scoreBoard')
def score_board():  # Sækja stigaskor leikmanna í lok leik
    dic = {}
    for player in game.players:
        dic[str(player.id)] = [player.name, player.score, player.id]
    return jsonify(**dic)


@app.route('/getPlayerName')
def get_current_name():  # Sækja þann leikmann sem á að gera að hverju sinni
    pl = game.players[game.current]
    return json.dumps(pl.name)


@app.route('/getScoreBoard')
def get_score():  # Sækja stigaskor leikmanna
    tableOfPlayers = []
    for player in game.players:
        temp = [str(player.name), str(player.score)]
        tableOfPlayers.append(temp)
    return jsonify(tableOfPlayers)


@app.route('/getRandomQuestion')
def get_random_question():  # Sækja random spurningu frá Jservice
    request = 'http://jservice.io/api/random?count=10'
    response = ur.urlopen(request).read()
    data = json.loads(response.decode('utf-8'))[0]
    return json.dumps(data)


@app.route('/getCategories')
def get_categories():  # Sækja random categoríur frá Jservice í byrjun leiks
    if game.categories == '':
        offset = random.uniform(0, 15000)
        request = 'http://jservice.io/api/categories?count=5&offset=' + str(offset)
        response = ur.urlopen(request).read()
        data = json.loads(response.decode('utf-8'))
        game.categories = data
    else:
        data = game.categories

    return json.dumps(data)


@app.route('/getCategory', methods=['GET'])
def get_category():
    global game     # Sækja category frá ID
    category_id = request.args.get('data')
    url = 'http://jservice.io/api/category?id=' + str(category_id)
    response = ur.urlopen(url).read()
    data = json.loads(response.decode('utf-8'))
    game.category = data
    return json.dumps(data)


@app.route('/getPlayers', methods=['POST', 'GET'])
def get_player_names():     # Sækja nöfn leikmanna sem gefin voru af notanda
    num = len(request.form)
    lstOfPLayers = []
    for i in range(1, num + 1):
        tempPlayer = Player()
        playerInfo = request.form['Player' + str(i)]
        tempPlayer.id = i
        tempPlayer.name = playerInfo
        lstOfPLayers.append(tempPlayer)
    game.players = lstOfPLayers
    for player in game.players:
        print(player.name, player.id, player.score)
    return render_template('index.html')


@app.route('/submitAnswer', methods=['POST', 'GET'])
def submit_answer():        # Taka á móti svari notanda og verify'a hvort það sé rétt
    dic = {}
    dic['answer'] = request.args.get('answer')
    ID = request.args.get('id')
    qNa = get_question_and_answer(ID)
    dic['correctAnswer'] = sanitize(str(qNa[1]))
    dic['question'] = qNa[0]
    value = qNa[2]
    if correct(str(dic['answer']), str(dic['correctAnswer'])):
        dic['result'] = True
        game.players[game.current].score += int(value)

    else:
        dic['result'] = False
        game.players[game.current].score -= int(value)

    return jsonify(**dic)


@app.route('/updateGame', methods=['GET'])
def update_game():      # Uppfæra stöðu leiks
    if game.current == len(game.players) - 1:
        game.current = 0
        game.turn += 1
        if game.turn >= 5:
            return json.dumps(True)
        else:
            return json.dumps(False)
    else:
        game.current += 1
        return json.dumps(False)


def sanitize(theString):    # Hreinsa svar
    print(theString)
    theString.replace('<i>', '')
    theString.replace('</i>', '')
    return theString


def get_question_and_answer(ID):    # Sækja spurningu og svar frá ID
    global game
    cat = game.category['clues']
    for i in range(len(cat)):
        if str(ID) == str(cat[i]['id']):
            q = cat[i]['question']
            a = cat[i]['answer']
            v = cat[i]['value']
            break
    return (q, a, v)


def correct(answer, rightAnswer):    # Verify'a hvort svar notanda var nægilega rétt
    if answer.lower() == rightAnswer.lower():
        return True
    compare = difflib.SequenceMatcher(None, answer.lower(), rightAnswer.lower())
    ratio = compare.ratio()
    if ratio >= 0.8:
        return True

    return False


if __name__ == "__main__":
    app.run()
