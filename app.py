import json
from flask import Flask, render_template, request, jsonify
import urllib.request as ur
from klasar import Game, Player

app = Flask(__name__)
categoryOffset = 0


game = Game()

@app.route('/')
def main():
    return render_template('mainMenu.html')


@app.route('/newGame')
def newGame():
    return render_template('newGame.html')


@app.route('/highScores')
def highScores():
    return render_template('highScores.html')


@app.route('/game')
def game():
    return render_template('index.html')


@app.route('/getRandomQuestion')
def get_random_question():
    request = 'http://jservice.io/api/random?count=10'
    response = ur.urlopen(request).read()
    data = json.loads(response.decode('utf-8'))[0]
    return json.dumps(data)


@app.route('/getCategories')
def get_categories():
    global categoryOffset
    request = 'http://jservice.io/api/categories?count=3&offset=' + str(categoryOffset)
    categoryOffset += 3
    response = ur.urlopen(request).read()
    data = json.loads(response.decode('utf-8'))
    return json.dumps(data)
    get_category(category_id)


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
    return json.dumps(len(request.form))
    lstOfPLayers = []
    for i in range(1, num):
        tempPlayer = Player()
        playerInfo = request.form['Player' + str(i)]
        tempPlayer.id = i
        tempPlayer.name = playerInfo
        lstOfPLayers.append(tempPlayer)
    toplel = Game(lstOfPLayers)
    return json.dumps({'success': True})



@app.route('/submitAnswer', methods=['POST', 'GET'])
def submit_answer():
	dic = {}
	dic['answer'] = request.args.get('answer')
	ID = request.args.get('id')
	qNa = get_question_and_answer(ID)
	dic['correctAnswer'] = sanitize(qNa[1])
	dic['question'] = qNa[0]
	value = qNa[2]
	if str(dic['answer']) == str(dic['correctAnswer']):
		dic['result'] = True
	else:
		dic['result'] = False
	return jsonify(**dic)



def sanitize(theString):
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

if __name__ == "__main__":
    app.run()
