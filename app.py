from flask import Flask,request,jsonify
from chatterbot import ChatBot
import os
import logging

app = Flask(__name__)
port = int(os.getenv('VCAP_APP_PORT', '8000'))

#Chatbot load
logging.basicConfig(level=logging.INFO)
def debug(message):
	print("[debug] : %s" %(message))

bot = ChatBot(
	'Poc Bot',
	logic_adapters=[{
            'import_path': 'chatterbot.logic.BestMatch'}
	,{
		'import_path': 'acronym_logic_adapter.AcronymLogicAdapter'
	},
	{
		'import_path': 'greeting_logic_adapter.GreetingLogicAdapter'
	},
	{
		'import_path': 'chatterbot.logic.LowConfidenceAdapter',
		'threshold': 0.75,
		'default_response': 'Acronym not found'
	}],
	trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

bot.train('data/acronyms/acronyms.yml')
#Changement type de training de corpus vers listrainer
debug("chatterbot is running  ...")

#desactivation d'apprentissage automatique
bot.read_only = True
@app.route('/message',methods=['POST'])
def post_message():
	request_response = request.get_json(force=True,silent=True)
	content = request_response['content'] #message from user
	print('session ',bot.default_session.id_string)
	response_dict = {'message': bot.get_response(content).text }
	return jsonify(response_dict)

@app.route('/message',methods=['GET'])
def get_message():
	response_dict = {'message': bot.get_response('ITG').text }
	response_json = jsonify(response_dict)
	print(type(response_json))
	return response_json

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=True)

