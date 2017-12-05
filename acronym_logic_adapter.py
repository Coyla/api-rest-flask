# -*- coding: utf-8 -*-
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

class AcronymLogicAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(AcronymLogicAdapter, self).__init__(**kwargs)


    def can_process(self, statement):
		return False

    def process(self, statement):
        import random
        import chatterbot.response_selection
        # Randomly select a confidence between 0 and 1
        return_message = 'hello'
        confidence = random.uniform(0, 1)

        acronyms = self.normalize(statement).split()

        # For this example, we will just return the input as output
        selected_statement = Statement(return_message)
        selected_statement.confidence = confidence
        print('acronyms_adapter  ----')
        print(selected_statement.confidence)

        return selected_statement
    def normalize(self, statement):
	    message = statement.text.lower()
	    return message