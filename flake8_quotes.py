__author__ = 'Javier Domingo Cansino <javierdo1@gmail.com>'
__version__ = '0.0.1'

import ast

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(asctime)s %(message)s')
logger = logging.getLogger()

DQ = '"'
SQ = '\''


class StringChecker(ast.NodeVisitor):
    def visit_Module(self, node):
        self.strings = list()
        self.generic_visit(node)

    def visit_Str(self, node):
        self.strings.append(node)


def error(code, msg, *args, **kw):
    assert len(code) == 4
    if args:
        if kw:
            raise TypeError(
                "You may give positional or keyword arguments, not both")
    args = args or kw
    return (code + ' ' + msg) % args


def error_single_quotes(string):
    return error('Q100', 'String should be defined with single quotes: %s',
                 string)


class QuotesChecker(object):
    '''String literals checker tool'''
    name = 'flake8-quotes'
    version = __version__

    def __init__(self, tree, filename, *args, **kwargs):
        self.tree = tree
        self.filename = filename
        with open(filename) as f:
            self.lines = f.readlines()
            f.seek(0)
            self.raw_text = f.read()

    def return_all_strings(self):
        '''Returns all the strings in the file using the ast'''
        s = StringChecker()
        s.visit(self.tree)
        for string in s.strings:
            yield string.lineno, string.col_offset, string.s

    def return_single_quote(self, lineidx, colno):
        quote_type = self.lines[lineidx][colno]
        line = self.lines[lineidx][colno:]
        if quote_type * 3 == line[:2]:
            pass  # TODO: Have to implement multiline quotes
        escaped = True  # We suppose the first is escaped to avoid extra logic
        is_raw = False
        if colno > 0 and self.lines[lineidx][colno - 1].lower() == 'r':
            is_raw = True
        for i, char in enumerate(line):
            if char == quote_type and not escaped:
                i += 1
                break
            if char == '\\' and not is_raw:
                escaped = True
                continue
            escaped = False
        return line[:i]

    def return_quote(self, lineno, colno, string):
        '''Classify string and run it's quote extractor'''
        if colno == -1:
            logger.error('Docstrings not implemented: %d:%d %s',
                         lineno, colno, repr(string))
            return  # TODO: Docstring
        simple_quote = self.return_single_quote(lineno - 1, colno)
        try:
            m = ast.parse(simple_quote)
        except SyntaxError:
            logger.error('Parsing error, does it have correct syntax?:'
                         ' %d:%d %s => %s', lineno, colno, repr(string),
                         simple_quote)
            return  # TODO: Know when this can happen
        s = StringChecker()
        s.visit(m)
        assert len(s.strings) == 1
        parsed_string = next(iter(s.strings)).s
        if parsed_string == string:
            yield lineno, colno, simple_quote
            return
        # TODO: Multiline string
        logger.error(
            'Expanding multiple lines not implemented: %d:%d %s => %s',
            lineno, colno, repr(string), simple_quote
        )

    def check_quote(self, line, col, quote):
        if quote.startswith(DQ):
            if not SQ in quote:
                return error_single_quotes(quote)

    def run(self):
        for line, colno, string in self.return_all_strings():
            for line_s, col_s, quote in self.return_quote(line, colno, string):
                error = self.check_quote(line_s, col_s, quote)
                if error:
                    yield (line_s, col_s, error, type(self))
