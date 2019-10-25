from os import path

class TipoToken:
    IDENT = ('ID', 'ident') #No Máximo 32 bits // Não Case Sensitive
    CONST = ('CTE', 'const')
    CADCARACTER = ('CADEIA', 'string')
    ATRIB = ('ATRIB', ':=')
    OPIGUAL = ('OPREL', '=')
    OPMENOR = ('OPREL', '<')
    OPMAIOR = ('OPREL', '>')
    OPMENORI = ('OPREL', '<=')
    OPMAIORI = ('OPREL', '>=')
    OPDIF = ('OPREL', '<>')
    OPMAIS = ('OPAD', '+')
    OPMENOS = ('OPAD', '-')
    OPMULT = ('OPMUL', '*')
    OPDIV = ('OPMUL', '/')
    OPNEG = ('OPNEG', '!')
    OPPV = ('PVIRG', ';')
    DPONTOS = ('DPONTOS', ':')
    OPVIRG = ('VIRG', ',')
    OPABREP = ('ABREPAR', '(')
    OPFECHAP = ('FECHAPAR', ')')
    OPABREC = ('ABRECH', '{')
    OPFECHAC = ('FECHACH', '}')
    ERROR = ('ERRO', 'erro')
    FIMARQ = ('EOF', 'fimArquivo')
    LOGICO = ('LOGICO', 'TLogico')
    CARACTER = ('CARACTER', 'caractere')
    FALSO = ('FALSO', 'VLogico')
    VERDADEIRO = ('VERDADEIRO', 'VLogico')
    PROGRAMA = ('PROGRAMA', 'Programa')
    REAL = ('REAL', 'TReal')
    INTEIRO = ('INTEIRO', 'TIntero')
    VARIAVEL = ('VARIAVEIS', 'Variavel')
    SE = ('SE', 'Condicional')
    SENAO = ('SENAO', 'Condicional')
    WHILE = ('ENQUANTO', 'TLaco')
    READ = ('LEIA', 'Leitura')
    WRITE = ('ESCREVA', 'Leitura')

class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (classe, id) = tipo
        self.id = id
        self.classe = classe
        self.lexema = lexema
        self.linha = linha

    def getIDToken(self):
        return self.id

    def getClasseToken(self):
        return self.classe

    def getLinhaToken(self):
        return self.linha

    def getLexemaToekn(self):
        return self.lexema
    
    def setIDToken(self, id):
        self.id = id

    def setClasseToken(self, classe):
        self.classe = classe

    def setLinhaToken(self, linha):
        self.linha = linha

    def setLexemaToekn(self, lexema):
       self.lexema = lexema

