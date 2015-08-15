__author__ = 'Javier Domingo Cansino <javierdo1@gmail.com>'
__version__ = '0.0.1'

import ast


class QuotesChecker(object):
    '''String literals checker tool'''
    name = 'flake8-quotes'
    version = __version__

    def __init__(self, tree, *args, **kwargs):
        self.tree = tree
        print(args, kwargs)

    def run(self):
        print(ast.dump(self.tree))
        return []
