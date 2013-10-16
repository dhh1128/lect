t_linebreak = 13
t_space = 32
t_name = ord('a')
t_colon = ord(':')
t_number = ord('0')
t_indent = ord('\t')
t_comment = ord('#')
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
            
    def _get_token(self, txt, i, end):
        self.beginning_of_line = False
        c = txt[i]
        if c == '\n':
            self.beginning_of_line = True
            return i, i + 1, t_linebreak
        elif c == ' ':
            j = self._spaces(txt, i, end)
            if self.beginning_of_line:
                if self.indenter is None:
                    self.indenter = self.txt[i:j]
                    return i, j, t_indent
                elif (j - i) % len(self.indenter) == 0:
                    return i, j, t_indent
                else:
                    return i, self._rest_of_line(txt, i + 1, end), t_invalid
            else:
                return i, j, t_space
        elif c == '#':
            return i, self._rest_of_line(txt, i + 1, end), t_comment
        elif c == ':':
            return i, i + 1, t_colon
        elif c.isdigit():
            return i, self._number(txt, i + 1, end), t_number
        elif c.isalpha():
            return i, self._name(txt, i + 1, end), t_name
        else:
            return i, i + 1, t_invalid
            
        
    def __call__(self, txt):
        i = 0
        end_of_txt = len(txt)
        while i < end_of_txt:
            start, end, token_type = self._get_token(txt, i, end_of_txt)
            yield start, end, token_type
            i = end
            