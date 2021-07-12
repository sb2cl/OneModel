from position import Position
from tokens import Token, TokenType

WHITESPACE = ' \n\t'
DIGITS = '0123456789'

# Keywords reserved.
KEYWORDS = [
        'VAR',
        'AND',
        'OR',
        'NOT',
        'IF',
        'ELIF',
        'ELSE',
        'FOR',
        'TO',
        'STEP',
        'WHILE',
        'FUN',
        'THEN',
        'END',
        'RETURN',
        'CONTINUE',
        'BREAK',
        ]

class Lexer:
    """ LEXER

    This class takes input text and generates a list of tokens.
    """

    def __init__(self,fn,text):
        """
        @brief: Constructor of Lexer.

        @param: fn   Filename of the text (used in error generation).
              : text Input text to convert into tokens.
        """
        self.fn = fn
        self.text = text
        # Init the position
        self.pos = Position(-1,0,-1,fn,text)
        # Current char to be processed by the Lexer.
        self.current_char = None
        # Advance to the first char of the input text.
        self.advance()

    def advance(self):
        """ ADVANCE
        @brief: Update self.current_char with the next char to be processed.

        @return: None
        """
        # Keep track of the position in the file
        self.pos.advance(self.current_char)
        # Update current_char
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        """ MAKE_TOKENS
        @brief: Process all the input text and make the corresponding tokens.

        @return: tokens Array with the tokens.
               : error  ExpectedCharError, IllegalCharError, or None
        """
        tokens = []

        # Process all the chars one by one
        while self.current_char != None:
            # Remove white space
            if self.current_char in WHITESPACE:
                self.advance()

            elif self.current_char == '.' or self.current_char in DIGITS:
                tokens.append(self.generate_number())

            elif self.current_char == '"':
                tokens.append(self.generate_string())

            elif self.current_char == '+':
                tokens.append(Token(TokenType.PLUS, pos_start=self.pos))
                self.advance()

        # Add end of file token.
        tokens.append(Token(TokenType.END_OF_FILE, pos_start=self.pos))
        return tokens, None

    def generate_number(self):
        """ GENERATE_NUMBER
        @brief: Generate a number (float)

        @return: Token Generated number token.
        """
        decimal_point_count = 0
        number_str = self.current_char
        pos_start = self.pos.copy()

        self.advance()

        while self.current_char != None and (self.current_char == '.' or self.current_char in DIGITS):
            if self.current_char == '.':
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break

            number_str += self.current_char
            self.advance()

        if number_str.startswith('.'):
            number_str = '0' + number_str
        if number_str.endswith('.'):
            number_str += '0'

        return Token(TokenType.NUMBER, value=(number_str), pos_start=pos_start, pos_end=self.pos)

    def generate_string(self):
        """ GENERATE_STRING
        @brief: Generate a string

        @return: Token  Generated string Token
        """
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {
                'n': '\n',
                't': '\t',
                '"': '"'
                }

        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
            else:
                if self.current_char == '\\':
                    escape_character = True
                    self.advance()
                    continue # The above statements are useless without thiss one.
                else:
                    string += self.current_char
                self.advance()
                escape_character = False

        self.advance()
        return Token(TokenType.STRING, string, pos_start, self.pos)
