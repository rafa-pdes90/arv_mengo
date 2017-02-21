#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import os
import random
from tkinter import *
    
class Nodo:
    def __init__(self, item, black, esq = None, dir = None, alt = 1): ###############
        self.item = item
        self.black = black
        self.esq = esq
        self.dir = dir
        self.alt = alt
    def __str__(self):
        out = '{'
        if (self != None):
            out += ' ' + str(self.item) + ' [ '
            if (self.esq == None and self.dir == None):
                out += '-'
            else:
                if (self.esq != None):
                    out += str(self.esq.item)
                else:
                    out += '-'
                out += ' ; '
                if (self.dir != None):
                    out += str(self.dir.item)
                else:
                    out += '-'
            out += ' ] '
        return out + '}'

        
class ArvoreBinaria:
    def __init__(self, raiz = None):
        self.raiz = raiz
    def criarNodo(self, item, black): ########################
        return Nodo(item, black)
    def inicializarRaiz(self, item, black): #####################
        self.raiz = self.criarNodo(item, black)
        return self.raiz
    def estaVazia(self):
        return self.raiz == None
    def getBlackAltura(self, raiz): ###################
        if (raiz == None):
            return 0
        return raiz.black + max(self.getBlackAltura(raiz.esq), self.getBlackAltura(raiz.dir))
    def getBlackBalanco(self, raiz): ###################
        if (raiz == None):
            return 0
        return self.getBlackAltura(raiz.esq) - self.getBlackAltura(raiz.dir)
    def getAltura(self, raiz):
        if (raiz == None):
            return 0
        return raiz.alt
    def getBalanco(self, raiz):
        if (raiz == None):
            return 0
        return self.getAltura(raiz.esq) - self.getAltura(raiz.dir)
    def rotacaoDir(self, velhaRaiz):
        novaRaiz = velhaRaiz.esq
        velhaRaiz.esq, novaRaiz.dir = novaRaiz.dir, velhaRaiz
        velhaRaiz.alt = max(self.getAltura(velhaRaiz.esq), self.getAltura(velhaRaiz.dir)) + 1
        novaRaiz.alt = max(self.getAltura(novaRaiz.esq), self.getAltura(novaRaiz.dir)) + 1
        return novaRaiz
    def rotacaoEsq(self, velhaRaiz):
        novaRaiz = velhaRaiz.dir
        velhaRaiz.dir, novaRaiz.esq = novaRaiz.esq, velhaRaiz
        velhaRaiz.alt = max(self.getAltura(velhaRaiz.esq), self.getAltura(velhaRaiz.dir)) + 1
        novaRaiz.alt = max(self.getAltura(novaRaiz.esq), self.getAltura(novaRaiz.dir)) + 1
        return novaRaiz
    def isNodoBlack(self, nodo): ##########################
        return (nodo.black if nodo != None else True)
    def isNodoRed(self, nodo): ##########################
        return (not nodo.black if nodo != None else False)
    def setNodoToBlack(self, nodo, black = True): ################
        if (nodo != None and nodo.item != None):
            nodo.black = black
            return nodo
        return
    def setNodoToRed(self, nodo, black = False): ##############
        if (nodo != None and nodo.item != None):
            nodo.black = black
            return nodo
        return
    def swapNodoCor(self, nodo1, nodo2): ######################
        nodo1_blackness = self.isNodoBlack(nodo1)
        nodo1 = self.setNodoToBlack(nodo1, black = self.isNodoBlack(nodo2))
        nodo2 = self.setNodoToBlack(nodo2, black = nodo1_blackness)
        return nodo1, nodo2
    def inserir(self, item, raiz): ##################
        raiz, caso = self.inserirMengo(item, raiz)
        raiz.black = True
        return raiz
    def inserirMengo(self, item, raiz): ###################
        if (raiz == None):
            return self.criarNodo(item, False), 1
        if (item < raiz.item):
            raiz.esq, caso = self.inserirMengo(item, raiz.esq)
            tio = raiz.dir
        elif (item > raiz.item):
            raiz.dir, caso = self.inserirMengo(item, raiz.dir)
            tio = raiz.esq
        else:
            return raiz, 0
        raiz.alt = max(self.getAltura(raiz.esq), self.getAltura(raiz.dir)) + 1
        
        if (caso == 1):
            if (raiz.black):
                caso = 0
            else:
                caso = 2
        elif (caso == 2):
            if (self.isNodoBlack(tio)):
                balanco = self.getBalanco(raiz)
                if (balanco > 1):
                    if (item > raiz.esq.item): #Left-Right
                        raiz.esq = self.rotacaoEsq(raiz.esq)
                    raiz = self.rotacaoDir(raiz)
                    raiz.dir, raiz = self.swapNodoCor(raiz.dir, raiz)
                    caso = 0
                elif (balanco < -1):
                    if (item < raiz.dir.item): #Right-Left
                        raiz.dir = self.rotacaoDir(raiz.dir)
                    raiz = self.rotacaoEsq(raiz)
                    raiz.esq, raiz = self.swapNodoCor(raiz.esq, raiz)
                    caso = 0
            else:
                raiz.esq = self.setNodoToBlack(raiz.esq)
                raiz.dir = self.setNodoToBlack(raiz.dir)
                raiz = self.setNodoToRed(raiz)
                caso = 1
        return raiz, caso
    def setNodoToDoubleBlack(self, nodo):
        if (nodo == None): return self.criarNodo(None, 2)
        nodo.black = 2
        return nodo
    def isNodoDoubleBlack(self, nodo):
        return (nodo.black == 2 if nodo != None else False)
    def delNodoSubstituto(self, nodo):
        if (nodo.dir != None): return self.delNodoSubstituto(nodo.dir)
        return nodo
    def deletar(self, item, raiz):
        raiz = self.deletarMengo(item, raiz)
        if (raiz.item == None):
            del raiz
            return
        raiz.black = True
        return raiz
    def deletarMengo(self, item, raiz):
        if (raiz == None or raiz.item == None): return raiz
        if (item < raiz.item):
            raiz.esq = self.deletarMengo(item, raiz.esq)
        elif (item > raiz.item):
            raiz.dir = self.deletarMengo(item, raiz.dir)
        else:
            if (raiz.esq != None and raiz.dir != None):
                subs = self.delNodoSubstituto(raiz.esq)
                raiz.item = subs.item
                raiz.esq = self.deletarMengo(subs.item, raiz.esq)
            else:
                if (raiz.esq == None): subs = raiz.dir
                else: subs = raiz.esq
                
                if (self.isNodoRed(raiz) or self.isNodoRed(subs)): #############
                    subs = self.setNodoToBlack(subs)
                else: subs = self.setNodoToDoubleBlack(subs)
                
                del raiz
                return subs
        
        irmao = None ####################
        if (self.isNodoDoubleBlack(raiz.esq)):
            irmao = raiz.dir
            coxinha = True
        elif (self.isNodoDoubleBlack(raiz.dir)):
            irmao = raiz.esq
            coxinha = False
        if (irmao != None):
            if (irmao.black):
                if (coxinha): raiz.esq = self.setNodoToBlack(raiz.esq)
                else: raiz.dir = self.setNodoToBlack(raiz.dir)
                if (self.isNodoBlack(irmao.esq) and self.isNodoBlack(irmao.dir)):
                    irmao = self.setNodoToRed(irmao)
                    if (self.isNodoBlack(raiz)): raiz = self.setNodoToDoubleBlack(raiz)
                    else: raiz = self.setNodoToBlack(raiz)
                else:
                    if (coxinha):
                        if (self.isNodoBlack(irmao.dir)): #Right-Left
                            irmao = self.rotacaoDir(irmao)
                            irmao.dir, irmao = self.swapNodoCor(irmao.dir, irmao)
                        raiz.dir = irmao
                        raiz = self.rotacaoEsq(raiz)
                        raiz.esq, raiz = self.swapNodoCor(raiz.esq, raiz)
                        raiz.dir = self.setNodoToBlack(raiz.dir, black = self.isNodoBlack(raiz.esq))
                    else:
                        if (self.isNodoBlack(irmao.esq)): #Left-Right
                            irmao = self.rotacaoEsq(irmao)
                            irmao.esq, irmao = self.swapNodoCor(irmao.esq, irmao)
                        raiz.esq = irmao
                        raiz = self.rotacaoDir(raiz)
                        raiz.dir, raiz = self.swapNodoCor(raiz.dir, raiz)
                        raiz.esq = self.setNodoToBlack(raiz.esq, black = self.isNodoBlack(raiz.dir))
            else:
                if (coxinha):
                    raiz = self.rotacaoEsq(raiz)
                    raiz.esq, raiz = self.swapNodoCor(raiz.esq, raiz)
                    raiz.dir = self.setNodoToBlack(raiz.dir)
                    raiz.esq = self.deletarMengo(item, raiz.esq)
                else:
                    raiz = self.rotacaoDir(raiz)
                    raiz.dir, raiz = self.swapNodoCor(raiz.dir, raiz)
                    raiz.esq = self.setNodoToBlack(raiz.esq)
                    raiz.dir = self.deletarMengo(item, raiz.dir)
        return raiz
    def reinserir(self, item, black, raiz):
        if (raiz == None): return self.criarNodo(item, black)
        if (item < raiz.item):
            raiz.esq = self.reinserir(item, black, raiz.esq)
        elif (item > raiz.item):
            raiz.dir = self.reinserir(item, black, raiz.dir)
        else: return raiz
        raiz.alt = max(self.getAltura(raiz.esq), self.getAltura(raiz.dir)) + 1
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
    def listaArvoreRB(self, raiz):
        if (raiz == None): return
        fila = [raiz]
        lista = []
        while fila:
            nodo = fila.pop(0)
            if (nodo.esq != None):
                fila.append(nodo.esq)
            if (nodo.dir != None):
                fila.append(nodo.dir)
            lista.append((nodo.item,nodo.black))
        return lista
    def listaNodosBFS(self, raiz):
        if (raiz == None): return
        fila = [raiz]
        lista = []
        while fila:
            nodo = fila.pop(0)
            if (nodo.esq != None):
                fila.append(nodo.esq)
            if (nodo.dir != None):
                fila.append(nodo.dir)
            lista.append(nodo)
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
    def listaNodos(self, raiz):
        if raiz == None:
            return []
        else:
            return  self.listaNodos(raiz.esq) + [raiz] + self.listaNodos(raiz.dir)
    def listaArvore(self, raiz):
        if raiz == None:
            return []
        else:
            return  self.listaArvore(raiz.esq) + [raiz.item] + self.listaArvore(raiz.dir)
    def listaInvertidaNodos(self, raiz):
        if raiz == None:
            return []
        else:
            return  self.listaInvertidaNodos(raiz.dir) + [raiz] + self.listaInvertidaNodos(raiz.esq)
    def listaInvertidaArvore(self, raiz):
        if raiz == None:
            return []
        else:
            return  self.listaInvertidaArvore(raiz.dir) + [raiz.item] + self.listaInvertidaArvore(raiz.esq)
    def strNodos(self, raiz):
        if raiz != None:
            return str(raiz) + ' ' + self.strNodos(raiz.esq) + self.strNodos(raiz.dir)
        return ''
    def strArvore(self, raiz):
        if raiz != None:
            return ' [ ' + str(raiz.item) + self.strArvore(raiz.esq) + self.strArvore(raiz.dir) + ' ] '
        return ''
    def __str__(self):
        out = '{'
        if (not self.estaVazia()):
            out += ' ' + self.strArvore(self.raiz) + ' '
        return out + '}'

        
