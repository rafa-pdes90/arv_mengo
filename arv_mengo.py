#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import os
import random
from tkinter import *


class Nodo:
    # True(1) para nodo black; False(0) para nodo red; (2) para nodo "double black".
    def __init__(self, item, black, esq = None, dir = None):
        self.item = item
        self.black = black
        self.esq = esq
        self.dir = dir

        
class ArvoreBinaria:
    # itensRecentes sao os nodos alterados/criados na última inserçao ou remoçao.
    # O primeiro elemento é o principal,
    # por ser ou o nodo inserido ou o substituto daquele que foi removido.
    def __init__(self, raiz = None):
        self.raiz = raiz
        if (raiz != None):
            self.itensRecentes = [raiz.item, None]
        else:
            self.itensRecentes = [None]
    # Nodo nodo
    def criarNodo(self, item, black):
        return Nodo(item, black)
    # Reseta os itensRecentes
    def clearRecentes(self):
        self.itensRecentes = [None]
    # Calcula a altura de nodos pretos somente,
    # a qual deve ser constante para os ramos esquerdos e direitos de uma árvore rubro-negra.
    def getBlackAltura(self, raiz):
        if (raiz == None):
            return 0
        return raiz.black + max(self.getBlackAltura(raiz.esq), self.getBlackAltura(raiz.dir))
    # Calcula a diferença de altura de nodos pretos entre os ramos esquerdos e direitos
    def getBlackBalanco(self, raiz):
        if (raiz == None):
            return 0
        return self.getBlackAltura(raiz.esq) - self.getBlackAltura(raiz.dir)
    # Calcula a altura total
    def getAltura(self, raiz):
        if (raiz == None):
            return 0
        return 1 + max(self.getAltura(raiz.esq), self.getAltura(raiz.dir))
    # Calcula o balanceamento total, o qual nao precisa estar tao preciso quanto a AVL.
    def getBalanco(self, raiz):
        if (raiz == None):
            return 0
        return self.getAltura(raiz.esq) - self.getAltura(raiz.dir)
    # Rotaciona à direita
    def rotacaoDir(self, velhaRaiz):
        novaRaiz = velhaRaiz.esq
        velhaRaiz.esq, novaRaiz.dir = novaRaiz.dir, velhaRaiz
        if (velhaRaiz.item == self.itensRecentes[0]):
            self.itensRecentes[0] = novaRaiz.item
        self.itensRecentes.extend([velhaRaiz.item, novaRaiz.item, velhaRaiz.esq])
        return novaRaiz
    # Rotaciona à esquerda
    def rotacaoEsq(self, velhaRaiz):
        novaRaiz = velhaRaiz.dir
        velhaRaiz.dir, novaRaiz.esq = novaRaiz.esq, velhaRaiz
        if (velhaRaiz.item == self.itensRecentes[0]):
            self.itensRecentes[0] = novaRaiz.item
        self.itensRecentes.extend([velhaRaiz.item, novaRaiz.item, velhaRaiz.dir])
        return novaRaiz
    # True se o nodo é black ou None, senao false
    # Nodos "None" sao sempre black
    def isNodoBlack(self, nodo):
        return (nodo.black if nodo != None else True)
    # True se o nodo é red, senao false
    def isNodoRed(self, nodo):
        return (not nodo.black if nodo != None else False)
    # Retorna o nodo com o atributo black modificado (padrao: True, ou Black)
    def setNodoToBlack(self, nodo, black = True):
        if (nodo != None and nodo.item != None):
            nodo.black = black
            self.itensRecentes.append(nodo.item)
            return nodo
        return
    # Retorna o nodo com o atributo black modificado (padrao: False, ou Red)
    def setNodoToRed(self, nodo, black = False):
        if (nodo != None and nodo.item != None):
            nodo.black = black
            self.itensRecentes.append(nodo.item)
            return nodo
        return
    # Retorna os dois nodos de entrada, com seus atributos black trocados
    def swapNodoCor(self, nodo1, nodo2): ######################
        nodo1_blackness = self.isNodoBlack(nodo1)
        nodo1 = self.setNodoToBlack(nodo1, black = self.isNodoBlack(nodo2))
        nodo2 = self.setNodoToBlack(nodo2, black = nodo1_blackness)
        self.itensRecentes.extend([nodo1.item, nodo2.item])
        return nodo1, nodo2
    # Inicializa a recursao da inserçao
    # Raiz sempre é BLACK.
    def inserir(self, item, raiz):
        raiz, caso = self.inserirMengo(item, raiz)
        raiz.black = True
        self.itensRecentes.append(None)
        return raiz
    # Inserçao binária recursiva comum, adicionada de balanceamento para a árvore rubro-negra
    # Sobre a variável "caso":
    # Se 0 significa que nao há mais nenhuma modificaçao necessária
    # Se 1 significa que o nodo atual(raiz) é o pai do nodo inserido
    # Se 2 significa que o nodo atual(raiz) é o avô do nodo inserido
    def inserirMengo(self, item, raiz):
        if (raiz == None): # O item nao existe, logo um nodo correspondente é criado. Sempre RED.
            nodo = self.criarNodo(item, False)
            self.itensRecentes = [item]
            return nodo, 1
        if (item < raiz.item): # Recursa para o ramo esquerdo
            raiz.esq, caso = self.inserirMengo(item, raiz.esq)
            tio = raiz.dir
        elif (item > raiz.item): # Recursa para o ramo direito
            raiz.dir, caso = self.inserirMengo(item, raiz.dir)
            tio = raiz.esq
        else: # Item repetido, logo Caso = 0
            self.itensRecentes = []
            return raiz, 0
        
        if (caso == 1):
            if (raiz.black): # Se o pai é preto, nao precisa modificar mais nada.
                caso = 0
            else: # Senao, vai depender do tio, logo deve-se retornar ao avô.
                caso = 2
        elif (caso == 2):
            if (self.isNodoBlack(tio)): # Se o tio é preto, a operaçao é similar a da árvore AVL
                balanco = self.getBalanco(raiz)
                if (balanco > 1): # Desbalanceada para à esquerda
                    if (item > raiz.esq.item): #Left-Right, senao Left-Left
                        raiz.esq = self.rotacaoEsq(raiz.esq)
                    raiz = self.rotacaoDir(raiz)
                    raiz.dir, raiz = self.swapNodoCor(raiz.dir, raiz) # A diferença para à AVL está nesse troca de cor entre raiz e tio
                    caso = 0 # Ao fim, nao é necessária mais nenhuma modificaçao
                elif (balanco < -1): # Desbalanceada para à direita
                    if (item < raiz.dir.item): #Right-Left, senao Right-Right
                        raiz.dir = self.rotacaoDir(raiz.dir)
                    raiz = self.rotacaoEsq(raiz)
                    raiz.esq, raiz = self.swapNodoCor(raiz.esq, raiz) # A diferença para à AVL está nesse troca de cor entre raiz e tio
                    caso = 0 # Ao fim, nao é necessária mais nenhuma modificaçao
            else: # Se o tio é vermelho, deve-se pintar pai e tio de preto, o avô de vermelho, e considerar o avô como o novo filho
                raiz.esq = self.setNodoToBlack(raiz.esq)
                raiz.dir = self.setNodoToBlack(raiz.dir)
                raiz = self.setNodoToRed(raiz)
                caso = 1 # Avô (nodo atual) vira filho.
        return raiz, caso
    # Retorna o nodo com o atributo black = 2
    # É um nodo especial para ser usado, temporariamente, no processo de remoçao
    def setNodoToDoubleBlack(self, nodo):
        if (nodo == None): return self.criarNodo(None, 2)
        nodo.black = 2
        self.itensRecentes.append(nodo.item)
        return nodo
    # Testa se o nodo é "double black", ou black = 2
    def isNodoDoubleBlack(self, nodo):
        return (nodo.black == 2 if nodo != None else False)
    # Funçao auxiliar da remocao
    # Retorna o maior nodo no ramo esquerdo
    def delNodoSubstituto(self, nodo):
        if (nodo.dir != None): return self.delNodoSubstituto(nodo.dir)
        return nodo
    # Inicializa a recursao da remoçao
    # Raiz sempre é BLACK
    def deletar(self, item, raiz):
        if (raiz == None): return
        self.itensRecentes = []
        itemAtual = raiz.item
        raiz = self.deletarMengo(item, raiz)
        if (raiz.item == None):
            del raiz
            return
        elif (raiz.item == itemAtual):
            if (raiz.black):
                self.itensRecentes[:] = [item for item in self.itensRecentes if item != raiz.item]
        raiz.black = True
        self.itensRecentes.append(self.itensRecentes.pop(0))
        self.itensRecentes.insert(0, None)
        return raiz
    # Remoçao binária comum, adicionada de reparaçao do balanceamento para a árvore rubro-negra
    # Certo momento é preciso considerar None como sendo um nodo None com black = 2,
    # ou seja, um None double black, porém é logo substituído por None.
    def deletarMengo(self, item, raiz):
        if (raiz == None): # Item nao encontrado
            self.itensRecentes.append(None)
            return raiz
        if (raiz.item == None): # nodo None double black
            return raiz
        if (item < raiz.item): # Recursa para à esquerda
            raiz.esq = self.deletarMengo(item, raiz.esq)
        elif (item > raiz.item): # Recursa para à direita
            raiz.dir = self.deletarMengo(item, raiz.dir)
        else:
            if (raiz.esq != None and raiz.dir != None): # Item localizado, porém contem ambos os ramos
                subs = self.delNodoSubstituto(raiz.esq) # Encontra-se o maior subsituto no ramo esquerdo
                self.itensRecentes.append(subs.item)
                raiz.item = subs.item # Troca-se os valores do atual e o substituo
                raiz.esq = self.deletarMengo(subs.item, raiz.esq) # Recursa, no ramo esquerdo, para deletar o novo nodo contendo o valor de item
            else: # Item (re)localizado, com pelo menos um ramo None
                if (raiz.esq == None): subs = raiz.dir # O substituto será uma filho "válido", se existente, senao None
                else: subs = raiz.esq
                if (subs != None):
                    self.itensRecentes.append(subs.item)
                else:
                    self.itensRecentes.append(None)
                if (self.isNodoRed(raiz) or self.isNodoRed(subs)): # Se ou filho substituto ou o atual for RED, basta setar o substituto para BLACK.
                    subs = self.setNodoToBlack(subs)
                else: subs = self.setNodoToDoubleBlack(subs) # Senao, o substituto torna-se double black(mesmo se for None), e será preciso rebalancear.
                
                del raiz
                return subs
        #if (raiz != None):
        # Rebalanceamento
        # Primeiro identifica-se o irmao e seu ramo
        irmao = None
        if (self.isNodoDoubleBlack(raiz.esq)):
            irmao = raiz.dir
            coxinha = True
        elif (self.isNodoDoubleBlack(raiz.dir)):
            irmao = raiz.esq
            coxinha = False
        if (irmao != None): # Se há um double black, haverá um irmao válido.
            if (irmao.black): # Se o irmao for BLACK
                if (coxinha): raiz.esq = self.setNodoToBlack(raiz.esq) # Desfaz-se a condiçao de double black do substituto
                else: raiz.dir = self.setNodoToBlack(raiz.dir)
                if (self.isNodoBlack(irmao.esq) and self.isNodoBlack(irmao.dir)): # Se os sobrinhos forem ambos BLACK (ou None)
                    irmao = self.setNodoToRed(irmao) # Irmao é colorido em RED
                    if (self.isNodoBlack(raiz)): raiz = self.setNodoToDoubleBlack(raiz) # Pai se torna double black se for black
                    else: raiz = self.setNodoToBlack(raiz) # Ou black se for RED (ou seja, nível de black é aumentado em 1)
                else: # Se pelo menos um sobrinho for vermelho
                    if (coxinha): # Irmao no ramo direito
                        if (self.isNodoBlack(irmao.dir)): # Right-Left, senao Right-Right
                            irmao = self.rotacaoDir(irmao)
                            irmao.dir, irmao = self.swapNodoCor(irmao.dir, irmao)
                        raiz.dir = irmao
                        raiz = self.rotacaoEsq(raiz)
                        raiz.esq, raiz = self.swapNodoCor(raiz.esq, raiz)
                        raiz.dir = self.setNodoToBlack(raiz.dir, black = self.isNodoBlack(raiz.esq))
                    else: # Irmao no ramo esquerdo
                        if (self.isNodoBlack(irmao.esq)): # Left-Right, senao Left-Left
                            irmao = self.rotacaoEsq(irmao)
                            irmao.esq, irmao = self.swapNodoCor(irmao.esq, irmao)
                        raiz.esq = irmao
                        raiz = self.rotacaoDir(raiz)
                        raiz.dir, raiz = self.swapNodoCor(raiz.dir, raiz)
                        raiz.esq = self.setNodoToBlack(raiz.esq, black = self.isNodoBlack(raiz.dir))
            # Se o irmao for RED, é feita algumas operaçoes de rotaçao e swap de cor,
            # para novamente se visitar o ramo do nodo substituto
            # Note que o nodo double-black nao foi desfeito ainda.
            else: 
                if (coxinha): # Se irmao no ramo esquerdo
                    raiz = self.rotacaoEsq(raiz)
                    raiz.esq, raiz = self.swapNodoCor(raiz.esq, raiz)
                    raiz.dir = self.setNodoToBlack(raiz.dir)
                    raiz.esq = self.deletarMengo(item, raiz.esq)
                else: # Se irmao no ramo direito
                    raiz = self.rotacaoDir(raiz)
                    raiz.dir, raiz = self.swapNodoCor(raiz.dir, raiz)
                    raiz.esq = self.setNodoToBlack(raiz.esq)
                    raiz.dir = self.deletarMengo(item, raiz.dir)
        return raiz
    # Reconstroi a árvore a partir de uma lista produzida pela funçao 'listaArvoreRB', abaixo
    def reinserir(self, item, black, raiz):
        if (raiz == None): return self.criarNodo(item, black)
        if (item < raiz.item):
            raiz.esq = self.reinserir(item, black, raiz.esq)
        elif (item > raiz.item):
            raiz.dir = self.reinserir(item, black, raiz.dir)
        return raiz
    def isFamiliaBlack(self, raiz):
        if (raiz == None or raiz.esq == None or raiz.dir == None): return False
        return self.isNodoBlack(raiz) and self.isNodoBlack(raiz.esq) and self.isNodoBlack(raiz.dir) and self.isNodoBlack(raiz.esq.esq) and self.isNodoBlack(raiz.esq.dir) and self.isNodoBlack(raiz.dir.esq) and self.isNodoBlack(raiz.dir.dir)
    def redistribuirCores(self, raiz):
        if (raiz == None): return
        fila = []
        filaAux = [raiz]
        familiasRed = False
        while filaAux:
            for nodo in filaAux:
                if (not self.isFamiliaBlack(nodo)):
                    familiasRed = True
            while filaAux:
                nodo = filaAux.pop()
                if (not familiasRed):
                    nodo.esq = self.setNodoToRed(nodo.esq)
                    nodo.dir = self.setNodoToRed(nodo.dir)
                    fila.append(nodo.esq)
                    fila.append(nodo.dir)
                else:
                    fila.append(nodo)
            familiasRed = False
            while fila:
                nodo = fila.pop()
                if (nodo.esq != None):
                    filaAux.append(nodo.esq)
                if (nodo.dir != None):
                    filaAux.append(nodo.dir)
        return raiz
    def pesquisar(self, item, raiz):
        if (raiz != None):
            if (item == raiz.item):
                return raiz
            elif (item < raiz.item):
                return self.pesquisar(item, raiz.esq)
            else:
                return self.pesquisar(item, raiz.dir)
        return
    # "Visita" a árvore pelo método da busca em largura (BFS)
    # e salva os dados da lista necessários para reconstruçao:
    # itensRecentes; nodos e suas respectivas cores.
    def listaArvoreRB(self, raiz):
        if (raiz == None): return
        fila = [raiz]
        lista = [self.itensRecentes[:]]
        while fila:
            nodo = fila.pop(0)
            if (nodo.esq != None):
                fila.append(nodo.esq)
            if (nodo.dir != None):
                fila.append(nodo.dir)
            lista.append((nodo.item,nodo.black))
        return lista
    def listaArvoreBFS(self, raiz):
        if (raiz == None): return
        fila = [raiz]
        lista = []
        while fila:
            nodo = fila.pop(0)
            if (nodo.esq != None):
                fila.append(nodo.esq)
            if (nodo.dir != None):
                fila.append(nodo.dir)
            lista.append(nodo.item)
        return lista


