import copy
import math
import sys
import os
import time


class nodInfo:
    def __init__(self, broscute, frunze, greutatiMal):
        self.broscute = broscute
        self.frunze = frunze
        self.greutatiMal = greutatiMal

class Graph:  # graful problemei
    def __init__(self, nume_fisier):
        f = open(nume_fisier, 'r')

        continutFisier = f.read()
        f.close()
        liniiFisier = continutFisier.split("\n")
        self.razaLac = int(liniiFisier[0])

        linieBroscute = liniiFisier[1]
        broscute = {}
        self.listaBroscute = []                                     #dictionarul le pastreaza intr-o ordine random, in enunt scrie ca trebuie luata in ordinea indexului sariturile din fiecare nod
        for i in range(0, len(linieBroscute.split(" ")), 3):
            nume = linieBroscute.split(" ")[i]
            greutate = int(linieBroscute.split(" ")[i + 1])
            numeFrunza = linieBroscute.split(" ")[i + 2]
            broscute[nume] = [greutate, numeFrunza]
            self.listaBroscute.append(nume)

        liniiFrunze = liniiFisier[2:]
        frunze = {}
        for l in liniiFrunze:
            nume = l.split(" ")[0]
            x = int(l.split(" ")[1])
            y = int(l.split(" ")[2])
            insecte = int(l.split(" ")[3])
            greutate = int(l.split(" ")[4])
            greutateFolosita = 0
            frunze[nume] = [x, y, insecte, greutate, greutateFolosita]

        for b in broscute.keys():
            frunze[broscute[b][1]][4] = broscute[b][0]

        greutatiMal = {}# grautaMal

        self.start = nodInfo(broscute, frunze, greutatiMal)

    def testeazaScop(self, nodCurent):
        return len(nodCurent.info.broscute.keys()) == 0

    def genereazaMutariBroscuta(self, broscuta, stariVechi):
        stariNoi = []
        for s in stariVechi:
            frunzaCurenta = s.broscute[broscuta][1]
            for i in range(s.frunze[frunzaCurenta][2] + 1):
                greutateNoua = s.broscute[broscuta][0] + i - 1
                if greutateNoua > 0:
                    for f in s.frunze.keys():
                        xCurent = s.frunze[frunzaCurenta][0]
                        yCurent = s.frunze[frunzaCurenta][1]
                        xFinal = s.frunze[f][0]
                        yFinal = s.frunze[f][1]
                        if math.sqrt((xCurent - xFinal) ** 2 + (yCurent - yFinal) ** 2) <= (greutateNoua + 1) / 3:
                            if s.frunze[f][3] >= s.frunze[f][4] + s.frunze[f][2] + greutateNoua:
                                if frunzaCurenta != f:
                                    stareNoua = copy.deepcopy(s)

                                    stareNoua.frunze[f][4] += greutateNoua
                                    stareNoua.frunze[frunzaCurenta][4] -= s.broscute[broscuta][0]

                                    stareNoua.broscute[broscuta][1] = f
                                    stareNoua.broscute[broscuta][0] = greutateNoua

                                    stareNoua.frunze[frunzaCurenta][2] -= i

                                    stariNoi.append(stareNoua)

                    if math.sqrt(s.frunze[frunzaCurenta][0] ** 2 + s.frunze[frunzaCurenta][1] ** 2) >= self.razaLac - (greutateNoua + 1) / 3:
                        stareNoua = copy.deepcopy(s)

                        stareNoua.frunze[frunzaCurenta][4] -= s.broscute[broscuta][0]

                        stareNoua.broscute.pop(broscuta, None)
                        stareNoua.greutatiMal[broscuta] = greutateNoua

                        stareNoua.frunze[frunzaCurenta][2] -= i

                        stariNoi.append(stareNoua)

        return stariNoi


    def costMutare(self, stareNoua, nodCurent):
        cost = 0
        for b in nodCurent.info.broscute.keys():
            if b in stareNoua.broscute.keys():
                xCurent = nodCurent.info.frunze[nodCurent.info.broscute[b][1]][0]
                yCurent = nodCurent.info.frunze[nodCurent.info.broscute[b][1]][1]
                xNou = stareNoua.frunze[stareNoua.broscute[b][1]][0]
                yNou = stareNoua.frunze[stareNoua.broscute[b][1]][1]

                cost += math.sqrt((xCurent - xNou) ** 2 + (yCurent - yNou) ** 2)
            else:
                xCurent = nodCurent.info.frunze[nodCurent.info.broscute[b][1]][0]
                yCurent = nodCurent.info.frunze[nodCurent.info.broscute[b][1]][1]

                cost += self.razaLac - math.sqrt(xCurent ** 2 + yCurent ** 2)                                                              ###

        return cost



    def genereazaSuccesori(self, nodCurent, tipEuristica = "euristica banala"):
        global numarNoduriGenerate

        listaSuccesori = []
        stari = [nodCurent.info]
        for b in self.listaBroscute:
            if b in nodCurent.info.broscute.keys():
                stari = self.genereazaMutariBroscuta(b, stari)

        for s in stari:
            if not nodCurent.contineInDrum(s):
                nodNou = NodParcurgere(s, nodCurent, cost = nodCurent.g + self.costMutare(s, nodCurent), h = self.calculeazaH(s, tipEuristica))
                listaSuccesori.append(nodNou)

        numarNoduriGenerate += len(listaSuccesori)
        return listaSuccesori

    def calculeazaH(self, infoNod, tipEuristica = "euristica banala"):
        if tipEuristica == "euristica banala":
            if len(infoNod.broscute.keys()) > 0:
                return 1
            return 0

        if tipEuristica == "euristica admisibila 1":
            h = 0
            for b in infoNod.broscute.keys():
                xBroscuta = infoNod.frunze[infoNod.broscute[b][1]][0]
                yBroscuta = infoNod.frunze[infoNod.broscute[b][1]][1]

                h += self.razaLac - math.sqrt(xBroscuta ** 2 + yBroscuta ** 2) #distanta de la broscuta la marginea lacului

            return h

        if tipEuristica == "euristica admisibila 2": #daca broscuta poate ajunge la mal dintr-o saritura atunci lungimea sariturii este costul, daca broscuta e la mal costul e 0 si altfel costul este minimul dintre sumele dintre distantele de la broasca la toate frunzele la care poate ajunge si distanta de la fiecare dintre aceste frunze la mal
            h = 0
            for b in infoNod.broscute.keys():
                xBroscuta = infoNod.frunze[infoNod.broscute[b][1]][0]
                yBroscuta = infoNod.frunze[infoNod.broscute[b][1]][1]
                rangeMaxim = (infoNod.broscute[b][0] + infoNod.frunze[infoNod.broscute[b][1]][2]) / 3

                if math.sqrt(xBroscuta ** 2 + yBroscuta ** 2) + rangeMaxim >= self.razaLac:
                    h += self.razaLac - math.sqrt(xBroscuta ** 2 + yBroscuta ** 2)
                else :
                    sume = []
                    for f in infoNod.frunze.keys():
                        xFrunza = infoNod.frunze[f][0]
                        yFrunza = infoNod.frunze[f][1]
                        distBroascaFrunza = math.sqrt((xBroscuta - xFrunza) ** 2 + (yBroscuta - yFrunza) ** 2)
                        if distBroascaFrunza <= rangeMaxim:
                            sume.append(distBroascaFrunza + (self.razaLac - math.sqrt(xFrunza ** 2 + yFrunza ** 2)))
                    h += min(sume)

            return h

        if tipEuristica == "euristica neadmisibila": # adunam maximul distantei de care am vorbit mai sus la toate broscutele (indiferent daca ajungeau la mal dintr-o saritura sau mai multe)
            h = 0
            for b in infoNod.broscute.keys():
                xBroscuta = infoNod.frunze[infoNod.broscute[b][1]][0]
                yBroscuta = infoNod.frunze[infoNod.broscute[b][1]][1]
                rangeMaxim = (infoNod.broscute[b][0] + infoNod.frunze[infoNod.broscute[b][1]][2]) / 3
                sume = []
                for f in infoNod.frunze.keys():
                    xFrunza = infoNod.frunze[f][0]
                    yFrunza = infoNod.frunze[f][1]
                    distBroascaFrunza = math.sqrt((xBroscuta - xFrunza) ** 2 + (yBroscuta - yFrunza) ** 2)
                    if distBroascaFrunza <= rangeMaxim:
                        sume.append(distBroascaFrunza + (self.razaLac - math.sqrt(xFrunza ** 2 + yFrunza ** 2)))
                h += max(sume)

            return h


        else:
            print ("Eroare tip euristica typo")
    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


