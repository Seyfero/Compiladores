# Trabalho de Compiladores 2019.
# IFMG - Campus Formiga.
#
# Alunos: Renan Evilásio Silva de Oliveira;
#         Saulo Cassiano de Carvalho
#
# Linguagem P :
#
# A -> PROG
# PROG -> programa id pvirg DECLS C-COMP
# DECLS -> vazio | variaveis LIST-DECLS
# LIST-DECLS -> DECL-TIPO D
# D -> vazio | LIST-DECLS
# DECL-TIPO -> LIST-ID dpontos TIPO pvirg
# LIST-ID -> id E
# E -> vazio | virg LIST-ID
# TIPO -> inteiro | real | logico | caracter
# C-COMP -> abrech LISTA-COMANDOS fechach
# LISTA-COMANDOS -> COMANDOS G
# G -> vazio | LISTA-COMANDOS
# COMANDOS -> IF | WHILE | READ | WRITE | ATRIB
# IF -> se abrepar EXPR fechapar C-COMP H
# H -> vazio | senao C-COMP
# WHILE -> enquanto abrepar EXPR fechapar C-COMP
# READ -> leia abrepar LIST-ID fechapar pvirg
# ATRIB -> id atrib EXPR pvirg
# WRITE -> escreva abrepar LIST-W fechapar pvirg
# LIST-W -> ELEM-W L
# L -> vazio | virg LIST-W
# ELEM-W -> EXPR | cadeia
# EXPR -> SIMPLES P
# P -> vazio | oprel SIMPLES
# SIMPLES -> TERMO R
# R -> vazio | opad SIMPLES
# TERMO -> FAT S
# S -> vazio | opmul TERMO
# FAT -> id | cte | abrepar EXPR fechapar | verdadeiro | falso | opneg FAT
#
#-----------------------------------------------------------------------------------------------------------------------
"""
Este trabalho teve como base um algoritmo já previamente desenvolvido, disponível em: "meu.if.edu.br", seu desenvolvedor foi o professor Mário Luiz Rodrigues Oliveira
Foram reaproveitados trechos de código e também a ideia em si do trabalho, essas foram as bases para o desenvolvimento deste.

Cada erro encontrado são mostrados todos tokens que se esperava naquele momento. Para verificação dos erros, é usado o "Modo Pânico". Este foi desenvolvido seguindo a linha de pensamento usando Follows. Cada função tem seu Follow, com isso, o programa tenta executar a ação e caso não consiga, ele entra em um "Exception". Após isto, é procuro um token para fornecer sincronia na gramática após o erro e o resto desta e assim, encontrado um, tenta-se continuar a execução. Porém, por se tratar de uma heurística, não é eficaz para todos casos.

Para roda o Arquivo, primeiro chama-se o interpretador Python3, em sequência chama-se o analisador: AnalisadorSintatico.py, caso queira ver a tabela de símbolos, passa-se o parâmetro "-t" e por fim, o arquivo que contém a gramática.

Exemplo para rodar: python3 AnalisadorSintatico.py -t exemplo1.txt
Exemplo para rodar: python3 AnalisadorSintatico.py exemplo1.txt
"""


from Lexico import TipoToken as tt, Lexico
import sys

