import string
import unicodedata
from textwrap import wrap
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

Ui_MainWindow, QtBaseClass = uic.loadUiType("gui.ui")

class MyApp(QMainWindow, Ui_MainWindow):

    matrix = np.empty((5,5), dtype=str)


    def encoding(self, text):
        text = unicodedata.normalize('NFD', text)
        text = u"".join([c for c in text if not unicodedata.combining(c)])
        return text


    def lowerAndPunctuation(self, text):
        text.translate(str.maketrans('', '', string.punctuation))
        text = str.lower(text)
        return text


    def normalizeText(self, text):
        text = self.lowerAndPunctuation(text)
        text = self.encoding(text)
        text = text.replace(" ", "")
        text = text.replace("i", "y")
        return text


    def checkDuplicates(self, text):
        p=""
        for i in text:
            if i not in p:
                p += i
        return p


    def storeStringInMatrix(self, text):
        alphabet = string.ascii_lowercase
        alphabet = alphabet.replace("i", "y")
        for i in alphabet:
            if i not in text:
                text += i
        list(text)

        k = 0
        for i in range(len(MyApp.matrix)):
            for j in range(len(MyApp.matrix[i])):
                MyApp.matrix[i][j] = text[k]
                k += 1
        return MyApp.matrix


    def findPosition(self, matrix,letter):
        x=y=0
        for i in range(5):
            for j in range(5):
                if matrix[i][j]==letter.lower():
                    x=i
                    y=j
        return x, y


    def zasifruj(self):
        klic = self.klic.text()
        OT = self.inputZasifrovat.text()
        ST = ""
        OT = self.normalizeText(OT)
        ot = [OT[i:i + 2] for i in range(0, len(OT), 2)]
        klic = self.normalizeText(klic)
        klic = self.checkDuplicates(klic)
        keyMatrix = self.storeStringInMatrix(klic)
        
        for m in ot:
            m1, n1 = self.findPosition(keyMatrix,m[0])
            m2, n2 = self.findPosition(keyMatrix,m[1])
            if m1 == m2:
                ST += keyMatrix[m1][(n1+1)%5]
                ST += keyMatrix[m1][(n2+1)%5]
            elif n1==n2:
                ST += keyMatrix[(m1+1)%5][n1]
                ST += keyMatrix[(m2+1)%5][n2]
            elif m1 != m2 and n1 != n2:
                ST += keyMatrix[m1][n2]
                ST += keyMatrix[m2][n1]

        ST = wrap(ST, 5)
        ST = " ".join(ST)
        self.outputZasifrovat.setText(ST)


    def desifruj(self):
        klic = self.klic.text()
        klic = self.normalizeText(klic)
        klic = self.checkDuplicates(klic)
        keyMatrix = self.storeStringInMatrix(klic)
        text = self.inputDesifrovat.text()
        text = "".join(text)
        text = [text[i:i + 2] for i in range(0, len(text), 2)]
        output = ""
       
        for m in text:
            m1, n1 = self.findPosition(keyMatrix,m[0])
            m2, n2 = self.findPosition(keyMatrix,m[1])
            if m1 == m2:
                output += keyMatrix[m1][(n1-1)%5]
                output += keyMatrix[m1][(n2-1)%5]
            elif n1 == n2:
                output += keyMatrix[(m1-1)%5][n1]
                output += keyMatrix[(m2-1)%5][n2]
            elif m1 != m2 and n1 != n2:
                output += keyMatrix[m1][n2]
                output += keyMatrix[m2][n1]
            
        self.outputDesifrovat.setText(output)



    def __init__(self):

        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


        self.zasifrovat.clicked.connect(self.zasifruj)
        self.desifrovat.clicked.connect(self.desifruj)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())