class NodParcurgere:
    def __init__(self, info, parinte, cost = 0, h = 0):
        self.info = info
        self.parinte = parinte
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisareDrum(self, afisCost = False, afisLung = False):
        l = self.obtineDrum()
        for nod in range(len(l)):
            fo.write(str(nod) + ")" + "\n")
            fo.write(str(l[nod]) + "\n")
        if afisCost:
            fo.write("Cost: " + str(self.g) + "\n")
        if afisLung:
            fo.write("Lungime: " + str(len(l)) + "\n")
        fo.write("Timp:{:.2f}\n".format(time.time() - timpInitial))
        fo.write("Numarul de noduri generate:" + str(numarNoduriGenerate) + "\n")
        fo.write("Numarul maxim de noduri la un moment dat:" + str(maxNumarNoduri) + "\n")
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if infoNodNou == nodDrum.info:
                return True
            nodDrum = nodDrum.parinte
        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return sir

    def __str__(self):
        sir = ""
        if self.parinte is None:
            for b in self.info.broscute.keys():
                sir += b + " se afla pe frunza initiala " + self.info.broscute[b][1] + "(" + str(self.info.frunze[self.info.broscute[b][1]][0]) + "," + str(self.info.frunze[self.info.broscute[b][1]][1]) + "). Greutate broscuta: " + str(self.info.broscute[b][0]) + ".\n"
        else:
            for b in self.parinte.info.broscute.keys():
                if b in self.info.broscute.keys():
                    sir += b
                    sir += " a mancat "
                    sir += str(self.info.broscute[b][0] - self.parinte.info.broscute[b][0] + 1)
                    sir += " insecte. "
                    sir += b
                    sir += " a sarit de la "

                    sir += self.parinte.info.broscute[b][1]
                    sir += "("
                    sir += str(self.parinte.info.frunze[self.parinte.info.broscute[b][1]][0])
                    sir += ","
                    sir += str(self.parinte.info.frunze[self.parinte.info.broscute[b][1]][1])
                    sir += ") la "

                    sir += self.info.broscute[b][1]
                    sir += "("
                    sir += str(self.info.frunze[self.info.broscute[b][1]][0])
                    sir += ","
                    sir += str(self.info.frunze[self.info.broscute[b][1]][1])
                    sir += "). Greutate broscuta: "

                    sir += str(self.info.broscute[b][0])

                    sir += ".\n"
                else:
                    sir += b
                    sir += " a mancat "
                    sir += str(self.info.greutatiMal[b] - self.parinte.info.broscute[b][0] + 1)
                    sir += " insecte. "
                    sir += b
                    sir += " a sarit de la "

                    sir += self.parinte.info.broscute[b][1]
                    sir += "("
                    sir += str(self.parinte.info.frunze[self.parinte.info.broscute[b][1]][0])
                    sir += ","
                    sir += str(self.parinte.info.frunze[self.parinte.info.broscute[b][1]][1])
                    sir += ") la mal. Greutate broscuta: "

                    sir += str(self.info.greutatiMal[b])

                    sir += ".\n"

            sir += "Stare frunze:"
            firstPrint = False
            for f in self.info.frunze.keys():
                if firstPrint is False:
                    firstPrint = True
                else:
                    sir += ","
                sir += " "
                sir += f
                sir += "("
                sir += str(self.info.frunze[f][2])
                sir += ","
                sir += str(self.info.frunze[f][3])
                sir += ")"

            sir += ".\n"

        return sir


