'''
What does this do?
recieves some atributes that every item will have
use_function, targeting, targeting_message, function_kwargs.
What are these kwargs?
'''

class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs