__author__ = 'Javier Domingo Cansino <javierdo1@gmail.com>'
__version__ = '0.0.1'

import ast
import logging
from functools import partial

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(asctime)s %(message)s')
logger = logging.getLogger()

DQ = '"'
SQ = "'"


class StringChecker(ast.NodeVisitor):
    def visit_Module(self, node):  # noqa
        self.strings = list()
        self.generic_visit(node)

    def visit_Str(self, node):  # noqa
        self.strings.append(node)

def quote_value(quote):
    qast = ast.parse(quote)
    sc = StringChecker()
    sc.visit(qast)
    assert len(sc.strings) == 1
    return next(iter(sc.strings)).s


class errors(object):  # noqa
    Q100 = 'Q100 Single quotes should be used by default'
    Q101 = 'Q101 Double quotes should be used to avoid single quote scaping'
    Q102 = 'Q102 When double and single, single quotes should be used'
    Q103 = 'Q103 With single quotes, double quotes should not be escaped'
    Q104 = 'Q104 With double quotes, single quotes should not be escaped'

class PropertyString(str):
    def __init__(self, *args, line=0, col=0, **kwargs):
        super(PropertyString, self).__init__(*args, **kwargs)
        self.value = quote_value(self)
        self.text = self
        self.line = line
        self.col = col

        self.is_raw = self.text.startswith('r')
        if self.is_raw:
            self.text = self.text[1:]

        self.is_bin = self.text.startswith('b')
        if self.is_bin:
            self.text = self.text[1:]

        self.is_dq = self.text.startswith('"')
        self.is_sq = self.text.startswith("'")

        self.is_docstring = self.text[:2] in ('"""', "'''")
        if self.is_docstring:
            self.text = self.text[3:-3]
        else:
            self.text = self.text[1:-1]

    def escaped_quote(self):
        if self.is_docstring:
            return # Docstrings don't have such escaping thing
        escaped, line, col = False, self.line, self.col
        for ch in self.text:
            if ch is '\\':
                escaped = not escaped
                col += 1
                continue
            if not escaped:
                col += 1
                continue
            escaped = False
            if ch is 'n':
                line += 1
                col = 0
                continue
            if ch is 't': # TODO: Check what flake does with tabs
                col +=4
                continue
            if ch is '"':
                yield line, col, ch
            elif ch is "'":
                yield line, col, ch
            col += 1


class QuotesChecker(object):
    '''String literals checker tool'''
    name = 'flake8-quotes'
    version = __version__

    def __init__(self, tree, filename, *args, **kwargs):
        self.tree = tree
        self.filename = filename
        if not filename:
            return
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

    def extract_quote(self, lineno, colno, string):
        '''Classify string and run it's quote extractor'''
        if colno == -1:
            logger.error('Docstrings not implemented: %d:%d %s',
                         lineno, colno, repr(string))
            return  # TODO: Docstring
        simple_quote = self.return_single_quote(lineno - 1, colno)
        try:
            parsed_string = self.quote_value(simple_quote)
        except SyntaxError:
            logger.error('Parsing error, does it have correct syntax?:'
                         ' %d:%d %s => %s', lineno, colno, repr(string),
                         simple_quote)
            return  # TODO: Know when this can happen
        if parsed_string == string:
            yield lineno, colno, simple_quote
            return
        # TODO: Multiline string
        logger.error(
            'Expanding multiple lines not implemented: %d:%d %s => %s',
            lineno, colno, repr(string), simple_quote
        )

    def escaped_quote(self, line, col, raw, quote):
        is_raw = raw.startswith('r')
        for ch in raw:

    def check_quote(self, line, col, raw):
        '''Find errors in the given quote.'''
        is_raw = raw.startswith('r')
        if is_raw:
            quote = raw[1:]
        else:
            quote = raw
        is_docstring = quote[0:2] in ('"""', "'''")
        quote_value = self.quote_value(quote)
        if quote.startswith(DQ):
            if SQ in quote_value:
                if DQ in quote_value:
                    yield line, col, errors.Q102
            else:
                yield line, col, errors.Q100
        if quote.startswith(SQ):
            if SQ in quote_value and DQ not in quote_value:
                yield line, col, errors.Q101

    def run(self):
        # For each parsed string
        for line, colno, string in self.return_all_strings():
            # Extract unjoined quotes, ej. s = 'a' 'b' => 'a', 'b'
            for line_s, col_s, quote in self.extract_quote(line, colno, string):
                # Search errors in each quote
                for line_e, col_e, error = self.check_quote(line_s, col_s, quote):
                    # Send error message
                    yield (line_e, col_e, error, type(self))