def breadthFirst(gr, nrSolutiiCautate = 1, tipEuristica = "euristica banala"):
    global timeout
    global maxNumarNoduri

    c = [NodParcurgere(gr.start, None)]

    while len(c) > 0:
        if time.time() - timpInitial > timeout:
            return
        nodCurent = c.pop(0)

        if gr.testeazaScop(nodCurent):
            fo.write("Solutie:" + "\n")
            nodCurent.afisareDrum(afisCost=True, afisLung=True)
            fo.write("\n----------------\n" + "\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tipEuristica = tipEuristica)
        c.extend(lSuccesori)
        if len(c) > maxNumarNoduri:
            maxNumarNoduri = len(c)

def depthFirst(gr, nrSolutiiCautate = 1, tipEuristica = "euristica banala"):
    global numarCurentNoduri
    global maxNumarNoduri

    numarCurentNoduri = 1
    maxNumarNoduri = 1

    df(gr, NodParcurgere(gr.start, None), nrSolutiiCautate, tipEuristica = tipEuristica)

def df(gr, nodCurent, nrSolutiiCautate, tipEuristica = "euristica banala"):
    global numarCurentNoduri
    global maxNumarNoduri
    global timeout

    if time.time() - timpInitial > timeout:
        return nrSolutiiCautate

    if nrSolutiiCautate <= 0:
        numarCurentNoduri -= 1
        return nrSolutiiCautate
    if gr.testeazaScop(nodCurent):
        fo.write("Solutie:" + "\n")
        nodCurent.afisareDrum(afisCost=True, afisLung=True)
        fo.write("\n----------------\n" + "\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            numarCurentNoduri -= 1
            return nrSolutiiCautate
    lSuccesori = gr.genereazaSuccesori(nodCurent, tipEuristica = tipEuristica)
    for sc in lSuccesori:
        if nrSolutiiCautate > 0:
            numarCurentNoduri += 1
            if numarCurentNoduri > maxNumarNoduri:
                maxNumarNoduri = numarCurentNoduri
            nrSolutiiCautate = df(gr, sc, nrSolutiiCautate, tipEuristica = tipEuristica)
    numarCurentNoduri -= 1
    return nrSolutiiCautate

def dfi(gr, nodCurent, adancime, nrSolutiiCautate, tipEuristica = "euristica banala"):
    global numarCurentNoduri
    global maxNumarNoduri
    global timeout

    if time.time() - timpInitial > timeout:
        return nrSolutiiCautate
    if adancime == 1 and gr.testeazaScop(nodCurent):
        fo.write("Solutie:" + "\n")
        nodCurent.afisareDrum(afisCost=True, afisLung=True)
        fo.write("\n----------------\n" + "\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            numarCurentNoduri -= 1
            return nrSolutiiCautate
    if adancime > 1:
        lSuccesori = gr.genereazaSuccesori(nodCurent, tipEuristica = tipEuristica)
        for sc in lSuccesori:
            if nrSolutiiCautate > 0:
                numarCurentNoduri += 1
                if numarCurentNoduri > maxNumarNoduri:
                    maxNumarNoduri = numarCurentNoduri
                nrSolutiiCautate = dfi(gr, sc, adancime - 1, nrSolutiiCautate, tipEuristica = tipEuristica)
    numarCurentNoduri -= 1
    return nrSolutiiCautate

def depthFirstIterativ(gr, nrSolutiiCautate = 1, tipEuristica = "euristica banala"):
    global numarCurentNoduri
    global maxNumarNoduri
    for i in range(1, 101):
        if nrSolutiiCautate <= 0:
            numarCurentNoduri -= 1
            return
        fo.write("Adancime:" + str(i) + "\n")
        numarCurentNoduri += 1
        if (numarCurentNoduri > maxNumarNoduri):
            maxNumarNoduri = numarCurentNoduri
        nrSolutiiCautate = dfi(gr, NodParcurgere(gr.start, None), i, nrSolutiiCautate, tipEuristica = tipEuristica)


def aStarNeOp(gr, nrSolutiiCautate = 1, tipEuristica = "euristica banala"):
    global maxNumarNoduri
    global timeout

    c = [NodParcurgere(gr.start, None, 0, gr.calculeazaH(gr.start, tipEuristica = tipEuristica))]

    while len(c) > 0:
        nodCurent = c.pop(0)
        if time.time() - timpInitial > timeout:
            return

        if gr.testeazaScop(nodCurent):
            fo.write("Solutie:" + "\n")
            nodCurent.afisareDrum(afisCost=True, afisLung=True)
            fo.write("\n----------------\n" + "\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tipEuristica = tipEuristica)
        for s in lSuccesori:
            i = 0
            gasitLoc = False
            for i in range(len(c)):
                if c[i].f > s.f:
                    gasitLoc = True
                    break
            if gasitLoc:
                c.insert(i, s)
            else:
                c.append(s)

        if len(c) > maxNumarNoduri:
            maxNumarNoduri = len(c)


def aStarOp(gr, tipEuristica = "euristica banala"):
    global maxNumarNoduri
    global timeout

    lOpen = [NodParcurgere(gr.start, None, 0, gr.calculeazaH(gr.start, tipEuristica = tipEuristica))]
    lClosed = []

    while len(lOpen) > 0:
        nodCurent = lOpen.pop(0)
        lClosed.append(nodCurent)

        if time.time() - timpInitial > timeout:
            return

        if gr.testeazaScop(nodCurent):
            fo.write("Solutie:" + "\n")
            nodCurent.afisareDrum(afisCost=True, afisLung=True)
            fo.write("\n----------------\n" + "\n")
            return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tipEuristica = tipEuristica)
        for s in lSuccesori:
            gasitC = False
            for nodC in lOpen:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori.remove(s)
                    else:
                        lOpen.remove(nodC)
                    break
            if not gasitC:
                for nodC in lClosed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:
                            lClosed.remove(nodC)
                        break
        for s in lSuccesori:
            i = 0
            gasitLoc = False
            for i in range(len(lOpen)):
                if lOpen[i].f > s.f or (lOpen[i].f == s.f and lOpen[i].g <= s.g):
                    gasitLoc = True
                    break
            if gasitLoc:
                lOpen.insert(i, s)
            else:
                lOpen.append(s)

        if len(lOpen) + len(lClosed) > maxNumarNoduri:
            maxNumarNoduri = len(lOpen) + len(lClosed)


def idaStar(gr, nrSolutiiCautate = 1, tipEuristica = "euristica banala"):
    global maxNumarNoduri
    global numarCurentNoduri
    maxNumarNoduri = 1
    numarCurentNoduri = 1

    nodStart = NodParcurgere(gr.start, None, 0, gr.calculeazaH(gr.start, tipEuristica = tipEuristica))
    limita = nodStart.f
    while True:
        nrSolutiiCautate, rez = construiesteDrum(gr, nodStart, limita, nrSolutiiCautate, tipEuristica = tipEuristica)
        if rez == "gata":
            break
        if rez == float('inf'):
            fo.write("Nu mai exista solutii!" + "\n")
            break
        limita = rez


def construiesteDrum(gr, nodCurent, limita, nrSolutiiCautate, tipEuristica = "euristica banala"):
    global maxNumarNoduri
    global numarCurentNoduri
    global timeout

    if time.time() - timpInitial > timeout:
        return 0, "gata"

    if nodCurent.f > limita:
        numarCurentNoduri -= 1
        return nrSolutiiCautate, nodCurent.f
    if gr.testeazaScop(nodCurent) and nodCurent.f == limita:
        fo.write("Solutie:" + "\n")
        nodCurent.afisareDrum(afisCost=True, afisLung=True)
        fo.write("\n----------------\n" + "\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            numarCurentNoduri -= 1
            return 0, "gata"
    lSuccesori = gr.genereazaSuccesori(nodCurent, tipEuristica = tipEuristica)
    minim = float('inf')
    for s in lSuccesori:
        numarCurentNoduri += 1
        if numarCurentNoduri > maxNumarNoduri:
            maxNumarNoduri = numarCurentNoduri
        nrSolutiiCautate, rez = construiesteDrum(gr, s, limita, nrSolutiiCautate, tipEuristica = tipEuristica)
        if rez == "gata":
            numarCurentNoduri -= 1
            return 0, "gata"
        if rez < minim:
            minim = rez
    numarCurentNoduri -= 1
    return nrSolutiiCautate, minim

def apelFunctii(gr, tipEuristica):
    global timpInitial
    global numarNoduriGenerate
    global maxNumarNoduri
    global numarCurentNoduri

    fo.write("************************************************************************************" + tipEuristica + "\n")
    fo.write("===============================BF:" + "\n")
    timpInitial = time.time()
    numarNoduriGenerate = 0
    maxNumarNoduri = 0
    numarCurentNoduri = 0
    breadthFirst(gr, tipEuristica = tipEuristica)

    fo.write("===============================DF:" + "\n")
    timpInitial = time.time()
    numarNoduriGenerate = 0
    maxNumarNoduri = 0
    numarCurentNoduri = 0
    depthFirst(gr, tipEuristica = tipEuristica)

    fo.write("===============================DFI:" + "\n")
    timpInitial = time.time()
    numarNoduriGenerate = 0
    maxNumarNoduri = 0
    numarCurentNoduri = 0
    depthFirstIterativ(gr, tipEuristica = tipEuristica)

    fo.write("===============================A Star neoptimizat:" + "\n")
    timpInitial = time.time()
    numarNoduriGenerate = 0
    maxNumarNoduri = 0
    numarCurentNoduri = 0
    aStarNeOp(gr, tipEuristica = tipEuristica)

    fo.write("===============================A Star optimizat:" + "\n")
    timpInitial = time.time()
    numarNoduriGenerate = 0
    maxNumarNoduri = 0
    numarCurentNoduri = 0
    aStarOp(gr, tipEuristica = tipEuristica)

    fo.write("===============================IDA Star:" + "\n")
    timpInitial = time.time()
    numarNoduriGenerate = 0
    maxNumarNoduri = 0
    numarCurentNoduri = 0
    idaStar(gr, tipEuristica = tipEuristica)



inputPath = sys.argv[1]
outputPath = sys.argv[2]
nsol = int(sys.argv[3])
timeout = int(sys.argv[4])


timpInitial = 0
numarNoduriGenerate = 0
maxNumarNoduri = 0
numarCurentNoduri = 0

listaFisiereInput = os.listdir(inputPath)
if not os.path.exists(outputPath):
    os.mkdir(outputPath)
fo = ""
for fi in listaFisiereInput:
    numeFisierOutput = "output_" + fi
    gr = Graph(inputPath + "/" + fi)
    fo = open(outputPath + "/" + numeFisierOutput, "w")
    apelFunctii(gr, "euristica banala")
    apelFunctii(gr, "euristica admisibila 1")
    apelFunctii(gr, "euristica admisibila 2")
    apelFunctii(gr, "euristica neadmisibila")
    fo.close()

# gr = Graph(inputPath)
# apelFunctii(gr, "euristica banala")
# apelFunctii(gr, "euristica admisibila 1")
# apelFunctii(gr, "euristica admisibila 2")
# apelFunctii(gr, "euristica neadmisibila")
