t_linebreak = 13
t_space = 32
t_name = ord('a')
t_colon = ord(':')
t_number = ord('0')
t_indent = ord('\t')
t_comment = ord('#')
t_open_paren = ord('(')
t_close_paren = ord(')')
t_mark = 1
t_plus = ord('+')
t_plus_equals = ord('+') + ord('=')
t_minus = ord('-')
t_minus_equals = ord('-') + ord('=')
t_star = ord('*')
t_star_equals = ord('*') + ord('=')
t_slash = ord('/')
t_slash_equals = ord('/') + ord('=')
t_equals = ord('=')
t_tilde = ord('~')
t_dot = ord('.')
t_comma = ord(',')
t_quote = ord('"')
t_modulo = ord('%')
t_modulo_equals = ord('%') + ord('=')
t_bit_and = ord('&')
t_bit_or = ord('|')
t_bit_xor = ord('^')
t_lt = ord('<')
t_lte = ord('<') + ord('=')
t_2lt = ord('<') * 2
t_gt = ord('>')
t_gte = ord('>') + ord('=')
t_2gt = ord('>') * 2
t_invalid = -1

class Lexer:
    def __init__(self):
        self.indenter = None
        self.indent_level = 0
        self.beginning_of_line = False

    def _spaces(self, txt, i, end):
        while i < end:
            if txt[i] != ' ':
                return i
            i += 1
        return end

    def _number(self, txt, i, end):
        while i < end:
            if not txt[i].isdigit():
                return i
            i += 1
        return end

    def _quoted(self, txt, i, end):
        while i < end:
            c = txt[i]
            if c == '\\':
                i += 1
            elif c == '"':
                return i + 1
            i += 1
        return end

    def _name(self, txt, i, end):
        while i < end:
            c = txt[i]
            if not (c.isalnum() or c == '_'):
                return i
            i += 1
        return end

    def _rest_of_line(self, txt, i, end):
        while i < end:
            if txt[i] == '\n':
                return i
            i += 1
        return end

    def _operator(self, txt, i, end, operator_token, mark_compatible=False):
        if i < end - 1:
            c = txt[i + 1]
            if mark_compatible and c.isalpha():
                return i, self._name(txt, i + 2, end), t_mark
            elif c == '=':
                return i, i + 2, operator_token + ord('=')
        return i, i + 1, operator_token

    def _get_token(self, txt, i, end):
        bol = False
        try:
            c = txt[i]
            if c == '\n':
                bol = True
                return i, i + 1, t_linebreak
            elif c == ' ':
                j = self._spaces(txt, i, end)
                if self.beginning_of_line:
                    if self.indenter is None:
                        self.indenter = txt[i:j]
                        return i, j, t_indent
                    elif (j - i) % len(self.indenter) == 0:
                        return i, j, t_indent
                    else:
                        return i, self._rest_of_line(txt, i + 1, end), t_invalid
                else:
                    return i, j, t_space
            elif c == '#':
                return i, self._rest_of_line(txt, i + 1, end), t_comment
            elif c == ',':
                return i, i + 1, t_comma
            elif c == '=':
                return i, i + 1, t_equals
            elif c == '+':
                return self._operator(txt, i, end, t_plus, mark_compatible=True)
            elif c == '-':
                return self._operator(txt, i, end, t_minus, mark_compatible=True)
            elif c == '*':
                return self._operator(txt, i, end, t_star, mark_compatible=False)
            elif c == '/':
                return self._operator(txt, i, end, t_slash, mark_compatible=False)
            elif c == '%':
                return self._operator(txt, i, end, t_modulo, mark_compatible=False)
            elif c == '&':
                return self._operator(txt, i, end, t_bit_and, mark_compatible=False)
            elif c == '|':
                return self._operator(txt, i, end, t_bit_or, mark_compatible=False)
            elif c == '^':
                return self._operator(txt, i, end, t_bit_xor, mark_compatible=False)
            elif c == '~':
                return self._operator(txt, i, end, t_tilde, mark_compatible=False)
            elif c == '(':
                return i, i + 1, t_open_paren
            elif c == ')':
                return i, i + 1, t_close_paren
            elif c == '"':
                return i, self._quoted(txt, i + 1, end), t_quote
            elif c == ':':
                return i, i + 1, t_colon
            elif c == '.':
                return i, i + 1, t_dot
            elif c == '<':
                if i < end - 1:
                    c = txt[i+1]
                    if c == '=':
                        return i, i + 2, t_lte
                    elif c == '<':
                        return i, i + 2, t_2lt
                return i, i + 1, t_lt
            elif c == '>':
                if i < end - 1:
                    c = txt[i+1]
                    if c == '=':
                        return i, i + 2, t_gte
                    elif c == '<':
                        return i, i + 2, t_2gt
                return i, i + 1, t_gt
            elif c.isdigit():
                return i, self._number(txt, i + 1, end), t_number
            elif c.isalpha():
                return i, self._name(txt, i + 1, end), t_name
            else:
                return i, i + 1, t_invalid
        finally:
            self.beginning_of_line = bol


    def __call__(self, txt):
        i = 0
        end_of_txt = len(txt)
        while i < end_of_txt:
            start, end, token_type = self._get_token(txt, i, end_of_txt)
            yield start, end, token_type
            i = end