class Aplicacao:
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
        self.b3 = Button(pai, text = "Criar árvore aleatória de N nodos", command = self.geraAleatoria)
        self.b3.pack()
        self.f2 = Frame(pai)
        self.f2.pack()
        self.b4 = Button(self.f2, text = "Desfazer", state = "disabled", command = self.desfazArvore)
        self.b4.pack(side=LEFT)
        self.b5 = Button(self.f2, text = "Refazer", state = "disabled", command = self.refazArvore)
        self.b5.pack(side=RIGHT)
        self.c1 = Canvas(pai,width=1024,height=768)
        self.c1.pack()
        self.HORIZONTAL = 1024
        self.VERTICAL = 768
        self.tamanho = 30
        self.arvoreBinaria = ArvoreBinaria()
        self.raiz = None
        self.bakArvores = [None]
        self.bakIndex = 0
        self.desenhaArvore()
    def constroiArvore(self, *args):
        try:
            valor = int(self.t1.get())
        except Exception:
            return
        os.system('cls' if os.name == 'nt' else 'clear')
        self.t1.delete(0, 'end')
        if self.raiz == None:
            print("Criando com raiz ", str(valor), "...\n")
            self.b2['state'] = 'normal'
            self.b4['state'] = 'normal'
        else:
            print("Inserindo", str(valor), "...\n")
        self.raiz = self.arvoreBinaria.inserir(valor, self.raiz)
        self.mostrarBalanco()
        self.desenhaArvore()
        self.backupArvore()
    def desconstroiArvore(self, *args):
        try:
            valor = int(self.t1.get())
        except Exception:
            return
        os.system('cls' if os.name == 'nt' else 'clear')
        self.t1.delete(0, 'end')
        print("Deletando", str(valor), "...\n")
        self.raiz = self.arvoreBinaria.deletar(valor, self.raiz)
        if (self.raiz == None):
            print("Arvore esvaziada.")
            self.b2['state'] = 'normal'
        self.mostrarBalanco()
        self.desenhaArvore()
        self.backupArvore()
    def geraAleatoria(self, *args):
        try:
            valor = int(self.t1.get())
            if (valor < 0): raise Exception
        except Exception:
            return
        os.system('cls' if os.name == 'nt' else 'clear')
        self.raiz = None
        if (valor == 0):
            print("Arvore esvaziada.")
            self.t1.delete(0, 'end')
            self.b2['state'] = 'disabled'
        else:
            print("Gerando árvore binária aleatória com", str(valor), "nodos...\n")
            for i in range(valor):
                self.raiz = self.arvoreBinaria.inserir(random.randint(10*valor,100*valor), self.raiz)
            self.mostrarBalanco()
            self.b2['state'] = 'normal'
            self.b4['state'] = 'normal'
        self.desenhaArvore()
        self.backupArvore()
        '''
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
        '''
    def desfazArvore(self, *args):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Desfazendo a última alteraçao...\n")
        self.bakIndex -= 1
        listaArvore = self.bakArvores[self.bakIndex]
        self.raiz = None
        if (listaArvore != None):
            self.b2['state'] = 'normal'
            for dados in listaArvore:
                self.raiz = self.arvoreBinaria.reinserir(dados[0], dados[1], self.raiz)
            self.mostrarBalanco()
        else:
            self.b2['state'] = 'disabled'
        if (self.bakIndex == 0):
            print("Arvore esvaziada.")
            self.b4['state'] = 'disabled'
        self.b5['state'] = 'normal'
        self.desenhaArvore()
    def refazArvore(self, *args):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Refazendo recentes alteraçoes...\n")
        self.bakIndex += 1
        listaArvore = self.bakArvores[self.bakIndex]
        self.raiz = None
        if (listaArvore == None):
            print("Arvore esvaziada.")
            self.b2['state'] = 'disabled'
        else:
            self.b2['state'] = 'normal'
            for dados in listaArvore:
                self.raiz = self.arvoreBinaria.reinserir(dados[0], dados[1], self.raiz)
            self.mostrarBalanco()
        self.b4['state'] = 'normal'
        if (self.bakIndex + 1 == len(self.bakArvores)):
            self.b5['state'] = 'disabled'
        self.desenhaArvore()
    def backupArvore(self):
        if (self.raiz != self.bakArvores[self.bakIndex]):
            self.bakIndex += 1
            if (self.bakIndex < len(self.bakArvores)):
                self.bakArvores = self.bakArvores[0:self.bakIndex]
                self.b5['state'] = 'disabled'
            self.bakArvores.append(self.arvoreBinaria.listaArvoreRB(self.raiz))
    def checarBalanco(self, raiz, balanceado = True):
        if (raiz != None):
            balanceado *= self.checarBalanco(raiz.esq)
            balanceado *= self.checarBalanco(raiz.dir)
            if (balanceado):
                balanco = self.arvoreBinaria.getBalanco(raiz)
                if (balanco < -1) or (balanco > 1):
                    return False
        return balanceado
    def checarBlackBalanco(self, raiz, balanceado = True):
        if (raiz != None):
            balanceado *= self.checarBlackBalanco(raiz.esq)
            balanceado *= self.checarBlackBalanco(raiz.dir)
            if (balanceado):
                balanco = self.arvoreBinaria.getBlackBalanco(raiz)
                if balanco != 0:
                    return False
        return balanceado
    def mostrarBalanco(self):
        balanceado = self.checarBalanco(self.raiz) != 0
        print('Balanceada pela altura total? ' + str(balanceado))
        balanceado = self.checarBlackBalanco(self.raiz) != 0
        print('Balanceada pela altura de nodos negros? ' + str(balanceado))
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
        if (nodo == self.arvoreBinaria.raiz):
            self.c1.create_oval(x1-3,y1-3,x2+3,y2+3,fill='GOLD')
        nodoCor = ("black" if self.arvoreBinaria.isNodoBlack(nodo) else "red") ###############
        self.c1.create_oval(x1,y1,x2,y2,fill=nodoCor) ############
        self.c1.create_text(posX,posY,text=str(nodo.item),fill="white")
    
    
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    root = Tk(None,None," Desenhando Uma Árvore Binária Rubro-Negra")
    root.geometry("1024x750")
    ap = Aplicacao(root)
    root.mainloop()
    os.system('cls' if os.name == 'nt' else 'clear')
