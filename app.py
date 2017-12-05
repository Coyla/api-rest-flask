from flask import Flask, render_template, request, jsonify
import atexit
import json
from cloudant import Cloudant
from chatterbot import ChatBot
import cf_deployment_tracker
import os
import logging


cf_deployment_tracker.track()

app = Flask(__name__)

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
#port = os.getenv('VCAP_APP_PORT', '5000')


#Chatbot loading
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
@app.route("/<content>")
def message(content):
	response = 'User said : ' + content

	print(response)
	print('session ',bot.default_session.id_string)
	bot_response = 'bot said : ' + bot.get_response(content).text
	return bot_response

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=True)
