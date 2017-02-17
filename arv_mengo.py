#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import os
import random
from tkinter import *


class Nodo:
    def __init__(self, item, esq = None, dir = None, black = True): ###############
        self.item = item
        self.esq = esq
        self.dir = dir
        self.alt = 1
        self.black = black
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
        return Nodo(item, black = black)
    def inicializarRaiz(self, item, black): #####################
        self.raiz = self.criarNodo(item, black=black)
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
    def nodoIsBlack(self, nodo): ##########################
        if (nodo == None): return True
        return nodo.black
    def swapNodoCor(self, nodo1, nodo2): ######################
        return self.nodoIsBlack(nodo2), self.nodoIsBlack(nodo1)
    def rotacaoDir(self, velhaRaiz):
        novaRaiz = velhaRaiz.esq
        velhaRaiz.esq, novaRaiz.dir = novaRaiz.dir, velhaRaiz
        velhaRaiz.alt = max(self.getAltura(velhaRaiz.esq), self.getAltura(velhaRaiz.dir)) + 1
        novaRaiz.alt = max(self.getAltura(novaRaiz.esq), self.getAltura(novaRaiz.dir)) + 1
        velhaRaiz.black, novaRaiz.black = self.swapNodoCor(velhaRaiz, novaRaiz) ###########
        return novaRaiz
    def rotacaoEsq(self, velhaRaiz):
        novaRaiz = velhaRaiz.dir
        velhaRaiz.dir, novaRaiz.esq = novaRaiz.esq, velhaRaiz
        velhaRaiz.alt = max(self.getAltura(velhaRaiz.esq), self.getAltura(velhaRaiz.dir)) + 1
        novaRaiz.alt = max(self.getAltura(novaRaiz.esq), self.getAltura(novaRaiz.dir)) + 1
        velhaRaiz.black, novaRaiz.black = self.swapNodoCor(velhaRaiz, novaRaiz) ############
        return novaRaiz
    def setNodoToBlack(self, nodo, black = True): ################
        if (nodo != None):
            nodo.black = black
    def inserir(self, item, raiz): ##################
        raiz, caso = self.inserirMengo(item, raiz)
        raiz.black = True
        return raiz
    def inserirMengo(self, item, raiz): ###################
        if (raiz == None):
            return self.criarNodo(item, black = False), 1
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
            if (tio == None or tio.black):
                balanco = self.getBalanco(raiz)
                if (balanco > 1):
                    if (item > raiz.esq.item): #Left-Right
                        raiz.esq = self.rotacaoEsq(raiz.esq)
                    return self.rotacaoDir(raiz), 0
                elif (balanco < -1):
                    if (item < raiz.dir.item): #Right-Left
                        raiz.dir = self.rotacaoDir(raiz.dir)
                    return self.rotacaoEsq(raiz), 0
            else:
                self.setNodoToBlack(raiz.esq)
                self.setNodoToBlack(raiz.dir)
                self.setNodoToBlack(raiz, black=False)
                caso = 1
        return raiz, caso
    def pesquisar(self, item, raiz):
        if (raiz != None):
            if (item == raiz.item):
                return raiz
            elif (item < raiz.item):
                return self.pesquisar(item, raiz.esq)
            else:
                return self.pesquisar(item, raiz.dir)
        return
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
        self.b1 = Button(self.f1, text = "Inserir N")
        self.b1.bind("<Button-1>", self.constroiArvore)
        self.b1.pack(side=RIGHT)
        self.b2 = Button(pai, text = "Criar árvore aleatória de N nodos")
        self.b2.bind("<Button-1>", self.geraAleatoria)
        self.b2.pack()
        self.f2 = Frame(pai)
        self.f2.pack()
        self.b3 = Button(self.f2, text = "Desfazer", state = "disabled", command = self.desfazArvore)
        self.b3.pack(side=LEFT)
        self.b4 = Button(self.f2, text = "Refazer", state = "disabled", command = self.refazArvore)
        self.b4.pack(side=RIGHT)
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
            self.b3['state'] = 'normal'
        else:
            print("Inserindo", str(valor), "...\n")
        self.raiz = self.arvoreBinaria.inserir(valor, self.raiz)
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
        else:
            print("Gerando árvore binária aleatória com", str(valor), "nodos...\n")
            for i in range(valor):
                self.raiz = self.arvoreBinaria.inserir(random.randint(10*valor,100*valor), self.raiz)
            self.mostrarBalanco()
            self.b3['state'] = 'normal'
        self.desenhaArvore()
        self.backupArvore()
    def desfazArvore(self, *args):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Desfazendo a última alteraçao...\n")
        self.bakIndex -= 1
        listaArvore = self.bakArvores[self.bakIndex]
        self.raiz = None
        if (listaArvore != None):
            for item in listaArvore:
                self.raiz = self.arvoreBinaria.inserir(item, self.raiz)
            self.mostrarBalanco()
        if (self.bakIndex == 0):
            print("Arvore esvaziada.")
            self.b3['state'] = 'disabled'
        self.b4['state'] = 'normal'
        self.desenhaArvore()
    def refazArvore(self, *args):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Refazendo recentes alteraçoes...\n")
        self.bakIndex += 1
        listaArvore = self.bakArvores[self.bakIndex]
        self.raiz = None
        if (listaArvore == None):
            print("Arvore esvaziada.")
        else:
            for item in listaArvore:
                self.raiz = self.arvoreBinaria.inserir(item, self.raiz)
            self.mostrarBalanco()
        self.b3['state'] = 'normal'
        if (self.bakIndex + 1 == len(self.bakArvores)):
            self.b4['state'] = 'disabled'
        self.desenhaArvore()
    def backupArvore(self):
        if (self.raiz != self.bakArvores[self.bakIndex]):
            self.bakIndex += 1
            if (self.bakIndex < len(self.bakArvores)):
                self.bakArvores = self.bakArvores[0:self.bakIndex]
                self.b4['state'] = 'disabled'
            self.bakArvores.append(self.arvoreBinaria.listaArvoreBFS(self.raiz))
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
        self.c1.create_rectangle(0, 0, self.HORIZONTAL, self.VERTICAL, fill="#74AFAD")
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
        nodoCor = ("black" if self.arvoreBinaria.nodoIsBlack(nodo) else "red") ###############
        self.c1.create_oval(x1,y1,x2,y2,fill=nodoCor) ############
        self.c1.create_text(posX,posY,text=str(nodo.item),fill="white")
    
    
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    root = Tk(None,None," Desenhando Uma Árvore Binária Rubro-Negra")
    root.geometry("1024x750")
    ap = Aplicacao(root)
    root.mainloop()
    input('\nPress any key to continue . . . ')
    os.system('cls' if os.name == 'nt' else 'clear')
