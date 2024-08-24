import datetime, sys, platform, json, os
from PySide6 import QtCore
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QVBoxLayout,QMenu , QHBoxLayout, QWidget, QLabel, QApplication, QSystemTrayIcon)
from pathlib import Path
import faulthandler ;faulthandler.enable()
class GlobalVars:
    FileName = ""
    FilePath = ""
    CurrentDay = ""
    WindowSize = (298, 252)
    DebugBit = 1
    LabelCount = 12
    ConfigState = 1
    VersionNumber = 2.0
def LoadConfig():
    match platform.system():
        case "Windows":
            GlobalVars.FileName = "Config.Json"
            GlobalVars.FilePath = os.getcwd()
            ParentPath = os.getcwd()
        case "Linux": 
            GlobalVars.homePath = str(Path.home())
            ConfigDir = "/.config/Pluto/"
            ParentPath = os.path.join(str(Path.home()) + ConfigDir)
            GlobalVars.FileName = "Config.Json"
            GlobalVars.FilePath = os.path.join(str(ParentPath) + GlobalVars.FileName)
            os.chdir(ParentPath)
        case _:
            GlobalVars.homePath = str(Path.home())
            ConfigDir = "/.config/Pluto/"
            ParentPath = os.path.join(str(Path.home()) + ConfigDir)
            GlobalVars.FileName = "Config.Json"
            GlobalVars.FilePath = os.path.join(str(ParentPath) + GlobalVars.FileName)
            os.chdir(ParentPath)
LoadConfig()
with open(str(GlobalVars.FileName), "r") as f:
    GlobalVars.data = json.load(f)
class data():
    def getClass(i):
        Classes = GlobalVars.data["Classes"]
        CurrentDay = GlobalVars.data["CurrentDay"]
        Schedule = GlobalVars.data["Days"][CurrentDay]["Schedule"]
        key = Schedule[str(i)]
        Class = Classes[key]
        return(Class)
    def getSchedule():
        CurrentDay = GlobalVars.data["CurrentDay"]
        Schedule = GlobalVars.data["Days"][CurrentDay]["Schedule"]
        return(Schedule)
    def getTimes(i,operator=1 or 2):
        CurrentDay = GlobalVars.data["CurrentDay"]
        Schedule = GlobalVars.data["Days"][CurrentDay]["Schedule"]
        BellTimes = GlobalVars.data["Days"][CurrentDay]["Times"]
        key = Schedule[str(i)]
        if operator == 1: Time = BellTimes[key]["Start"]
        if operator == 2: Time = BellTimes[key]["End"]
        return(Time)
def GetDeltaTime(d):
    CurrentTime = datetime.datetime.strptime(str(datetime.datetime.now().time().isoformat()), "%H:%M:%S.%f")
    EndTime = datetime.datetime.strptime(str(datetime.datetime.strptime((data.getTimes(d,2)),"%I:%M %p",)),"%Y-%d-%m %H:%M:%S",)
    StartTime = datetime.datetime.strptime(str(datetime.datetime.strptime((data.getTimes(d,1)),"%I:%M %p",)), "%Y-%d-%m %H:%M:%S")
    if CurrentTime - EndTime > datetime.timedelta(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0):          DeltaTime = "Done"
    elif CurrentTime - EndTime < datetime.timedelta(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0):        
        DeltaTime = "Time left: " + str((EndTime - CurrentTime)- datetime.timedelta(0.0, 0.0, (EndTime - CurrentTime).microseconds, 0.0, 0.0, 0.0, 0.0))
    if CurrentTime < StartTime:                                                                DeltaTime = "Time Until: " + str(((StartTime - CurrentTime)- datetime.timedelta(0.0, 0.0, (StartTime - CurrentTime).microseconds, 0.0, 0.0, 0.0, 0.0))) 
    RawDeltaTime = CurrentTime - EndTime
    DeltaString = str((EndTime - CurrentTime)- datetime.timedelta(0.0, 0.0, (EndTime - CurrentTime).microseconds, 0.0, 0.0, 0.0, 0.0))
    return [CurrentTime, DeltaTime, RawDeltaTime,DeltaString]
class MainApp(QWidget):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        LabelUpdateTimer = QTimer(self)
        LabelUpdateTimer.timeout.connect(MainApp.UpdateLabels)
        LabelUpdateTimer.start(250)
        MainApp.Question = QLabel("Config File Not Found please select the day", alignment=Qt.AlignBottom)
        MainApp.Question.hide()
        MainApp.ClassLabels = []
        main_widget = QWidget()
        content_layout = QVBoxLayout()
        for i in range(GlobalVars.LabelCount):
            MainApp.ClassLabels.append(QLabel("", alignment=Qt.AlignmentFlag.AlignCenter))
            content_layout.addWidget(self.ClassLabels[i])
            MainApp.ClassLabels[i].hide()
            MainApp.ClassLabels[i].setStyleSheet("QLabel {color : white; }")
        main_widget.setLayout(content_layout)
        layout = QHBoxLayout()
        layout.addWidget(main_widget, 4)
        self.setLayout(layout)
        if (datetime.datetime.strptime(GlobalVars.data["SavedDate"], "%Y-%m-%d").date()== datetime.datetime.now().date()):
            GlobalVars.CurrentDay = GlobalVars.data["CurrentDay"]
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    @QtCore.Slot()
    def AboutMenu(self):
        About.__init__(self)
    def SystemTray(self):
        systemTray.__init__(self)
    def UpdateLabels(x=1):
        if GlobalVars.CurrentDay != '':
            for i in range(len(data.getSchedule())):
                MainApp.ClassLabels[i].setText(data.getClass(i)+ " | "+ str(GetDeltaTime(i)[1]))
                MainApp.ClassLabels[i].show()
            for i in range(GlobalVars.LabelCount- (GlobalVars.LabelCount - len(data.getSchedule())),GlobalVars.LabelCount,):
                MainApp.ClassLabels[i].hide()
        else:
            for i in range(GlobalVars.LabelCount):
                MainApp.ClassLabels[i].hide()
class systemTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        self.setIcon(QIcon("/home/carl/Documents/repos/pluto/Pluto.png"))
        self.setToolTip("Pluto")
        self.showMessage("Test","this is a test")
        self.ClassEndTimer = QTimer(self)
        self.ClassEndTimer.timeout.connect(lambda: CheckTime())
        self.ClassEndTimer.start(1000)
        self.menu = QMenu()
        self.menu.setTitle("What day is it?")
        self.menu.addAction("A").triggered.connect(lambda: ButtonClicked("A"))
        self.menu.addAction("B").triggered.connect(lambda: ButtonClicked("C"))
        self.menu.addAction("C").triggered.connect(lambda: ButtonClicked("B"))
        self.menu.addSeparator()
        self.menu.addAction("Reload Config").triggered.connect(lambda: LoadConfig())
        self.menu.addSeparator()
        self.menu.addAction("About Pluto").triggered.connect(MainApp.AboutMenu)
        self.menu.addSeparator()
        self.menu.addAction("Exit Pluto").triggered.connect(lambda: Exit())
        self.setContextMenu(self.menu)
        self.show()
        def Notify(Title,Message,ExpireTime):
            T=str(Title)
            M=str(Message)
            E=int(ExpireTime)
            if systemTray.supportsMessages():
                systemTray.showMessage(self,T, M, QIcon(  "/Pluto.png"),ExpireTime)
        Notify("Pluto","Your system Supports Notifications.",2)
        def CheckTime():
            for i in range(len(data.getSchedule())):
                print(data.getClass(i))
                if GetDeltaTime(i)[2] < datetime.timedelta(0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0):
                    Notify("Pluto","Warning "+str(data.getClass(i))+" Is ending in "+GetDeltaTime(i)[3],999)#"Warning "+str(GlobalVars.data["Days"][GlobalVars.CurrentDay]["Classes"][str(2)]["Name"])+"is ending in:"

class About(QWidget):
    def __init__(self=1, parent=MainApp):
        About.Window = QWidget()
        About.LabelWidget = QWidget()
        About.ItemsWidget = QWidget()
        About.LabelLayout = QVBoxLayout()
        About.ItemsLayout = QVBoxLayout()
        About.IconFrame = QVBoxLayout()
        About.Layout = QHBoxLayout()
        About.L =  [QLabel("App Version:", alignment=Qt.AlignmentFlag.AlignLeft),
                    QLabel("Qt Version:", alignment=Qt.AlignmentFlag.AlignLeft),
                    QLabel("Python Version:", alignment=Qt.AlignmentFlag.AlignLeft),
                    QLabel("Operating system:", alignment=Qt.AlignmentFlag.AlignLeft),
                    QLabel("Config Path:", alignment=Qt.AlignmentFlag.AlignLeft),
                    QLabel("Author:", alignment=Qt.AlignmentFlag.AlignLeft),]
        About.R =  [QLabel(str(GlobalVars.VersionNumber), alignment=Qt.AlignmentFlag.AlignRight),
                    QLabel(str(QtCore.qVersion()), alignment=Qt.AlignmentFlag.AlignRight),
                    QLabel(platform.python_version(), alignment=Qt.AlignmentFlag.AlignRight),
                    QLabel(str(platform.system()) + " " + str(platform.release()),alignment=Qt.AlignmentFlag.AlignRight),
                    QLabel(str(GlobalVars.ParentPath)+GlobalVars.FileName, alignment=Qt.AlignmentFlag.AlignRight),
                    QLabel("Carl Hillam", alignment=Qt.AlignmentFlag.AlignRight),]
        for i in range(len(About.L)):
            About.ItemsLayout.addWidget(About.R[i])
            About.LabelLayout.addWidget(About.L[i])
        About.LabelWidget.setLayout(About.LabelLayout)
        About.ItemsWidget.setLayout(About.ItemsLayout)
        About.Layout.addWidget(About.LabelWidget, 1)
        About.Layout.addWidget(About.ItemsWidget, 2)
        About.Window.setLayout(About.Layout)
        About.Window.setWindowFlags(Qt.WindowType.Popup)
        About.Window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        About.Window.show()
def ConfigChecks():
    if GlobalVars.data["SavedDate"] != str(datetime.datetime.now().date()):
        GlobalVars.data["SavedDate"] = str(datetime.datetime.now().date())
        with open(str(GlobalVars.FileName), "w") as f:
            json.dump(GlobalVars.data, f)
            f.close()
    if GlobalVars.data["CurrentDay"] != str(datetime.datetime.now().date()):
        GlobalVars.data["CurrentDay"] = str(datetime.datetime.now().date())
        with open(str(GlobalVars.FileName), "w") as f:
            json.dump(GlobalVars.data, f)
            f.close()
def ButtonClicked(Day):
    ConfigChecks(Day)
    GlobalVars.CurrentDay = Day
    MainApp.Question.hide()
    MainApp.UpdateLabels()
def Exit():
    sys.exit()
if __name__ == "__main__":
    app = QApplication([])
    tray = QSystemTrayIcon()
    Main = MainApp()
    Main.resize(298, 204)
    app.setApplicationName("Pluto")
    systemTray.__init__(tray)
    app.exec()


