import json
from flask import Flask, render_template, request, jsonify, make_response
import urllib.request as ur
import difflib
import random


from klasar import Game, Player

app = Flask(__name__)

game = Game()


@app.route('/')
def main():
    return render_template('mainMenu.html')


@app.route('/newGame')
def newGame():
    return render_template('newGame.html')


@app.route('/highScores')
def highScores():
    return render_template('highScore.html')


@app.route('/game')
def play():
    return render_template('index.html')

@app.route('/final')
def finalResult():
    return render_template('final.html')

@app.route('/scoreBoard')
def scoreBoard():
    dic = {}
    for player in game.players:
        dic[str(player.id)] = [player.name, player.score, player.id]
    return jsonify(**dic)

@app.route('/getPlayerName')
def getCurrentName():
    pl = game.players[game.current]
    return json.dumps(pl.name)


@app.route('/getScoreBoard')
def get_score():
    tableOfPlayers = []
    for player in game.players:
        temp = [str(player.name), str(player.score)]
        tableOfPlayers.append(temp)
    return jsonify(tableOfPlayers)


@app.route('/getRandomQuestion')
def get_random_question():
    request = 'http://jservice.io/api/random?count=10'
    response = ur.urlopen(request).read()
    data = json.loads(response.decode('utf-8'))[0]
    return json.dumps(data)


@app.route('/getCategories')
def get_categories():
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
    global game
    category_id = request.args.get('data')
    url = 'http://jservice.io/api/category?id=' + str(category_id)
    response = ur.urlopen(url).read()
    data = json.loads(response.decode('utf-8'))
    game.category = data
    return json.dumps(data)


@app.route('/getPlayers', methods=['POST', 'GET'])
def get_player_names():
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
def submit_answer():
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
def update_game():
    if game.current == len(game.players)-1:
        game.current = 0
        game.turn += 1
        if game.turn >= 5:
            return json.dumps(True)
        else:
            return json.dumps(False)
    else:
        game.current += 1
        return json.dumps(False)

def sanitize(theString):
    print(theString)
    theString.replace('<i>', '')
    theString.replace('</i>', '')
    return theString


def get_question_and_answer(ID):
    global game
    cat = game.category['clues']
    for i in range(len(cat)):
        if str(ID) == str(cat[i]['id']):
            q = cat[i]['question']
            a = cat[i]['answer']
            v = cat[i]['value']
            break
    return (q, a, v)


def correct(answer, rightAnswer):
    if answer.lower() == rightAnswer.lower():
        return True
    compare = difflib.SequenceMatcher(None, answer.lower(), rightAnswer.lower())
    ratio = compare.ratio()
    if ratio >= 0.8:
        return True

    return False


if __name__ == "__main__":
    app.run()
