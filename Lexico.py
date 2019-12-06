"""
Este trabalho teve como base um algoritmo já previamente desenvolvido, disponível em: "meu.if.edu.br", seu desenvolvedor foi o professor Mário Luiz Rodrigues Oliveira
Foram reaproveitados trechos de código e também a ideia em si do trabalho, essas foram as bases para o desenvolvimento deste.

O arquivo Lexico.py, fornece ao sintático tokens, a ideia dele é, a partir de um arquivo de entrada, vai lendo caractere por caractere, dado seus valores, tratando da forma correta.
"""

from os import path
import re

#TipoToken armazena a classe, descrição e um id para os Tokens
class TipoToken:
    IDENT = ('ID', 'ident', 1)
    CONST = ('CTE', 'const', 2)
    CADCARACTER = ('CADEIA', 'string', 3)
    ATRIB = ('ATRIB', ':=', 5)
    OPIGUAL = ('OPREL', '=', 6)
    OPMENOR = ('OPREL', '<', 7)
    OPMAIOR = ('OPREL', '>', 8)
    OPMENORI = ('OPREL', '<=', 9)
    OPMAIORI = ('OPREL', '>=', 10)
    OPDIF = ('OPREL', '<>', 11)
    OPMAIS = ('OPAD', '+', 12)
    OPMENOS = ('OPAD', '-', 13)
    OPMULT = ('OPMUL', '*', 14)
    OPDIV = ('OPMUL', '/', 15)
    OPNEG = ('OPNEG', '!', 16)
    OPPV = ('PVIRG', ';', 17)
    DPONTOS = ('DPONTOS', ':', 18)
    OPVIRG = ('VIRG', ',', 19)
    OPABREP = ('ABREPAR', '(', 20)
    OPFECHAP = ('FECHAPAR', ')', 21)
    OPABREC = ('ABRECH', '{', 22)
    OPFECHAC = ('FECHACH', '}', 23)
    ERROR = ('ERRO', 'erro', 24)
    FIMARQ = ('EOF', 'fimArquivo', 25)
    LOGICO = ('LOGICO', 'TLogico', 26)
    CARACTER = ('CARACTER', 'caractere', 27)
    FALSO = ('FALSO', 'VLogico', 28)
    VERDADEIRO = ('VERDADEIRO', 'VLogico', 29)
    PROGRAMA = ('PROGRAMA', 'Programa', 30)
    REAL = ('REAL', 'TReal', 31)
    INTEIRO = ('INTEIRO', 'TInteiro', 32)
    VARIAVEL = ('VARIAVEIS', 'Variavel', 33)
    SE = ('SE', 'Condicional', 34)
    SENAO = ('SENAO', 'Condicional', 35)
    WHILE = ('ENQUANTO', 'TLaco', 35)
    READ = ('LEIA', 'Leitura', 36)
    WRITE = ('ESCREVA', 'Leitura', 37)

class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (classe, desc, id) = tipo
        self.id = id
        self.desc = desc
        self.classe = classe
        self.lexema = lexema
        self.linha = linha

