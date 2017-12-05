# -*- coding: utf-8 -*-
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

class GreetingLogicAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(GreetingLogicAdapter, self).__init__(**kwargs)

    def can_process(self, statement):
        if statement.text.startswith('greetings'):
            return True
        else:
            return False

    def process(self, statement):
        import random

        # Randomly select a confidence between 0 and 1
        #confidence = random.uniform(0, 1)


        # For this example, we will just return the input as output
        selected_statement = Statement('Hello user ! ')
        print('greetings_adapter ----')
        print('selected_statement.confidence')
        return selected_statement