class Sintatico:

    # TABELA DOS FOLLOWS DE CADA FUNÇÃO:
    FOLLOW_A = [tt.FIMARQ]
    FOLLOW_PROG = [tt.FIMARQ[0]]
    FOLLOW_DECLS = [tt.OPABREC[0], tt.FIMARQ[0]]
    FOLLOW_LIST_DECLS = [tt.OPABREC[0], tt.OPPV[0], tt.FIMARQ[0]]
    FOLLOW_D = [tt.OPABREC[0], tt.FIMARQ[0]]
    FOLLOW_DECL_TIPO = [tt.OPABREC[0], tt.IDENT[0], tt.FIMARQ[0]]
    FOLLOW_LIST_ID = [tt.DPONTOS[0], tt.OPFECHAP[0], tt.FIMARQ[0]]
    FOLLOW_E = [tt.DPONTOS[0], tt.OPFECHAP[0], tt.FIMARQ[0]]
    FOLLOW_TIPO = [tt.OPPV[0], tt.FIMARQ[0]]
    FOLLOW_C_COMP = [tt.WHILE[0], tt.WRITE[0], tt.OPFECHAC[0], tt.IDENT[0], tt.READ[0], tt.SE[0], tt.SENAO[0], tt.FIMARQ[0]]
    FOLLOW_LISTA_COMANDOS = [tt.OPFECHAC[0], tt.FIMARQ[0]]
    FOLLOW_G = [tt.OPFECHAC, tt.FIMARQ[0]]
    FOLLOW_COMANDOS = [tt.FIMARQ[0], tt.WHILE[0], tt.WRITE[0], tt.OPFECHAP[0], tt.IDENT[0], tt.READ[0], tt.SE[0]]
    FOLLOW_IF = [tt.FIMARQ[0], tt.WHILE[0], tt.WRITE[0], tt.OPFECHAP[0], tt.IDENT[0], tt.READ[0], tt.SE[0]]
    FOLLOW_H = [tt.FIMARQ[0], tt.WHILE[0], tt.WRITE[0], tt.OPFECHAP[0], tt.IDENT[0], tt.READ[0], tt.SE[0]]
    FOLLOW_WHILE = [tt.FIMARQ[0], tt.WHILE[0], tt.WRITE[0], tt.OPFECHAP[0], tt.IDENT[0], tt.READ[0], tt.SE[0]]
    FOLLOW_READ = [tt.FIMARQ[0], tt.WHILE[0], tt.WRITE[0], tt.OPFECHAP[0], tt.IDENT[0], tt.READ[0], tt.SE[0]]
    FOLLOW_ATRIB = [tt.FIMARQ[0], tt.WHILE[0], tt.WRITE[0], tt.OPFECHAP[0], tt.IDENT[0], tt.READ[0], tt.SE[0]]
    FOLLOW_WRITE = [tt.FIMARQ[0], tt.WHILE[0], tt.WRITE[0], tt.OPFECHAP[0], tt.IDENT[0], tt.READ[0], tt.SE[0]]
    FOLLOW_ELEM_W = [tt.FIMARQ[0], tt.OPFECHAP[0], tt.OPVIRG[0]]
    FOLLOW_P = [tt.FIMARQ[0], tt.OPFECHAP[0], tt.OPVIRG[0], tt.OPPV[0]]
    FOLLOW_R = [tt.FIMARQ[0], tt.OPFECHAP[0], tt.OPVIRG[0], tt.OPPV[0]]
    FOLLOW_S = [tt.FIMARQ[0], tt.OPFECHAP[0], tt.OPVIRG[0], tt.OPPV[0]]
    FOLLOW_FAT = [tt.FIMARQ[0], tt.OPMAIS[0], tt.OPMULT[0]]

    # CONSTRUTOR DA CLASSE SINTATICO.
    def __init__(self, nomeArquivo):
        self.lex = None # LEXICO COMEÇA VAZIO.
        self.tokenAtual = None # COMEÇA COM O TOKEN ESCOLHIDO VAZIO.
        self.compiladoSucesso = [True,0] # COMEÇA COM O RESULTADO DA COMPILAÇÃO REALIZADA COM SUCESSO.
        self.vetTabela = [] # COMEÇA COM O VETOR VAZIO NA TABELA DE SIMBOLOS.
        self.nomeArquivo = nomeArquivo # RECEBE O NOME DO ARQUIVO POR MEIO DE PARAMETRO.

    # FUNÇÃO PARA ABRIR O ARQUIVO E COMECAR A COMPILAÇÃO.
    def interprete(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo() # ABRE O ARQUIVO PASSADO POR PARAMETRO.
            self.tokenAtual = self.lex.getToken() # A FUNÇÃO "getToken" PEGA UM TOKEN DO LEXICO
            # PARA MINHA VARIAVEL CHAMADA "tokenAtual".
            self.A()

    # FUNÇÃO QUE REALIZA O PROCESSO FINAL DA COMPILAÇÃO.
    def finalArquivo(self, nome):
        param = sys.argv
        if self.compiladoSucesso == [True,0]: # SE A TUPLA DA VARIAVEL "compiladoSucesso" FOR "True, 0".
            # MOSTRA QUE COMPILAÇÃO FOI COM SUCESSO E QUE NÃO MOSTROU NENHUMA VEZ A MENSAGEM DO RESULTADO DE COMPILAÇÃO.
            print('Compilado com Sucesso !.')
            if param[1] == '-t': # CASO TENHA PEDIDO PARA MOSTRAR A TABELA DE SIMBOLOS.
                self.printTabela(nome) # A FUNÇÃO DA PRINT DA TABELA NO TERMINAL.
            self.compiladoSucesso = [True]
        elif self.compiladoSucesso == [False,0]: # SE A TUPLA DA VARIAVEL "compiladoSucesso" FOR "Falsa, 0"
            # MOSTRA QUE COMPILAÇÃO FOI COM FALHA E QUE NÃO MOSTROU NENHUMA VEZ A MENSAGEM DO RESULTADO DE COMPILAÇÃO.
            print('Falha na Compilacao !.')
            if param[1] == '-t': # CASO TENHA PEDIDO PARA MOSTRAR A TABELA DE SIMBOLOS.
                self.printTabela(nome) # A FUNÇÃO DA PRINT DA TABELA NO TERMINAL.
            self.compiladoSucesso = [False]
        quit(0) # DA UM QUIT NO CODIGO, DESEMPILANDO.

    # FUNÇÃO QUE FAZ A COMPARAÇÃO DO TOKEN ATUAL PELO ESPERADA.
    def atualIgual(self, token):
        (classe, desc, id) = token # PEGA O TOKEN ATUAL E COLOCA NUMA TUPLA.
        return self.tokenAtual.classe == classe # COMPARA A VARIAVEL CLASSE DA TUPLA COM A CLASSE QUE É ESPERADA PELA LINGUAGEM.

    # FUNÇÃO QUE CONSOME O TOKEN ATUAL E PEGA O PROXIMO TOKEN, CASO CONTRARIO ENTRA NO MODO PANICO.
    def consome(self, token):
        if self.atualIgual(token): # SE O TOKEN PEGADO FOR O ESPERADO ENTÃO PEGA O PROXIMO TOKEN.
            if self.tokenAtual.classe == tt.IDENT[0]:
                self.vetTabela.append(self.tokenAtual.lexema) # ADICIONA O "id" NO VETOR DA TABELA DE SIMBOLOS.
            self.tokenAtual = self.lex.getToken()
        else: # CASO CONTRARIO ELE INFORMA NO TERMINAL UMA MENSAGEM DE ERRO E ATIVA O MODO PANICO.
            self.mensagemERRO(token)
            self.modoPanico()

    # FUNÇÃO QUE MOSTRA OS ERROS NO TERMINAL.
    def mensagemERRO(self, token):
        (classe, desc, id) = token # PEGA O TOKEN ATUAL E COLOCA NUMA TUPLA.
        self.compiladoSucesso = [False, 0] # NA VARIAVEL "compiladoSucesso" COLOCA "False" INFORMANDO QUE A COMPILAÇÃO FALHOU.
        print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"' % (
        self.tokenAtual.linha, desc, self.tokenAtual.lexema)) # DA UM PRINT DE ERRO NO TEMINAL.

    # FUNÇÃO QUE ENTRA NO FOLLOW
    def modoPanico(self):
        self.tokenAtual = self.lex.getToken() # PEGA O PROXIMO TOKEN.
        raise Exception("") # ENTRA NO EXCEPTION DA FUNÇÃO QUE ESTAVA.

    # A PRIMEIRA FUNÇÃO DA GRAMATICA.
    def A(self):
        self.PROG() # FUNÇÃO QUE COMEÇA A CONSUMIR OS TOKENS DO TXT.
        self.lex.fechaArquivo() # FECHA O ARQUIVO QUE ESTAVA SENDO LIDO.
        self.finalArquivo(self.nomeArquivo)

    # FUNÇÃO QUE VERIFICA SE O INICIO DO CODIGO ESTA CORRETO PARA DEPOIS ENTRAR NA DECLARAÇAO DE VARIAVEIS E DEPOIS NO CORPO DO CODIGO.
    def PROG(self):
        try:
            self.consome(tt.PROGRAMA) # CONSOME O TOKEN "programa".
            self.consome(tt.IDENT) # CONSOME O TOKEN "id".
            self.consome(tt.OPPV) # CONSOME O TOKEN ";".
            self.DECLS()
            self.C_COMP()
        except:
            self.get_FOLLOW_PROG()

    # FUNÇAO QUE PEGA O FOLLOW DE PROG.
    def get_FOLLOW_PROG(self):
        if self.tokenAtual.classe in self.FOLLOW_PROG: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.OPPV[0]: # VERIFICA E CONSOME O TOKEN ";" E CONTINUA A GRAMATICA.
                self.consome(tt.OPPV)
                self.DECLS()
                self.C_COMP()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_PROG()

    # FUNÇÃO QUE INICIA A DECLARAÇÃO DE VARIAVEIS.
    def DECLS (self):
        try:
            if self.atualIgual(tt.VARIAVEL): # VERIFICA SE O TOKEN É "variavel" CASO SEJA CONSOME O TOKEN
                self.consome(tt.VARIAVEL)
                self.LIST_DECLS()
            else:
                pass
        except:
            self.get_FOLLOW_DECLS()

    # FUNÇÃO QUE PEGA O FOLLOW DE DECLS
    def get_FOLLOW_DECLS(self):
        if self.tokenAtual.classe in self.FOLLOW_DECLS: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.OPABREC[0]: # VERIFICA SE TOKEN É "{" E CONTINUA A GRAMATICA.
                self.C_COMP()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_DECLS()

    # VAI COMEÇAR A PEGAR OS ID E SEUS TIPOS
    def LIST_DECLS(self):
        try:
            self.DECL_TIPO()
            self.D()
        except:
            self.get_FOLLOW_LIST_DECLS()

    # FUNÇÃO QUE PEGA O FOLLOW DE LIST_DECLS
    def get_FOLLOW_LIST_DECLS(self):
        if self.tokenAtual.classe in self.FOLLOW_LIST_DECLS: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.OPABREC[0]: # VERIFICA SE TOKEN É "{" E CONTINUA A GRAMATICA.
                self.C_COMP()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_LIST_DECLS()

    # FUNÇÃO QUE VERIFICA SE O TOKEN E ID
    def D(self):
        try:
            if self.atualIgual(tt.IDENT): # VERIFICA SE EXISTE MAIS UM ID COMO VARIAVEL
                self.LIST_DECLS()
            else: # CASO CONTRARIO ACABOU AS DECLARAÇÕES DE VARIAVEIS
                pass
        except:
            self.get_FOLLOW_D()

    # FUNÇÃO QUE PEGA O FOLLOW DE D
    def get_FOLLOW_D(self):
        if self.tokenAtual.classe in self.FOLLOW_D: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.OPABREC[0]: # VERIFICA SE TOKEN É "{" E CONTINUA A GRAMATICA.
                self.C_COMP()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_D()

    # FUNÇÃO QUE MONTA A FORMA CERTA DA LINGUAGEM
    def DECL_TIPO(self):
        try:
            self.LIST_ID() # PEGA A ID DA VARIAVEL.
            self.consome(tt.DPONTOS) # CONSOME O TOKEN ":".
            self.TIPO() # PEGA O TIPO DA ID ACIMA.
            self.consome(tt.OPPV) # CONSOME O TOKEN ";".
        except:
            self.get_FOLLOW_DECL_TIPO()

    # FUNÇÃO QUE PEGA O FOLLOW DE DECL_TIPO
    def get_FOLLOW_DECL_TIPO(self):
        if self.tokenAtual.classe in self.FOLLOW_DECL_TIPO: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.OPABREC[0]: # VERIFICA SE TOKEN É "{" E CONTINUA A GRAMATICA.
                self.C_COMP()
            elif self.tokenAtual.classe == tt.IDENT[0]: # VERIFICA SE TOKEN É DA CLASSE "id" E CONTINUA A GRAMATICA.
                self.DECL_TIPO()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_DECL_TIPO()

    # FUNÇÃO QUE CONSOME E COLOCA NA TABELA O ID.
    def LIST_ID(self):
        try:
            self.consome(tt.IDENT) # CONSOME O TOKEN "id".
            self.E() # FUNÇÃO PARA VERIFICAR SE EXISTE "," PARA COLOCAR OUTRO "id" COM O MESMO TIPO.
        except:
            self.get_FOLLOW_LIST_ID()

    # FUNÇÃO QUE PEGA O FOLLOW DE LIST_ID
    def get_FOLLOW_LIST_ID(self):
        if self.tokenAtual.classe in self.FOLLOW_LIST_ID: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.DPONTOS[0]: # VERIFICA SE TOKEN É ":" E CONTINUA A GRAMATICA.
                return
            elif self.tokenAtual.classe == tt.OPFECHAP[0]: # VERIFICA SE TOKEN É DA CLASSE ")" E CONSOME O TOKEN.
                self.consome(tt.OPFECHAP)
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_LIST_ID()

    # FUNÇÃO QUE VERIFICA SE POSSUI "," DEPOIS DO ID.
    def E(self):
        if self.atualIgual(tt.OPVIRG): # VERIFICA SE O TOKEN É "," E CONSOME O TOKEN.
            self.consome(tt.OPVIRG)
            self.LIST_ID()

    # FUNÇÃO QUE VERIFICA, CONSOME E COLOCA NA TABELA O TIPO DO ID.
    def TIPO(self):
        try: # VERIFICA QUAL É O TIPO DO "id" E ADICIONA NA TABELA RELACIONANDO AO "id" E CONSOME O TOKEN.
            if self.atualIgual(tt.INTEIRO):
                self.vetTabela.append([self.tokenAtual.classe, self.tokenAtual.linha])
                self.consome(tt.INTEIRO)
            elif self.atualIgual(tt.REAL):
                self.vetTabela.append([self.tokenAtual.classe, self.tokenAtual.linha])
                self.consome(tt.REAL)
            elif self.atualIgual(tt.LOGICO):
                self.vetTabela.append([self.tokenAtual.classe, self.tokenAtual.linha])
                self.consome(tt.LOGICO)
            elif self.atualIgual(tt.CARACTER):
                self.vetTabela.append([self.tokenAtual.classe, self.tokenAtual.linha])
                self.consome(tt.CARACTER)
            else: # CASO NÃO SEJA NENHUM, LISTA TODAS AS POSSIBILIDADES PARA COMPILAR COM SUCESSO NO TERMINAL.
                self.mensagemERRO(tt.INTEIRO)
                self.mensagemERRO(tt.REAL)
                self.mensagemERRO(tt.LOGICO)
                self.mensagemERRO(tt.CARACTER)
                # E ENTRA NO MODOPANICO PARA ENTRAR NO EXCEPTION.
                self.modoPanico()
        except:
            self.get_FOLLOW_TIPO()

    # FUNÇÃO QUE PEGA O FOLLOW DE TIPO
    def get_FOLLOW_TIPO(self):
        if self.tokenAtual.classe in self.FOLLOW_LIST_ID: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.OPPV[0]:
                self.consome(tt.OPPV)
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_TIPO()

    # FUNÇÃO QUE INICIA O CORPO DO CODIGO DEPOIS DAS VARIAVEIS.
    def C_COMP(self):
        try:
            self.consome(tt.OPABREC) # CONSOME O TOKEN "{".
            self.LISTA_COMANDOS() # FUNÇÃO QUE INICIA O CORPO DO CODIGO DEPOIS DE DECLARAR AS VARIAVEIS.
            self.consome(tt.OPFECHAC) # CONSOME O TOKEN "}".
        except:
            self.get_FOLLOW_C_COMP()

    # FUNÇÃO QUE PEGA O FOLLOW DE C_COMP
    def get_FOLLOW_C_COMP(self):
        if self.tokenAtual.classe in self.FOLLOW_C_COMP: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.WHILE[0]:  # VERIFICA SE TOKEN É "while" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.WRITE[0]:  # VERIFICA SE TOKEN É "write" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.IDENT[0]:  # VERIFICA SE TOKEN É DA CLASSE "id" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.READ[0]:  # VERIFICA SE TOKEN É "read" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.SE[0]:  # VERIFICA SE TOKEN É "if" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_C_COMP()

    def LISTA_COMANDOS(self):
        self.COMANDOS()
        self.G()

    # FUNÇÃO QUE DECIDE O QUE VAI FAZER DE ACORDO COM TOKEN.
    def G(self):
        # CONFERE SE O TOKEN CORRESPONDE A ALGUM DOS TOKENS ESPERADOS.
        if self.atualIgual(tt.SE):
            self.LISTA_COMANDOS()
        elif self.atualIgual(tt.WHILE):
            self.LISTA_COMANDOS()
        elif self.atualIgual(tt.READ):
            self.LISTA_COMANDOS()
        elif self.atualIgual(tt.WRITE):
            self.LISTA_COMANDOS()
        elif self.atualIgual(tt.IDENT):
            self.LISTA_COMANDOS()
        else:
            pass

    # FUNÇÃO QUE DECIDE O QUE VAI FAZER DE ACORDO COM TOKEN.
    def COMANDOS(self):
        try:# CONFERE SE O TOKEN CORRESPONDE A ALGUM DOS TOKENS ESPERADOS, E CONTINUA A GRAMATICA.
            if self.atualIgual(tt.SE):
                self.IF()
            elif self.atualIgual(tt.WHILE):
                self.WHILE()
            elif self.atualIgual(tt.READ):
                self.READ()
            elif self.atualIgual(tt.WRITE):
                self.WRITE()
            elif self.atualIgual(tt.IDENT):
                self.ATRIB()
            else:
                # CASO NÃO SEJA NENHUM, LISTA TODAS AS POSSIBILIDADES PARA COMPILAR COM SUCESSO NO TERMINAL.
                self.mensagemERRO(tt.SE)
                self.mensagemERRO(tt.WHILE)
                self.mensagemERRO(tt.READ)
                self.mensagemERRO(tt.WRITE)
                self.mensagemERRO(tt.IDENT)
                # E ENTRA NO MODOPANICO PARA ENTRAR NO EXCEPTION.
                self.modoPanico()
        except:
            self.get_FOLLOW_COMANDOS()

    # FUNÇÃO QUE PEGA O FOLLOW DE COMANDOS
    def get_FOLLOW_COMANDOS(self):
        if self.tokenAtual.classe in self.FOLLOW_COMANDOS: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.WHILE[0]: # VERIFICA SE TOKEN É "while" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.WRITE[0]: # VERIFICA SE TOKEN É "write" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.IDENT[0]: # VERIFICA SE TOKEN É "id" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.READ[0]: # VERIFICA SE TOKEN É "read" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.SE[0]: # VERIFICA SE TOKEN É "if" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_COMANDOS()

    # FUNÇÃO PARA REALIZAR UM IF CASO O TOKEN FOR UM SE
    def IF(self):
        try:
            self.consome(tt.SE) # CONSOME O TOKEN "if".
            self.consome(tt.OPABREP)# CONSOME O TOKEN "(".
            self.EXPR()
            self.consome(tt.OPFECHAP)# CONSOME O TOKEN ")".
            self.C_COMP()
            self.H()
        except:
            self.get_FOLLOW_IF()

    # FUNÇÃO QUE PEGA O FOLLOW DE SE
    def get_FOLLOW_IF(self):
        if self.tokenAtual.classe in self.FOLLOW_IF: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.WHILE[0]: # VERIFICA SE TOKEN É "while" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.WRITE[0]: # VERIFICA SE TOKEN É "write" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.IDENT[0]: # VERIFICA SE TOKEN É "id" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.READ[0]: # VERIFICA SE TOKEN É "read" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.SE[0]: # VERIFICA SE TOKEN É "if" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_IF()

    # FUNÇÃO PARA REALIZAR UM ELSE CASO O TOKEN FOR UM SENAO.
    def H(self):
        try:
            if self.atualIgual(tt.SENAO):# VERIFICA E CONSOME O TOKEN "else".
                self.consome(tt.SENAO)
                self.C_COMP()
            else:
                pass
        except:
            self.get_FOLLOW_H()

    # FUNÇÃO QUE PEGA O FOLLOW DE H
    def get_FOLLOW_H(self):
        if self.tokenAtual.classe in self.FOLLOW_H: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.WHILE[0]: # VERIFICA SE TOKEN É "while" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.WRITE[0]: # VERIFICA SE TOKEN É "write" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.IDENT[0]: # VERIFICA SE TOKEN É "id" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.READ[0]: # VERIFICA SE TOKEN É "read" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.SE[0]: # VERIFICA SE TOKEN É "if" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_H()

    # FUNÇÃO PARA REALIZAR UM WHILE CASO O TOKEN FOR UM ENQUANTO.
    def WHILE(self):
        try:
            self.consome(tt.WHILE) # CONSOME O TOKEN "while".
            self.consome(tt.OPABREP) # CONSOME O TOKEN "(".
            self.EXPR()
            self.consome(tt.OPFECHAP) # CONSOME O TOKEN ")".
            self.C_COMP()
        except:
            self.get_FOLLOW_WHILE()

    # FUNÇÃO QUE PEGA O FOLLOW DE WHILE
    def get_FOLLOW_WHILE(self):
        if self.tokenAtual.classe in self.FOLLOW_WHILE: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.WHILE[0]: # VERIFICA SE TOKEN É "while" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.WRITE[0]: # VERIFICA SE TOKEN É "write" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.IDENT[0]: # VERIFICA SE TOKEN É "id" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.READ[0]: # VERIFICA SE TOKEN É "read" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.SE[0]: # VERIFICA SE TOKEN É "if" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_WHILE()

    # FUNÇÃO PARA REALIZAR UM READ CASO O TOKEN FOR UM LEIA
    def READ(self):
        try:
            self.consome(tt.READ) # CONSOME O TOKEN "read".
            self.consome(tt.OPABREP) # CONSOME O TOKEN "(".
            self.LIST_ID()
            self.consome(tt.OPFECHAP) # CONSOME O TOKEN ")".
            self.consome(tt.OPPV) # CONSOME O TOKEN ";".
        except:
            self.get_FOLLOW_READ()

    # FUNÇÃO QUE PEGA O FOLLOW DE READ
    def get_FOLLOW_READ(self):
        if self.tokenAtual.classe in self.FOLLOW_READ: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.WHILE[0]: # VERIFICA SE TOKEN É "while" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.WRITE[0]: # VERIFICA SE TOKEN É "write" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.IDENT[0]: # VERIFICA SE TOKEN É "id" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.READ[0]: # VERIFICA SE TOKEN É "read" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.SE[0]: # VERIFICA SE TOKEN É "if" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_READ()

    # FUNÇÃO QUE PEGA UMA ATRIBUIÇÃO NO CODIGO.
    def ATRIB(self):
        try:
            self.consome(tt.IDENT) # CONSOME O TOKEN "id".
            self.consome(tt.ATRIB) # CONSOME O TOKEN ":=".
            self.EXPR()
            self.consome(tt.OPPV) # CONSOME O TOKEN ";".
        except:
            self.get_FOLLOW_ATRIB()

    # FUNÇÃO QUE PEGA O FOLLOW DE ATRIB
    def get_FOLLOW_ATRIB(self):
        if self.tokenAtual.classe in self.FOLLOW_ATRIB: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.WHILE[0]: # VERIFICA SE TOKEN É "while" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.WRITE[0]: # VERIFICA SE TOKEN É "write" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.IDENT[0]: # VERIFICA SE TOKEN É "id" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.READ[0]: # VERIFICA SE TOKEN É "read" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.SE[0]: # VERIFICA SE TOKEN É "if" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_ATRIB()

    # FUNÇÃO PARA REALIZAR UM WRITE CASO O TOKEN FOR UM ESCREVA.
    def WRITE(self):
        try:
            self.consome(tt.WRITE) # CONSOME O TOKEN "write".
            self.consome(tt.OPABREP) # CONSOME O TOKEN "(".
            self.LIST_W()
            self.consome(tt.OPFECHAP) # CONSOME O TOKEN ")".
            self.consome(tt.OPPV) # CONSOME O TOKEN ";".
        except:
            self.get_FOLLOW_WRITE()

    # FUNÇÃO QUE PEGA O FOLLOW DE WRITE
    def get_FOLLOW_WRITE(self):
        if self.tokenAtual.classe in self.FOLLOW_WRITE: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.WHILE[0]: # VERIFICA SE TOKEN É "while" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.WRITE[0]: # VERIFICA SE TOKEN É "write" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.IDENT[0]: # VERIFICA SE TOKEN É "id" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.READ[0]: # VERIFICA SE TOKEN É "read" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.SE[0]: # VERIFICA SE TOKEN É "if" E CONTINUA A GRAMATICA.
                self.LISTA_COMANDOS()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_WRITE()

    # FUNÇÃO QUE OLHA O QUE TEM DENTRO DE UM WRITE.
    def LIST_W(self):
        self.ELEM_W()
        self.L()

    def L(self):
        if self.atualIgual(tt.OPVIRG):# VERIFICA SE PEGOU O TOKEN "else" E CONSOME O TOKEN.
            self.consome(tt.OPVIRG)
            self.LIST_W()
        else:
            pass

    # FUNÇÃO QUE OLHA SE O WRITE POSSUI UMA CADEIA DE CARACTER OU UMA EXPPRESSÃO.
    def ELEM_W(self):
        try:
            if self.atualIgual(tt.CADCARACTER): # VERIFICA SE PEGOU O TOKEN "cadeia de caracter" E CONSOME O TOKEN.
                self.consome(tt.CADCARACTER)
            else:
                self.EXPR() # CASO NAO SEJA UMA CADEIA DE CARACTER ELE ENTRA NA FUNÇÃO DE EXPRESSOES.
        except:
            self.get_FOLLOW_ELEM_W()

    # FUNÇÃO QUE PEGA O FOLLOW DE ELEM_W
    def get_FOLLOW_ELEM_W(self):
        if self.tokenAtual.classe in self.FOLLOW_ELEM_W: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.OPFECHAP[0]: # VERIFICA SE TOKEN É ")" E CONTINUA A GRAMATICA.
                self.consome(tt.OPFECHAP)
            elif self.tokenAtual.classe == tt.OPPV[0]: # VERIFICA SE TOKEN É ";" E CONTINUA A GRAMATICA.
                self.consome(tt.OPPV)
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_ELEM_W()

    # FUNÇÃO QUE LE A EXPRESSAO DO CODIGO.
    def EXPR(self):
        self.SIMPLES()
        self.P()

    # FUNÇÃO QUE VERIFICA E CONSOME SIMBOLOS MATEMATICOS.
    def P(self):
        try:
            if self.atualIgual(tt.OPIGUAL):
                self.consome(tt.OPIGUAL)
                self.SIMPLES()
            elif self.atualIgual(tt.OPMENOR):
                self.consome(tt.OPMENOR)
                self.SIMPLES()
            elif self.atualIgual(tt.OPMAIOR):
                self.consome(tt.OPMAIOR)
                self.SIMPLES()
            elif self.atualIgual(tt.OPMENORI):
                self.consome(tt.OPMENORI)
                self.SIMPLES()
            elif self.atualIgual(tt.OPMAIORI):
                self.consome(tt.OPMAIORI)
                self.SIMPLES()
            elif self.atualIgual(tt.OPDIF):
                self.consome(tt.OPDIF)
                self.SIMPLES()
            else:
                pass
        except:
            self.get_FOLLOW_P()

    # FUNÇÃO QUE PEGA O FOLLOW DE P
    def get_FOLLOW_P(self):
        if self.tokenAtual.classe in self.FOLLOW_P: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.OPFECHAP[0]: # VERIFICA SE TOKEN É ")" E CONTINUA A GRAMATICA.
                self.FAT()
            elif self.tokenAtual.classe == tt.OPPV[0]: # VERIFICA SE TOKEN É ";" E CONTINUA A GRAMATICA.
                self.consome(tt.OPPV)
            elif self.tokenAtual.classe == tt.OPVIRG[0]: # VERIFICA SE TOKEN É "," E CONTINUA A GRAMATICA.
                self.consome(tt.OPPV)
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_P()

    def SIMPLES(self):
        self.TERMO()
        self.R()

    # FUNÇÃO QUE CONSOME OS TOKENS IGUALDADE E DESIGUALDADE ENTRE CONSTANTES E ID.
    def R(self):
        try:
            if self.atualIgual(tt.OPMAIS):
                self.consome(tt.OPMAIS)
                self.SIMPLES()
            elif self.atualIgual(tt.OPMENOS):
                self.consome(tt.OPMENOS)
                self.SIMPLES()
            else:
                pass
        except:
            self.get_FOLLOW_R()

    # FUNÇÃO QUE PEGA O FOLLOW DE R
    def get_FOLLOW_R(self):
        if self.tokenAtual.classe in self.FOLLOW_R: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.OPFECHAP[0]: # VERIFICA SE TOKEN É ")" E CONTINUA A GRAMATICA.
                self.FAT()
            elif self.tokenAtual.classe == tt.OPPV[0]: # VERIFICA SE TOKEN É ";" E CONTINUA A GRAMATICA.
                self.consome(tt.OPPV)
            elif self.tokenAtual.classe == tt.OPVIRG[0]: # VERIFICA SE TOKEN É "," E CONTINUA A GRAMATICA.
                self.consome(tt.OPPV)
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_R()

    def TERMO(self):
        self.FAT()
        self.S()

    # FUNÇÃO QUE CONSOME OS TOKENS MATEMATICOS ENTRE CONSTANTES E ID.
    def S(self):
        try:
            if self.atualIgual(tt.OPMULT):
                self.consome(tt.OPMULT)
                self.SIMPLES()
            elif self.atualIgual(tt.OPDIV):
                self.consome(tt.OPDIV)
                self.SIMPLES()
            else:
                pass
        except:
            self.get_FOLLOW_S()

    # FUNÇÃO QUE PEGA O FOLLOW DE S
    def get_FOLLOW_S(self):
        if self.tokenAtual.classe in self.FOLLOW_S: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.OPFECHAP[0]: # VERIFICA SE TOKEN É ")" E CONTINUA A GRAMATICA.
                self.FAT()
            elif self.tokenAtual.classe == tt.OPPV[0]: # VERIFICA SE TOKEN É ";" E CONTINUA A GRAMATICA.
                self.consome(tt.OPPV)
            elif self.tokenAtual.classe == tt.OPVIRG[0]: # VERIFICA SE TOKEN É "," E CONTINUA A GRAMATICA.
                self.consome(tt.OPPV)
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_S()

    # FUNÇÃO QUE CONSOME DEPOIS DE UMA ATRIBUIÇÃO.
    def FAT(self):
        try:
            if self.atualIgual(tt.CONST):
                self.consome(tt.CONST)
            elif self.atualIgual(tt.OPABREP):
                self.consome(tt.OPABREP)
                self.EXPR()
                self.consome(tt.OPFECHAP)
            elif self.atualIgual(tt.VERDADEIRO):
                self.consome(tt.VERDADEIRO)
            elif self.atualIgual(tt.FALSO):
                self.consome(tt.FALSO)
            elif self.atualIgual(tt.OPNEG):
                self.consome(tt.OPNEG)
                self.FAT()
            elif self.atualIgual(tt.IDENT):
                self.consome(tt.IDENT)
            else:
                # CASO NÃO SEJA NENHUM, LISTA TODAS AS POSSIBILIDADES PARA COMPILAR COM SUCESSO NO TERMINAL.
                self.mensagemERRO(tt.CONST)
                self.mensagemERRO(tt.OPABREP)
                self.mensagemERRO(tt.VERDADEIRO)
                self.mensagemERRO(tt.FALSO)
                self.mensagemERRO(tt.OPNEG)
                self.mensagemERRO(tt.IDENT)
                # E ENTRA NO MODOPANICO PARA ENTRAR NO EXCEPTION.
                self.modoPanico()
        except:
            self.get_FOLLOW_FAT()

    # FUNÇÃO QUE PEGA O FOLLOW DE FAT
    def get_FOLLOW_FAT(self):
        if self.tokenAtual.classe in self.FOLLOW_FAT: # CONFERE SE O TOKEN E UM DOS FOLLOWS DA FUNÇÃO.
            if self.tokenAtual.classe == tt.OPMAIS[0]: # VERIFICA SE TOKEN É "+" E CONTINUA A GRAMATICA.
                self.R()
            elif self.tokenAtual.classe == tt.OPMULT[0]: # VERIFICA SE TOKEN É "*" E CONTINUA A GRAMATICA.
                self.S()
            elif self.tokenAtual.classe == tt.FIMARQ[0]:
                return
        else: # CASO CONTRARIO PEGA OUTRO TOKEN E CHAMA A FUNÇÃO FOLLOWS DENOVO.
            self.tokenAtual = self.lex.getToken()
            self.get_FOLLOW_FAT()

    # FUNÇÃO QUE DA PRINT DA TABELA NO TERMINAL.
    def printTabela(self, nome):
        controle = 0
        tipo = ''
        linha = ''
        aux = []
        escrita = []
        for i in range(len(self.vetTabela) - 1, -1, -1):
            if type(self.vetTabela[i]) is list:
                controle = 1
                tipo = self.vetTabela[i][0]
                linha = self.vetTabela[i][1]
            if controle == 1 and type(self.vetTabela[i]) is str:
                aux.append([self.vetTabela[i], tipo, linha])
        aux.pop()        
        for i in aux:
            escrita.append("Variável '%s' do tipo '%s' na linha %d" % (i[0], i[1], i[2])+"\n")

        arq = open('Tabela_Simbolos_'+nome, 'w')
        arq.writelines(escrita)
        arq.close()

if __name__ == "__main__":
    param = sys.argv
    if param[1] == '-t':
        nome = param[2]
        parser = Sintatico(nome)
        parser.interprete(nome)
    else:
        nome = param[1]
        parser = Sintatico(nome)
        parser.interprete(nome)