class Lexico:
    # dicionário de palavras reservadas
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
    
    #Função Padrão para Abertura de arquivos
    def abreArquivo(self):
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r", encoding="ISO-8859-1")
            # fila de caracteres 'deslidos' pelo ungetChar
            self.buffer = ''
            self.linha = 1
        else:
            print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo)
            quit()

    #Função Fecha Arquivo
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
        #Caso o buffer ja tenha algo, é pego o primeiro caractere
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.arquivo.read(1)
            # se nao foi eof, pelo menos um car foi lido
            # senão len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()
    
    #Função que devolve o caracterer atual que está sendo processado ao buffer de leitura 
    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    #Função principal que pega os tokens, dado um caracterer lido do arquivo, este será tratado devido sua importância para a  linguagem
    def getToken(self):
        estado = 1
        lexema = ''
        car = None
        #Foi usado um regex para verificar os limites do alfabeto
        verificaCaracter = re.compile('[A-Za-z]')
        while True:
            if estado == 1: #Estado inicial que pega o primeiro valor do arquivo para classificar
                car = self.getChar()#Pega-se um caracterer do Arquivo
                #Caso seja nulo apenas retorna token para fim de arquivo
                if car is None:
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)
                #Tratamentos para tabulações, espaços e quebras de linhas
                elif car in {' ', '\t', '\n'}:
                    if car == '\n':
                        self.linha = self.linha + 1
                #Se caracterer lido, for uma letra e estado for igual a um, estado recebe valor 2
                elif verificaCaracter.fullmatch(car) is not None:
                        estado = 2
                #Caso caractere for um número, estado recebe valor 3
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

                else:#Caso o caractere não for nenhum desses tratados é dado como erro e retorna o token de erro
                    return Token(TipoToken.ERROR, '<'+car+'>', self.linha)

            elif estado == 2: #Estado que trata nomes de variáveis ou palavras reservadas
                lexema += car
                car = self.getChar()
                verificaCaracter2 = re.compile('[A-Za-z0-9]')
                #Condição que verifica se o caractere lido é algo diferente do alfabeto a-zA-Z0-9
                #Caso seja diferente é verificado se o lexema atual é um id ou palavra reservada e caso seja um ID, se o id possui tamanha válido
                if verificaCaracter2.fullmatch(car) is None:
                    self.ungetChar(car)
                    if lexema in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema], lexema.lower(), self.linha)

                    elif len(lexema) <= 32:
                            return Token(TipoToken.IDENT, lexema.lower(), self.linha)

           #Condição para números, é verificado se veio um número e se o número é um inteiro ou float. Caso leia um numero e um ponto, é jogado em outro estado para  tratamento
            #Caso nao seja número e nem ponto é lido uma constante inteira
            elif estado == 3:
                lexema += car
                car = self.getChar()
                if car == '.':
                    estado = 33

                elif not car.isdigit():
                    self.ungetChar(car)
                    return Token(TipoToken.CONST, lexema.lower(), self.linha)

            #Retorna token de ponto e vírgula
            elif estado == 4:
                lexema += car
                return Token(TipoToken.OPPV, lexema.lower(), self.linha)

            #Retorna token de Abre Parêntese
            elif estado == 5:
                lexema += car
                return Token(TipoToken.OPABREP, lexema.lower(), self.linha)

            #Retorna token de Fecha Parêntese
            elif estado == 6:
                lexema += car
                return Token(TipoToken.OPFECHAP, lexema.lower(), self.linha)

            #Retorna token de Abre Chave
            elif estado == 7:
                lexema += car
                return Token(TipoToken.OPABREC, lexema.lower(), self.linha)

            #Retorna token de Fecha Chave
            elif estado == 8:
                lexema += car
                return Token(TipoToken.OPFECHAC, lexema.lower(), self.linha)

            #Retorna token de Igual       
            elif estado == 9:
                lexema += car
                return Token(TipoToken.OPIGUAL, lexema.lower(), self.linha)


            elif estado == 10:
                lexema += car
                car = self.getChar()
                if car == '=':
                    return Token(TipoToken.OPMAIORI, lexema.lower(), self.linha)
                else:
                    self.ungetChar(car)
                    return Token(TipoToken.OPMAIOR, lexema.lower(), self.linha)

            #Retorna token de maior ou igual
            elif estado == 11:
                lexema += car
                car = self.getChar()
                if car == '=':
                    return Token(TipoToken.OPMENORI, lexema.lower(), self.linha)
                else:
                    self.ungetChar(car)
                    return Token(TipoToken.OPMENOR, lexema.lower(), self.linha)

            #Retorna token de mais
            elif estado == 12:
                lexema += car
                return Token(TipoToken.OPMAIS, lexema.lower(), self.linha)

            #Retorna token de menos
            elif estado == 13:
                lexema += car
                return Token(TipoToken.OPMENOS, lexema.lower(), self.linha)
            
            #Retorna token de multiplicação
            elif estado == 14:
                lexema += car
                return Token(TipoToken.OPMULT, lexema.lower(), self.linha)

            #Caso encontre comentário de bloco, é jogado em outro estado para tratá-lo, se não for comentário normal "//" ou comentário de bloco "/*", é dado como operador de divisão
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
                    return Token(TipoToken.OPDIV, lexema.lower(), self.linha)

            #Retorna token de negação
            elif estado == 16:
                lexema += car
                return Token(TipoToken.OPNEG, lexema.lower(), self.linha)

            #Retorna token de vírgula
            elif estado == 17:
                lexema += car
                return Token(TipoToken.OPVIRG, lexema.lower(), self.linha)
            
            #Retorna token de atribuição caso a leitura depois dos  dois pontos ":" seja um igual "=", caso nao seja, apenas retorna dois pontos ":"
            elif estado == 18:
                lexema += car
                car = self.getChar()
                if car == '=':
                    lexema += car
                    return Token(TipoToken.ATRIB, lexema.lower(), self.linha)
                else:
                    return Token(TipoToken.DPONTOS, lexema.lower(), self.linha)
            
            #Condição que trata cadeia de caracteres
            elif estado == 19:
                lexema += car
                car = self.getChar()
                if car == '"':
                    lexema += car
                    return Token(TipoToken.CADCARACTER, lexema.lower(), self.linha)

                elif car == "\n":
                    self.linha += 1

                elif car is None:
                    return Token(TipoToken.FIMARQ, lexema.lower(), self.linha)

            #Continuação da função que pega constantes do tipo float
            elif estado == 33:
                lexema += car
                car = self.getChar()
                if not car.isdigit():
                    return Token(TipoToken.ERROR, lexema.lower(), self.linha)
                else:
                    estado = 333
            
            #Condição que trata comentário do tipo "//"
            elif estado == 40:
                car = self.getChar()
                if car == '\n':
                    estado = 1
                    self.linha += 1

            #Condição que trata comentário do tipo bloco "/**/"
            elif estado == 41:
                car = self.getChar()
                if car == '\n':
                    self.linha += 1

                elif car == '*':
                    car = self.getChar()
                    if car == '/':
                        estado = 1

                elif car is None:
                    return Token(TipoToken.FIMARQ, lexema.lower(), self.linha)
            
            #Condição que trata da leitura de constantes, verificação final
            elif estado == 333:
                lexema += car
                car = self.getChar()
                if not car.isdigit():
                    self.ungetChar(car)
                    return Token(TipoToken.CONST, lexema.lower(), self.linha)

