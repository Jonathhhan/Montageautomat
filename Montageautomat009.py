import sys, os
from threading import Timer
import random
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QSpinBox, QApplication, QFileDialog, QLabel, QCheckBox, QVBoxLayout, QPlainTextEdit, QDoubleSpinBox, QTreeWidget
from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtGui import QIcon, QPixmap
from Subtitle_class import Subtitles, findfollowers, make_seq
from PyQt5.QtMultimedia import QMediaContent
from VideoPlayer_class import VideoPlayer
from MplCanvas_class import MyMplCanvas
from colorama import Fore, Style, init
from collections import defaultdict, Counter
init()


#if getattr(sys, 'frozen', False):
#        # we are running in a bundle
#        bundle_dir = sys._MEIPASS
#else:
#        # we are running in a normal Python environment
#        bundle_dir = os.path.dirname(os.path.abspath(__file__))

#def resource_path(relative):
#    return os.path.join(
#        os.environ.get(
#            "_MEIPASS2",
#            os.path.abspath(".")
#        ),
#        relative
#    )
#pic_path=os.path.join(bundle_dir, "test.png")
pic_path = "test.png"

style = "text-align: left;"\
        "padding: 6px;"\
        "background-color: orange;"\
        "font: bold 10px;"\
        "font-family: Verdana;"\
        "color: black;"\
        "border-style: outset; border-width: 2px; border-color: black;"\
        "border-radius: 5px;"

