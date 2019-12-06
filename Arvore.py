import sys
class Arvore:
    def __init__(self, simbolo, esq = None, dir = None):
        self.raiz = simbolo
        self.esq = esq
        self.dir = dir

class Pilha:
    OPERADOR = ['+', '-', '/', '*']
    OPERANDO = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    VALORES = OPERADOR + OPERANDO

    def __init__(self):
        self.pilha = []

    #Função que monta a sub arvore, sempre da dois pop na pilha e verifica se o valor do pop ja é uma subárvore, caso seja,
        #apenas é atrabuida a função, caso nao seja, é criado uma subárvore tendo com raiz esse valor
    #Por fim é empilhado novamente na pilha
    def inserePilha(self, simbolo):
        dir = self.pilha.pop(-1)
        esq = self.pilha.pop(-1)
        if dir in self.VALORES:
            dir = Arvore(dir)

        if esq in self.VALORES:
            esq = Arvore(esq)

        arv = Arvore(simbolo, esq, dir)
        self.pilha.append(arv)

    #Enquanto vier numeros, vai empilhando, assim que vier um iperador, chama a função inserePilha e com paramtro
        #simbolo da operação
    def insereArvore(self, expressao):
        for i in expressao:
            if i in self.OPERADOR:
                self.inserePilha(i)
            else:
                self.pilha.append(i)

    #Caminhamento pos ordem na arvore e executando as operações. Passa-se uma lista por parametro que vai adicionando
        #os elementos até que encontre um operador, assim que encontrado, é dado dois pop, feita a operação e inserido
        #o resultado de volta na lista
    def posOrder(self, atual, lista):
        if atual is None:
            return
        self.posOrder(atual.esq, lista)
        self.posOrder(atual.dir, lista)
        if atual.raiz == '+':
            op1 = lista.pop(-1)
            op2 = lista.pop(-1)
            lista.append(str(float(op2)+float(op1)))

        elif atual.raiz == '-':
            op1 = lista.pop(-1)
            op2 = lista.pop(-1)
            lista.append(str(float(op2)-float(op1)))

        elif atual.raiz == '*':
            op1 = lista.pop(-1)
            op2 = lista.pop(-1)
            lista.append(str(float(op2)*float(op1)))

        elif atual.raiz == '/':
            op1 = lista.pop(-1)
            op2 = lista.pop(-1)
            lista.append(str(float(op2)/float(op1)))
        else:
            lista.append(atual.raiz)

    #Função que le do arquivo e armazena caracter por caracter
    def processaDados(self, expressao):
        lista = []
        for i in expressao:
            lista.append(i)

        return lista

    #Função padrão de leitura de arquivo
    def leituraArq(self, nome):
        arquivo = open(nome, 'r')
        if arquivo is None:
            return

        texto = ''
        for linhas in arquivo:
            texto += linhas

        arquivo.close()
        return self.processaDados(texto)


if __name__ == "__main__":
    param = sys.argv
    p = Pilha()
    expressao = p.leituraArq(param[1])
    p.insereArvore(expressao)
    saida = []
    p.posOrder(p.pilha[0], saida)
    print(saida[0])