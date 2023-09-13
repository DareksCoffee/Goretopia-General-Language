import sys

TOKEN_STRING = "STRING"
TOKEN_NUMBER = "NUMBER"
TOKEN_PRINT = "PRINT"
TOKEN_LPAREN = "LPAREN"
TOKEN_RPAREN = "RPAREN"
TOKEN_IDENTIFIER = "IDENTIFIER"
TOKEN_ASSIGN = "ASSIGN"
TOKEN_INT = "INT"
TOKEN_FLOAT = "FLOAT"
TOKEN_STRING_TYPE = "STRING_TYPE"

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def advance(self):
        self.pos += 1

    def peek(self):
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None

    def tokenize(self):
        tokens = []
        while self.pos < len(self.text):
            char = self.text[self.pos]

            if char.isspace():
                self.advance()
            elif char == '"':
                tokens.append(self.tokenize_string())
            elif char.isdigit() or char == '.':
                tokens.append(self.tokenize_number())
            elif char.isalpha():
                tokens.append(self.tokenize_keyword())
            elif char == '(':
                tokens.append(Token(TOKEN_LPAREN, char))
                self.advance()
            elif char == ')':
                tokens.append(Token(TOKEN_RPAREN, char))
                self.advance()
            elif char == '=':
                tokens.append(Token(TOKEN_ASSIGN, char))
                self.advance()
            else:
                raise Exception(f"Invalid character: {char}")

        return tokens

    def tokenize_string(self):
        value = ""
        self.advance()  
        while self.peek() != '"':
            value += self.peek()
            self.advance()
        self.advance()
        return Token(TOKEN_STRING, value)

    def tokenize_identifier(self):
        value = ""
        while self.peek() and (self.peek().isalpha() or self.peek().isdigit()):
            value += self.peek()
            self.advance()
        return Token(TOKEN_IDENTIFIER, value)

    def tokenize_number(self):
        value = ""
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            value += self.peek()
            self.advance()
        if '.' in value:
            return Token(TOKEN_FLOAT, float(value))
        else:
            return Token(TOKEN_INT, int(value))

    def tokenize_keyword(self):
        value = ""
        while self.peek() and (self.peek().isalpha() or self.peek().isdigit()):
            value += self.peek()
            self.advance()
        if value.lower() == "print":
            return Token(TOKEN_PRINT, value)
        elif value.lower() == "int":
            return Token(TOKEN_INT, value)
        elif value.lower() == "float":
            return Token(TOKEN_FLOAT, value)
        elif value.lower() == "string":
            return Token(TOKEN_STRING_TYPE, value)
        else:
            return Token(TOKEN_IDENTIFIER, value)


def interpret(tokens):
    variables = {}
    current_data_type = None
    i = 0
    while i < len(tokens):
        if tokens[i].type == TOKEN_INT or tokens[i].type == TOKEN_FLOAT or tokens[i].type == TOKEN_STRING_TYPE:
            current_data_type = tokens[i].type
            i += 1
            if i < len(tokens) and tokens[i].type == TOKEN_IDENTIFIER:
                variable_name = tokens[i].value
                i += 1
                if i < len(tokens) and tokens[i].type == TOKEN_ASSIGN:
                    i += 1
                    if i < len(tokens):
                        if tokens[i].type in [TOKEN_INT, TOKEN_FLOAT, TOKEN_STRING]:
                            assigned_value = tokens[i].value
                            if current_data_type == TOKEN_INT:
                                assigned_value = int(assigned_value)
                            elif current_data_type == TOKEN_FLOAT:
                                assigned_value = float(assigned_value)

                            variables[variable_name] = assigned_value
                            i += 1
                        else:
                            print(f"Error: Invalid assignment to '{variable_name}'")
                            return
                    else:
                        print(f"Error: Missing assignment value for '{variable_name}'")
                        return
                else:
                    print("Error: Invalid variable assignment")
                    return
            else:
                print("Error: Expected variable name after data type declaration")
                return
        elif tokens[i].type == TOKEN_PRINT:
            i += 1
            if i < len(tokens) and tokens[i].type == TOKEN_LPAREN:
                i += 1
                output = ""
                while i < len(tokens) and tokens[i].type != TOKEN_RPAREN:
                    if tokens[i].type == TOKEN_IDENTIFIER:
                        if tokens[i].value in variables:
                            output += str(variables[tokens[i].value])
                        else:
                            print(f"Error: Variable '{tokens[i].value}' is not defined")
                            return
                    elif tokens[i].type == TOKEN_INT or tokens[i].type == TOKEN_FLOAT or tokens[i].type == TOKEN_STRING:
                        output += str(tokens[i].value)
                    else:
                        output += tokens[i].value
                    i += 1
                if i < len(tokens) and tokens[i].type == TOKEN_RPAREN:
                    print(output)
                    i += 1
                else:
                    print("Error: Missing closing parenthesis after 'print'")
                    return
            else:
                print("Error: Missing opening parenthesis after 'print'")
                return
        else:
            print("Error: Expected data type declaration, 'print' statement, or variable assignment")
            return


def main():
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <filename>")
        return

    filename = sys.argv[1]
    try:
        with open(filename, "r") as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    interpret(tokens)

if __name__ == "__main__":
    main()