class Interface(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):

        print("Montageautomat 2018")

        self.very_important_value = 0
        self.important_value = 0
        self.unimportant_value = 0
        self.else_value = 0
        
        # Fenster Eigenschaften
        self.setWindowTitle('Montageautomat 2018') 
        self.setFixedSize(1150, 550)
        self.setWindowIcon(QIcon(pic_path)) 
        self.bgpic = QLabel(self)
        self.bgpic.setFixedSize(1150, 550)
        self.bgpic.setStyleSheet("background-color: grey")
        self.bgpic2 = QLabel(self)
        self.bgpic2.setFixedSize(720, 435)
        self.bgpic2.move(400,33)
        self.bgpic2.setStyleSheet("background-color: black")
        #self.bgpic.setPixmap(QPixmap(pic_path))

        # Video Player
        self.player = VideoPlayer(self)
        self.player.resize(740, 533)
        self.player.move(390,20)
        self.player.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("Alphaville.avi")))
        self.player.playButton.setEnabled(True)

        # Matplotlib Canvas
        self.plot = QWidget(self)
        l = QVBoxLayout(self.plot)
        sc = MyMplCanvas(self.plot, width=4.1, height=4, dpi=50)
        l.addWidget(sc)
        self.plot.move(5,320)

        # Button: Open Video 
        self.openVideo = QPushButton("Open Video",self)
        self.openVideo.setStyleSheet(style+"background-color: green;color: white; border-color: white;")
        self.openVideo.setFixedWidth(100)
        self.openVideo.clicked.connect(self.player.openFile)
        self.openVideo.move(10,10)

        # Label to show current subtitle
        self.label1 = QLabel(self)
        self.label1.setStyleSheet(style+"background-color: white;font-size: 8pt;")
        self.label1.setText("Nr: 0")
        self.label1.setFixedWidth(100)
        self.label1.setFixedHeight(25)
        self.label1.move(120,10)
        
        # Label to show current follow significance
        self.label2 = QLabel(self)
        self.label2.setStyleSheet(style+"background-color: white;font-size: 8pt;")
        self.label2.setText("W: 0")
        self.label2.setFixedWidth(100)
        self.label2.setFixedHeight(25)
        self.label2.move(120,45)

        #TextEdit1 Label 
        self.textEditLabel1 = QLabel(self)
        self.textEditLabel1.setStyleSheet(style+"background-color: white;font-size: 8pt;")
        self.textEditLabel1.setText("Very important:")
        self.textEditLabel1.setFixedWidth(125)
        self.textEditLabel1.setFixedHeight(30)
        self.textEditLabel1.move(240,10)
         # TextEdit1
        self.textEdit1 = QPlainTextEdit(self)
        self.textEdit1.setFixedWidth(125)
        self.textEdit1.setFixedHeight(65)
        self.textEdit1.keyPressEvent
        self.textEdit1.appendPlainText("know understand secret conscience think memory")
        self.textEdit1.move(240,45)
        self.very_important_words = self.textEdit1.toPlainText().split(" ")
        print("Very important words: ", self.very_important_words)
        def getsettext1():
            self.very_important_words = self.textEdit1.toPlainText().split(" ")
            print("Very important words: ", self.very_important_words)

        # Number Box1
        self.enterNumber1 = QDoubleSpinBox(self)
        self.enterNumber1.setStyleSheet(style)
        self.enterNumber1.setRange(0,1000000)
        self.enterNumber1.setFixedWidth(125)
        self.enterNumber1.setFixedHeight(25)
        self.enterNumber1.move(240,115)
        self.enterNumber1.setValue(20)
        self.very_important_value = self.enterNumber1.value()
        print("Very important value: ", self.very_important_value)
        def getsetvalue1():
            self.very_important_value = self.enterNumber1.value()
            print("Very important value: ", self.very_important_value)
        self.enterNumber1.valueChanged.connect(getsetvalue1)
        
        #TextEdit2 Label 
        self.textEditLabel2 = QLabel(self)
        self.textEditLabel2.setStyleSheet(style+"background-color: white;font-size: 8pt;")
        self.textEditLabel2.setText("Important:")
        self.textEditLabel2.setFixedWidth(125)
        self.textEditLabel2.setFixedHeight(30)
        self.textEditLabel2.move(240,150)
         # TextEdit2
        self.textEdit2 = QPlainTextEdit(self)
        self.textEdit2.setFixedWidth(125)
        self.textEdit2.setFixedHeight(65)
        self.textEdit2.appendPlainText("why because word words number")
        self.textEdit2.move(240,185)
        self.important_words = self.textEdit2.toPlainText().split(" ")
        print("Important words: ", self.important_words)
        # Number Box2
        self.enterNumber2 = QDoubleSpinBox(self)
        self.enterNumber2.setStyleSheet(style)
        self.enterNumber2.setRange(0,1000000)
        self.enterNumber2.setFixedWidth(125)
        self.enterNumber2.setFixedHeight(25)
        self.enterNumber2.move(240,255)
        self.enterNumber2.setValue(5)
        self.important_value = self.enterNumber2.value()
        print("Important value: ", self.important_value)
        def getsetvalue2():
            self.important_value = self.enterNumber2.value()
            print("Important value: ", self.important_value)
        self.enterNumber2.valueChanged.connect(getsetvalue2)
        
        #TextEdit3 Label 
        self.textEditLabel3 = QLabel(self)
        self.textEditLabel3.setStyleSheet(style+"background-color: white;font-size: 8pt;")
        self.textEditLabel3.setText("Unimportant:")
        self.textEditLabel3.setFixedWidth(125)
        self.textEditLabel3.setFixedHeight(30)
        self.textEditLabel3.move(240,290)
        # TextEdit3
        self.textEdit3 = QPlainTextEdit(self)
        self.textEdit3.setFixedWidth(125)
        self.textEdit3.setFixedHeight(65)
        self.textEdit3.appendPlainText("the you of i to a in and is it what are that me no for your one we „its“ „don't“ not but this my was with be or sir here do like they mr outlands have so from where very must all alphaville johnson if „ill“ will he alpha when see as by 60 „youre“ yes who an them which can never now well go vonbraun him too at es light come say those us afraid „whats“ about man were get thank going miss there night professor control said „ive“ only our his their  men day on her natasha death „thats“ „theres“")
        self.textEdit3.move(240,325)
        self.unimportant_words = self.textEdit3.toPlainText().split(" ")
        print("Unimportant words: ", self.unimportant_words)
        # Number Box3
        self.enterNumber3 = QDoubleSpinBox(self)
        self.enterNumber3.setStyleSheet(style)
        self.enterNumber3.setRange(0,1000000)
        self.enterNumber3.setFixedWidth(125)
        self.enterNumber3.setFixedHeight(25)
        self.enterNumber3.move(240,395)
        self.enterNumber3.setValue(0.1)
        self.unimportant_value = self.enterNumber3.value()
        print("Unimportant value: ",self.unimportant_value)
        def getsetvalue3():
            self.unimportant_value = self.enterNumber3.value()
            print("Unimportant value: ",self.unimportant_value)
        self.enterNumber3.valueChanged.connect(getsetvalue3)
        
        #TextEdit4 Label 
        self.textEditLabel4 = QLabel(self)
        self.textEditLabel4.setStyleSheet(style+"background-color: white;font-size: 8pt;")
        self.textEditLabel4.setText("Else:")
        self.textEditLabel4.setFixedWidth(125)
        self.textEditLabel4.setFixedHeight(30)
        self.textEditLabel4.move(240,430)
        #Number Box4
        self.enterNumber4 = QDoubleSpinBox(self)
        self.enterNumber4.setStyleSheet(style)
        self.enterNumber4.setRange(0,1000000)
        self.enterNumber4.setFixedWidth(125)
        self.enterNumber4.setFixedHeight(25)
        self.enterNumber4.move(240,465)
        self.enterNumber4.setValue(1)
        self.else_value = self.enterNumber4.value()
        print("Else value: ", self.else_value)
        def getsetvalue4():
            self.else_value = self.enterNumber4.value()
            print("Else value: ", self.else_value)
        self.enterNumber4.valueChanged.connect(getsetvalue4)

        #self.textEdit1.changeEvent(getsettext)
        self.words_button = QPushButton("Get words",self)
        self.words_button.setStyleSheet(str(style+"background-color: green;color: white; border-color: white;"))
        def getsettext1():
            self.very_important_words = self.textEdit1.toPlainText().split(" ")
            print("Very important words: ", self.very_important_words)
        self.words_button.clicked.connect(getsettext1)
        def getsettext2():
            self.important_words = self.textEdit2.toPlainText().split(" ")
            print("Important words: ", self.important_words)
        self.words_button.clicked.connect(getsettext2)
        def getsettext3():
            self.unimportant_words = self.textEdit3.toPlainText().split(" ")
            print("Unimportant words: ", self.unimportant_words)
        self.words_button.clicked.connect(getsettext3)
        self.words_button.setFixedWidth(80)
        self.words_button.move(240,500)

        # Button: Open New Subtitles
        self.new = "Alphaville.ENG.srt"
        def opennew():
            self.new = QFileDialog.getOpenFileName(self, "Select new Subtitle","", "Srt (*.srt)")[0]
        self.openNewST = QPushButton("New Subtitle",self)
        self.openNewST.setStyleSheet(str(style+"background-color: green;color: white; border-color: white;"))
        self.openNewST.clicked.connect(opennew)
        self.openNewST.setFixedWidth(100)
        self.openNewST.move(10,45)
   
        # Button: Open Learned Subtitles
        self.learned = "Alphaville.ENG.srt"
        def openlearned():
            self.learned = QFileDialog.getOpenFileName(self, "Select old Subtitle","", "Srt (*.srt)")[0]
            learned = Subtitles()
            learned.readUT(self.learned)
            print(Counter(learned.countlist).most_common(10))
            tups =  Counter(learned.countlist).most_common(200)
            tupslist = ', '.join(map(str, tups)) 
            tupslist = tupslist.replace("), ","\n")
            tupslist = tupslist.replace("(","")
            tupslist = tupslist.replace("'","")
            self.textEdit4.insertPlainText(tupslist)
        self.openLearnedST = QPushButton("Old Subtitle",self)
        self.openLearnedST.setStyleSheet(style+"background-color: green;color: white; border-color: white;")
        self.openLearnedST.setFixedWidth(100)
        self.openLearnedST.clicked.connect(openlearned)
        self.openLearnedST.move(10,80)
        learned = Subtitles()
        learned.readUT(self.learned)
        print(Counter(learned.countlist).most_common(10))
        tups =  Counter(learned.countlist).most_common(200)
        tupslist = ', '.join(map(str, tups)) 
        tupslist = tupslist.replace("), ","\n")
        tupslist = tupslist.replace("(","")
        tupslist = tupslist.replace("'","")

        
        
         # TextEdit4
        self.textEdit4 = QPlainTextEdit(self)
        self.textEdit4.setFixedWidth(100)
        self.textEdit4.setFixedHeight(200)
        self.textEdit4.appendPlainText(tupslist)
        self.textEdit4.move(120,100)
        
        #self.wordList.addTopLevelItems(Counter(learned.countlist).most_common(10))
        #self.wordList.move(240,325)
        

        # Button: Make Sequence # self_important words see textedit aboveTypeError("index 0 has type 'tuple' but 'str' is expected",)

        def seq():
            try: 
                self.sequence, self.sig = make_seq(self.new, self.learned, self.write, self.else_value, self.very_important_value, self.important_value, self.unimportant_value, self.very_important_words, self.important_words,  self.unimportant_words)
                sc.refresh_figure(self.sig)
                self.plot = QWidget(self)
                l = QVBoxLayout(self.plot)
                l.addWidget(sc)
                self.plot.move(5,320)
                self.plot.show()
            except: 
                if self.write == 0: print("\nFollow Matrix not available - click 'write fol_Matrix'")
                else: print("New and learned Subtitles need to be chosen!")     
        self.write = 0 # can be changed with checkbox
        self.start = QPushButton("Learn!", self)
        self.start.setStyleSheet(style)
        self.start.setFixedWidth(100)
        self.start.clicked.connect(seq)
        self.start.move(10,115)
        
        # Button: Print Sequence, Plot follow Significance, set Video positions
        def test():
            try: 
                print("\nFilmfolge: ", self.sequence, "\n")
                new = Subtitles()
                new.readUT(self.new)
                for i in range(20):
                    nr = self.sequence[i]
                    print(Fore.GREEN, new.subtitle[nr].start, " - ", new.subtitle[nr].end, ": ", 
                          Style.RESET_ALL, " ".join(new.subtitle[nr].words))
                print("...")
                learned.countlist.extend(new.countlist)
            except: print("No sequence yet")
        self.test = QPushButton("Print sequence", self)
        self.test.setStyleSheet(style)
        self.test.setFixedWidth(100)
        self.test.clicked.connect(test)
        self.test.move(10,150)

        # Button: Apply sequence
        def apply():
            try:
                new = Subtitles()
                new.readUT(self.new)
                # hier wird die Position anhand der "self.sequence" fortlaufend neu bestimmt
                def setposition(t):
                    if t >= len(new.subtitle): return("end")
                    nr = self.sequence[t]
                    self.player.mediaPlayer.setPosition(1000*new.subtitle[nr].start -0.4)
                    self.label1.setText("Nr: "+str(nr))
                    self.label2.setText("W: "+str("%.3f" % self.sig[t]))
                    print(nr)
                    t += 1 
                    # stoppe wenn der letzte UT erreicht, oder die Signifikanz 0 ist
                    if nr < len(self.sequence)-1 and 0 < self.sig[t]:
                    #if t < 5:
                        duration = new.subtitle[nr].duration + (new.subtitle[nr+1].start - new.subtitle[nr].end) - 0.4
                        Timer(duration, lambda: setposition(t)).start()
                    elif nr < len(self.sequence)-1: 
                         print("Letzte Szene!")
                         duration = new.subtitle[nr].duration + (new.subtitle[nr+1].start - new.subtitle[nr].end)
                         Timer(duration, self.player.play).start() 
                    else: print("Letzte Szene!")
                self.player.play()
                setposition(0)
            except: print("No sequence yet")
        self.test = QPushButton("Apply sequence", self)
        self.test.setStyleSheet(style)
        self.test.setFixedWidth(100)
        self.test.clicked.connect(apply)
        self.test.move(10,185)

        # Checkbox: Write folMatrix
        self.check = QCheckBox("Write \nfolMatrix", self)
        self.check.setStyleSheet(style)
        self.check.setFixedWidth(100)
        self.check.stateChanged.connect(self.checked)
        self.check.move(10,220)

        self.show()

    def checked(self, state):
        if state == QtCore.Qt.Checked: self.write = 1
        else: self.write = 0

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    GUI = Interface()
    sys.exit(app.exec_())