class Aplicacao:
    # Inicializa a GUI do programa, além de variáveis úteis
    def __init__(self, pai):
        self.f1 = Frame(pai)
        self.f1.pack()
        self.l1 = Label(self.f1, text = "N:")
        self.l1.pack(side=LEFT)
        self.t1 = Entry(self.f1, justify = "center", width=7)
        self.t1.bind("<Return>", self.constroiArvore) 
        self.t1.pack(side=LEFT)
        self.b1 = Button(self.f1, text = "Inserir N", command = self.constroiArvore)
        self.b1.pack(side=LEFT)
        self.b2 = Button(self.f1, text = "Deletar N", state = "disabled", command = self.desconstroiArvore)
        self.b2.pack(side=RIGHT)
        self.b3 = Button(self.f1, text = "Buscar", state = "disabled", command = self.pesquisarNaArvore)
        self.b3.pack(side=RIGHT)
        self.b4 = Button(pai, text = "Criar árvore aleatória de N nodos", command = self.geraAleatoria)
        self.b4.pack()
        self.f2 = Frame(pai)
        self.f2.pack()
        self.b5 = Button(self.f2, text = "Desfazer", state = "disabled", command = self.desfazArvore)
        self.b5.pack(side=LEFT)
        self.b6 = Button(self.f2, text = "Refazer", state = "disabled", command = self.refazArvore)
        self.b6.pack(side=RIGHT)
        self.c1 = Canvas(pai,width=1024,height=768)
        self.c1.pack()
        self.HORIZONTAL = 1024
        self.VERTICAL = 768
        self.tamanho = 30
        self.arvoreBinaria = ArvoreBinaria()
        self.raiz = None
        self.bakArvores = [None]
        self.bakIndex = 0
        self.itemAchado = None
        self.desenhaArvore()
    def pesquisarNaArvore(self, *args):
        try:
            valor = int(self.t1.get())
        except Exception:
            return
        os.system('cls' if os.name == 'nt' else 'clear')
        nodo = self.arvoreBinaria.pesquisar(valor, self.raiz)
        if (nodo == None):
            print('Nodo', valor, 'nao localizado.')
        else:
            print('Nodo', valor, 'localizado.')
            self.itemAchado = valor
            self.desenhaArvore()
            self.itemAchado = None
    # Funçao de inserçao na árvore
    def constroiArvore(self, *args):
        try:
            valor = int(self.t1.get())
        except Exception:
            return
        os.system('cls' if os.name == 'nt' else 'clear')
        self.t1.delete(0, 'end')
        if self.raiz == None:
            print("Criando com raiz ", str(valor), "...")
            self.b2['state'] = 'normal'
            self.b3['state'] = 'normal'
            self.b5['state'] = 'normal'
        else:
            print("Inserindo", str(valor), "...")
        self.raiz = self.arvoreBinaria.inserir(valor, self.raiz)
        if (self.arvoreBinaria.itensRecentes[0] == None): # Se valor já existe
            self.itemAchado = valor
        self.mostrarBalanco()
        self.desenhaArvore()
        self.backupArvore()
        self.itemAchado = None
    # Funcao de remoçao na árvore
    def desconstroiArvore(self, *args):
        try:
            valor = int(self.t1.get())
        except Exception:
            return
        os.system('cls' if os.name == 'nt' else 'clear')
        self.t1.delete(0, 'end')
        print("Deletando", str(valor), "...")
        self.raiz = self.arvoreBinaria.deletar(valor, self.raiz)
        if (self.raiz == None):
            print("\nArvore esvaziada.")
            self.b2['state'] = 'disabled'
            self.b3['state'] = 'disabled'
        self.mostrarBalanco()
        self.desenhaArvore()
        self.backupArvore()
    # Funçao que gera uma árvore aleatória
    def geraAleatoria(self, *args):
        try:
            valor = int(self.t1.get())
            if (valor < 0): raise Exception
        except Exception:
            return
        os.system('cls' if os.name == 'nt' else 'clear')
        self.raiz = None
        if (valor == 0):
            print("\nArvore esvaziada.")
            self.t1.delete(0, 'end')
            self.b2['state'] = 'disabled'
            self.b3['state'] = 'disabled'
        else:
            print("Gerando árvore binária aleatória com", str(valor), "nodos...")
            for i in range(valor):
                self.raiz = self.arvoreBinaria.inserir(random.randint(10*valor,100*valor), self.raiz)
            self.mostrarBalanco()
            self.b2['state'] = 'normal'
            self.b3['state'] = 'normal'
            self.b5['state'] = 'normal'
        self.arvoreBinaria.clearRecentes()
        self.desenhaArvore()
        self.backupArvore()
        '''
        self.b5['state'] = 'normal'
        tamanhos = [random.randint(10,100) for i in range(100)]
        for tam in tamanhos:
            self.raiz = None
            for i in range(tam):
                self.raiz = self.arvoreBinaria.inserir(random.randint(10*tam,100*tam), self.raiz)
            teste = self.arvoreBinaria.listaArvoreBFS(self.raiz)
            self.desenhaArvore()
            i = 0
            total = len(teste)-2
            while (i < total):
                last = len(teste) - 1
                valor = teste.pop(random.randint(0,last))
                self.raiz = self.arvoreBinaria.deletar(valor, self.raiz)
                self.desenhaArvore()
                self.backupArvore()
                balanceado = self.checarBlackBalanco(self.raiz) != 0
                if (not balanceado):
                    print('Balanceada pela altura de nodos negros? ' + str(balanceado))
                i += 1
        if (self.raiz == None):
            self.b2['state'] = 'disabled'
            self.b3['state'] = 'disabled'
        else:
            self.b2['state'] = 'normal'
            self.b3['state'] = 'normal'
        '''
    # Funçao que reconstrói a árvore anterior, se existir
    def desfazArvore(self, *args):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Desfazendo a última alteraçao...")
        self.bakIndex -= 1
        listaArvore = self.bakArvores[self.bakIndex]
        self.raiz = None
        if (listaArvore != None):
            self.b2['state'] = 'normal'
            self.b3['state'] = 'normal'
            self.arvoreBinaria.itensRecentes = listaArvore[0]
            for dados in listaArvore[1:]:
                self.raiz = self.arvoreBinaria.reinserir(dados[0], dados[1], self.raiz)
            self.mostrarBalanco()
        else:
            self.b2['state'] = 'disabled'
            self.b3['state'] = 'disabled'
        if (self.bakIndex == 0):
            print("\nArvore esvaziada.")
            self.b5['state'] = 'disabled'
        self.b6['state'] = 'normal'
        self.desenhaArvore()
    # Funçao que refaz as árvores anteriormente desfeitas
    # desde que nao tenha ocorrido modificaçoes na anterior (atual)
    def refazArvore(self, *args):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Refazendo recentes alteraçoes...")
        self.bakIndex += 1
        listaArvore = self.bakArvores[self.bakIndex]
        self.raiz = None
        if (listaArvore == None):
            print("\nArvore esvaziada.")
            self.b2['state'] = 'disabled'
            self.b3['state'] = 'disabled'
        else:
            self.b2['state'] = 'normal'
            self.b3['state'] = 'normal'
            self.arvoreBinaria.itensRecentes = listaArvore[0]
            for dados in listaArvore[1:]:
                self.raiz = self.arvoreBinaria.reinserir(dados[0], dados[1], self.raiz)
            self.mostrarBalanco()
        self.b5['state'] = 'normal'
        if (self.bakIndex + 1 == len(self.bakArvores)):
            self.b6['state'] = 'disabled'
        self.desenhaArvore()
    # Salva a listaArvoreRB atual, para possibilitar o desfazer/refazer
    def backupArvore(self):
        if (self.raiz != self.bakArvores[self.bakIndex]):
            self.bakIndex += 1
            if (self.bakIndex < len(self.bakArvores)):
                self.bakArvores = self.bakArvores[0:self.bakIndex]
                self.b6['state'] = 'disabled'
            self.bakArvores.append(self.arvoreBinaria.listaArvoreRB(self.raiz))
    # Checa o balanço total da árvore.
    # Ou seja, se está entre [-1, 1]
    def checarBalanco(self, raiz, balanceado = True):
        if (raiz != None):
            balanceado *= self.checarBalanco(raiz.esq)
            balanceado *= self.checarBalanco(raiz.dir)
            if (balanceado):
                balanco = self.arvoreBinaria.getBalanco(raiz)
                if (balanco < -1) or (balanco > 1):
                    return False
        return balanceado
    # Checa o balanço de nodos pretos da árvore
    # Ou seja, se a altura de ambos os ramos é igual
    def checarBlackBalanco(self, raiz, balanceado = True):
        if (raiz != None):
            balanceado *= self.checarBlackBalanco(raiz.esq)
            balanceado *= self.checarBlackBalanco(raiz.dir)
            if (balanceado):
                balanco = self.arvoreBinaria.getBlackBalanco(raiz)
                if balanco != 0:
                    return False
        return balanceado
    # Mostra no console o resultado das checagens de balanço
    def mostrarBalanco(self):
        balanceado = self.checarBalanco(self.raiz) != 0
        print('\nBalanceada pela altura total? ' + str(balanceado))
        balanceado = self.checarBlackBalanco(self.raiz) != 0
        print('Balanceada pela altura de nodos negros? ' + str(balanceado))
    # Funçao que desenha a árvore no canvas
    def desenhaArvore(self):
        self.c1.delete(ALL)
        self.c1.create_rectangle(0, 0, self.HORIZONTAL, self.VERTICAL, fill="#2EAAB3")
        if (self.raiz != None):
            self.xmax = self.c1.winfo_width() - 40 #margem de 40
            self.ymax = self.c1.winfo_height()
            self.numero_linhas = self.arvoreBinaria.getAltura(self.raiz)
            x1 = int(self.xmax/2+20)
            y1 = int(self.ymax/(self.numero_linhas+1))
            self.desenhaNodo(self.raiz,x1,y1,1)
    # Funçao que desenha o nodo no canvas, complemento da funçao acima
    def desenhaNodo(self, nodo, posX, posY, linha):
        dy = self.ymax/(self.numero_linhas+1)
        numero_colunas = 2**(linha+1)
        dx = self.xmax/numero_colunas
        posFilhoY = posY + dy
        if (nodo.dir != None):
            posFilhoX = posX + dx
            self.c1.create_line(posX,posY,posFilhoX,posFilhoY,fill="white")
            self.desenhaNodo(nodo.dir,posFilhoX,posFilhoY,linha+1)
        if (nodo.esq != None):
            posFilhoX = posX - dx
            self.c1.create_line(posX,posY,posFilhoX,posFilhoY,fill="white")
            self.desenhaNodo(nodo.esq,posFilhoX,posFilhoY,linha+1)     
        x1 = int(posX-self.tamanho/2)
        y1 = int(posY-self.tamanho/2)
        x2 = int(posX+self.tamanho/2)
        y2 = int(posY+self.tamanho/2)
        if (self.itemAchado == None):
            if (nodo.item in self.arvoreBinaria.itensRecentes[1:-1]):
                self.c1.create_oval(x1-5,y1-5,x2+5,y2+5,fill='indigo')
            if (nodo.item == self.arvoreBinaria.itensRecentes[0]):
                self.c1.create_oval(x1-5,y1-5,x2+5,y2+5,fill='#5DFC0A')
            if (nodo.item == self.arvoreBinaria.itensRecentes[-1]):
                self.c1.create_oval(x1-5,y1-5,x2+5,y2+5,fill='magenta')
        elif (nodo.item == self.itemAchado):
            self.c1.create_oval(x1-5,y1-5,x2+5,y2+5,fill='gold')
        nodoCor = ("black" if self.arvoreBinaria.isNodoBlack(nodo) else "#E34234") ###############
        self.c1.create_oval(x1,y1,x2,y2,fill=nodoCor) ############
        self.c1.create_text(posX,posY,text=str(nodo.item),fill="white")
    
# Execuçao principal
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    root = Tk(None,None," Desenhando Uma Árvore Binária Rubro-Negra")
    root.geometry("1024x750")
    ap = Aplicacao(root)
    root.mainloop()
    os.system('cls' if os.name == 'nt' else 'clear')
