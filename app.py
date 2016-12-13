
import json
from flask import Flask, render_template
import urllib.request as ur

app = Flask(__name__)


@app.route('/')
def main():
	return render_template('index.html')
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

def get_categories():
	request = 'http://jservice.io/api/categories?count=5&offset=10'

	response = ur.urlopen(request).read()
	data = json.loads(response.decode('utf-8'))
	return data
	get_category(category_id)

def get_category(category_id):
	request = 'http://jservice.io/api/category?id=' + str(category_id) 
	response = ur.urlopen(request).read()
	data = json.loads(response.decode('utf-8'))
	return data


def sanitize(theString):
	theString.replace('<i>', '')
	theString.replace('</i>', '')
	return theString


if __name__ == "__main__":
	app.run()