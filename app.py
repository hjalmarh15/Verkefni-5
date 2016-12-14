
import json
from flask import Flask, render_template, request
import urllib.request as ur

app = Flask(__name__)


@app.route('/')
def main():
	return render_template('mainMenu.html')

@app.route('/newGame')
def newGame():
	return render_template('index.html')

@app.route('/highScores')
def highScores():
	return render_template('highScores.html')

@app.route('/quitGame')
def quitGame():
	return render_template('highScores.html')
'''
def main():
	question = get_random_question()
	id = question['category']['id']
	category = get_category(id)['title']
	print('The category is: ' + category)
	print(question['question'])	
	userAnswer = input('Your answer: ')
	theAnswer = sanitize(question['answer']).lower()
	if userAnswer.lower() == theAnswer:
		print('Correct!!')
	else:
		print('Incorrect :(')
		print('The answer is:', question['answer'])
'''

@app.route('/getRandomQuestion')
def get_random_question():
	request = 'http://jservice.io/api/random?count=10'
	response = ur.urlopen(request).read()
	data = json.loads(response.decode('utf-8'))[0]
	return json.dumps(data)



@app.route('/getCategories')
def get_categories():
	request = 'http://jservice.io/api/categories?count=3&offset=20'

	response = ur.urlopen(request).read()
	data = json.loads(response.decode('utf-8'))
	return json.dumps(data)
	get_category(category_id)


@app.route('/getCategory', methods=['GET'])
def get_category():
	category_id = request.args.get('data')
	url = 'http://jservice.io/api/category?id=' + str(category_id) 
	response = ur.urlopen(url).read()
	data = json.loads(response.decode('utf-8'))
	return json.dumps(data)


def sanitize(theString):
	theString.replace('<i>', '')
	theString.replace('</i>', '')
	return theString


if __name__ == "__main__":
	app.run()