class Lexico:
    # dicionario de palavras reservadas
    reservadas = {'programa': TipoToken.PROGRAMA, 'variaveis': TipoToken.VARIAVEL, 'inteiro': TipoToken.INTEIRO, 'real': TipoToken.REAL, 'logico': TipoToken.LOGICO,
                  'caracter': TipoToken.CARACTER, 'se': TipoToken.SE, 'senao': TipoToken.SENAO, 'enquanto': TipoToken.WHILE,
                  'leia': TipoToken.READ, 'escreva': TipoToken.WRITE, 'falso': TipoToken.FALSO , 'verdadeiro': TipoToken.VERDADEIRO}

    tiposLinguagem = {'inteiro', 'real', 'logico', 'caractere'}

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        self.buffer = None
        self.linha = 0
        # os atributos buffer e linha sao incluidos no metodo abreArquivo

    def abreArquivo(self):
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r")
            # fila de caracteres 'deslidos' pelo ungetChar
            self.buffer = ''
            self.linha = 1
        else:
            print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo)
            quit()

    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        else:
            self.arquivo.close()

    def getChar(self):#Função que pega um valor do arquivo, um de cada vez
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.arquivo.read(1)
            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    def getToken(self):
        estado = 1
        lexema = ''
        car = None
        while True:
            if estado == 1: #Estado inicial que pega o primeiro valor do arquivo para classificar
                car = self.getChar()
                if car is None:
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)

                elif car in {' ', '\t', '\n'}:
                    if car == '\n':
                        self.linha = self.linha + 1

                elif car.isalpha():
                    estado = 2

                elif car.isdigit():
                    estado = 3

                elif car == ';':
                    estado = 4

                elif car == '(':
                    estado = 5

                elif car == ')':
                    estado = 6

                elif car == '{':
                    estado = 7

                elif car == '}':
                    estado = 8

                elif car == '=':
                    estado = 9

                elif car == '>':
                    estado = 10

                elif car == '<':
                    estado = 11

                elif car == '+':
                    estado = 12

                elif car == '-':
                    estado = 13

                elif car == '*':
                    estado = 14

                elif car == '/':
                    estado = 15

                elif car == '!':
                    estado = 16

                elif car == ',':
                    estado = 17

                elif car == ':':
                    estado = 18

                elif car == '"':
                    estado = 19

                else:
                    return Token(TipoToken.ERROR, '<'+car+'>', self.linha)

            elif estado == 2: #Estado que trata nomes de variáveis ou palavras reservadas
                lexema += car
                car = self.getChar()
                if not car.isdigit() and not car.isalpha():
                    self.ungetChar(car)
                    if lexema in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema], lexema, self.linha)

                    else:
                        if len(lexema) <= 32:
                            return Token(TipoToken.IDENT, lexema, self.linha)

                        else:
                            return Token(TipoToken.ERROR, '<' + lexema + '>' +
                            'Identificado com tamanho maior ou igual a 32', self.linha)


            elif estado == 3:
                lexema += car
                car = self.getChar()
                if car == '.':
                    estado = 33

                elif not car.isdigit():
                    self.ungetChar(car)
                    return Token(TipoToken.CONST, lexema, self.linha)

            elif estado == 4:
                lexema += car
                return Token(TipoToken.OPPV, lexema, self.linha)

            elif estado == 5:
                lexema += car
                return Token(TipoToken.OPABREP, lexema, self.linha)

            elif estado == 6:
                lexema += car
                return Token(TipoToken.OPFECHAP, lexema, self.linha)

            elif estado == 7:
                lexema += car
                return Token(TipoToken.OPABREC, lexema, self.linha)

            elif estado == 8:
                lexema += car
                return Token(TipoToken.OPFECHAC, lexema, self.linha)

            elif estado == 9:
                lexema += car
                return Token(TipoToken.OPIGUAL, lexema, self.linha)


            elif estado == 10:
                lexema += car
                car = self.getChar()
                if car == '=':
                    return Token(TipoToken.OPMAIORI, lexema, self.linha)
                else:
                    self.ungetChar(car)
                    return Token(TipoToken.OPMAIOR, lexema, self.linha)

            elif estado == 11:
                lexema += car
                car = self.getChar()
                if car == '=':
                    return Token(TipoToken.OPMAIOR, lexema, self.linha)
                else:
                    self.ungetChar(car)
                    return Token(TipoToken.OPMENOR, lexema, self.linha)

            elif estado == 12:
                lexema += car
                return Token(TipoToken.OPMAIS, lexema, self.linha)

            elif estado == 13:
                lexema += car
                return Token(TipoToken.OPMENOS, lexema, self.linha)

            elif estado == 14:
                lexema += car
                return Token(TipoToken.OPMULT, lexema, self.linha)

            elif estado == 15:
                lexema += car
                car = self.getChar()
                if car == '/':
                    lexema = lexema[:-1]
                    estado = 40
                elif car == '*':
                    lexema = lexema[:-1]
                    estado = 41
                else:
                    return Token(TipoToken.OPDIV, lexema, self.linha)

            elif estado == 16:
                lexema += car
                return Token(TipoToken.OPNEG, lexema, self.linha)

            elif estado == 17:
                lexema += car
                return Token(TipoToken.OPVIRG, lexema, self.linha)

            elif estado == 18:
                lexema += car
                car = self.getChar()
                if car == '=':
                    lexema += car
                    return Token(TipoToken.ATRIB, lexema, self.linha)
                else:
                    return Token(TipoToken.DPONTOS, lexema, self.linha)

            elif estado == 19:
                lexema += car
                car = self.getChar()
                if car == '"':
                    return Token(TipoToken.CADCARACTER, lexema, self.linha)

            elif estado == 33:
                lexema += car
                car = self.getChar()
                if not car.isdigit():
                    return Token(TipoToken.ERROR, '<'+ lexema + '>', self.linha)
                else:
                    estado = 333

            elif estado == 40:
                car = self.getChar()
                if car == '\n':
                    estado = 1
                    self.linha += 1

            elif estado == 41:
                car = self.getChar()
                if car == '\n':
                    self.linha += 1

                elif car == '*':
                    car = self.getChar()
                    if car == '/':
                        estado = 1

            elif estado == 333:
                lexema += car
                car = self.getChar()
                if not car.isdigit():
                    self.ungetChar(car)
                    return Token(TipoToken.CONST, lexema, self.linha)


if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'exemplo1.txt'
   lex = Lexico(nome)
   lex.abreArquivo()

   while(True):
       token = lex.getToken()
       print("token= %s , lexema= (%s), linha= %d" % (token.classe, token.lexema, token.linha))
       if token.classe == TipoToken.FIMARQ[0]:
           break
   lex.fechaArquivo()