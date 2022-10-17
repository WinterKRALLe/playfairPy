import string
import unicodedata
from textwrap import wrap
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtWidgets, QtCore

Ui_MainWindow, QtBaseClass = uic.loadUiType("gui.ui")

class MyApp(QMainWindow, Ui_MainWindow):

    matrix = np.empty((5,5), dtype=str)


    def encoding(self, text):
        text = unicodedata.normalize('NFD', text)
        text = u"".join([c for c in text if not unicodedata.combining(c)])
        return text


    def lowerAndPunctuation(self, text):
        punc = '''!()-[]{};:'"\,<>./?@#ˇ$%^&*_~'''
        for ele in text:
            if ele in punc:
                text = text.replace(ele, "")
        text = str.lower(text)
        return text


    def normalizeText(self, text):
        text = self.lowerAndPunctuation(text)
        text = self.encoding(text)
        for i in text:
            if " " in text:
                text = text.replace(" ","")
            if i.isdigit():
                text = text.replace(i, "")
        return text


    def checkDuplicates(self, text):
        p=""
        for i in text:
            if i not in p:
                p += i
        return p


    def pairPlainText(self, plainText):
        text = []
        for i in plainText:
            text.append(i)
        k = 0
        for i in range(len(text)//2):
                if text[k]==text[k+1]:
                        text.insert(k+1,'X')
                k += 2
        if len(text)%2==1:
            if text[len(text)-1] == "X":
                text.append("W")
            else:
                text.append("X")
        k = 0
        pairedText = []
        for i in range(1,len(text)//2+1):
                pairedText.append(text[k:k+2])
                k += 2
        return pairedText


    def storeStringInMatrix(self, text):
        alphabet = string.ascii_lowercase
        text = text.lower()
        for i in text:
            if i.isdigit():
                i = i.replace(i, "")
        if self.english.isChecked():
            alphabet = alphabet.replace("j", "i")
        elif self.cesky.isChecked():
            alphabet = alphabet.replace("q", "o")
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


    def findPosition(self, matrix, letter):
        x = 0
        y = 0
        for i in range(len(MyApp.matrix)):
            for j in range(len(MyApp.matrix[i])):
                if matrix[i][j] == letter.lower():
                    x = i
                    y = j
        return x, y


    def zasifruj(self):
        OT = self.inputZasifrovat.text()
        OT.lower()
        OT = OT.replace(" ", "xmezerax")
        OT = "".join(x for x in OT if x.isalpha())
        ot = self.pairPlainText(OT)
        ST = ""
        klic = self.klic.text()
        klic = self.normalizeText(klic)
        klic = self.checkDuplicates(klic)
        keyMatrix = self.storeStringInMatrix(klic)
        
        for m in ot:
            m1, n1 = self.findPosition(keyMatrix,m[0])
            m2, n2 = self.findPosition(keyMatrix,m[1])
            if m1 == m2:
                ST += keyMatrix[m1][(n1+1)%5] + keyMatrix[m1][(n2+1)%5]
            elif n1==n2:
                ST += keyMatrix[(m1+1)%5][n1] + keyMatrix[(m2+1)%5][n2]
            elif m1 != m2 and n1 != n2:
                ST += keyMatrix[m1][n2] + keyMatrix[m2][n1]

        ST = wrap(ST, 5)
        ST = " ".join(ST)
        self.displayData(keyMatrix)
        self.outputZasifrovat.setText(ST)


    def desifruj(self):
        klic = self.klic.text()
        klic = self.normalizeText(klic)
        klic = self.checkDuplicates(klic)
        keyMatrix = self.storeStringInMatrix(klic)
        text = self.inputDesifrovat.text()
        text = self.normalizeText(text)
        text = text.replace(" ", "")
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
        output = output.replace("xmezerax", " ")
        self.outputDesifrovat.setText(output)


    def displayData(self, keyMatrix):
        numcols = len(keyMatrix[0])
        numrows = len(keyMatrix)
        self.matrix.setColumnCount(numcols)
        self.matrix.setRowCount(numrows)
        self.matrix.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.matrix.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        for row in range(numrows):
            for column in range(numcols):
                item = QtWidgets.QTableWidgetItem(keyMatrix[row][column])
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.matrix.setItem(row, column, item)


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