import datetime, sys, platform, json, os, math
from datemath import datemath # type: ignore
from PySide6 import QtCore
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QVBoxLayout,QMenu , QHBoxLayout, QWidget, QLabel, QApplication, QSystemTrayIcon)
from pathlib import Path
import faulthandler ;faulthandler.enable()
class GlobalVars:
    SpacingGoal = 0
    FileName = ""
    FilePath = ""
    CalendarName = ""
    CalendarPath = ""
    IconName = ""
    IconPath = ""
    ParentPath = ""
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
            GlobalVars.CalendarName = "Calendar.Json"
            GlobalVars.IconName = "Pluto.png"
            GlobalVars.IconPath = os.path.join(str(ParentPath) + GlobalVars.IconName)
            GlobalVars.FilePath = os.path.join(str(ParentPath) + GlobalVars.FileName)
            GlobalVars.CalendarPath = os.path.join(str(ParentPath) + GlobalVars.CalendarName)
            os.chdir(ParentPath)
        case _:
            GlobalVars.homePath = str(Path.home())
            ConfigDir = "/.config/Pluto/"
            ParentPath = os.path.join(str(Path.home()) + ConfigDir)
            GlobalVars.FileName = "Config.Json"
            GlobalVars.CalendarName = "Calendar.Json"
            GlobalVars.IconName = "Pluto.png"
            GlobalVars.IconPath = os.path.join(str(ParentPath) + GlobalVars.IconName)
            GlobalVars.FilePath = os.path.join(str(ParentPath) + GlobalVars.FileName)
            GlobalVars.CalendarPath = os.path.join(str(ParentPath) + GlobalVars.CalendarName)
            os.chdir(ParentPath)
    with open(str(GlobalVars.FileName), "r") as f:
        GlobalVars.data = json.load(f)
    with open(str(GlobalVars.CalendarName), "r") as f:
        GlobalVars.Cal = json.load(f)
    GlobalVars.CurrentDay = str(GlobalVars.Cal[str(datetime.datetime.now().month)][str(datetime.datetime.now().day)])
    ConfigChecks()
def ConfigChecks():
    if GlobalVars.data["SavedDate"] != str(datetime.datetime.now().date()):
        GlobalVars.data["SavedDate"] = str(datetime.datetime.now().date())
        with open(str(GlobalVars.FileName), "w") as f:
            json.dump(GlobalVars.data, f)
            f.close()
    if GlobalVars.data["CurrentDay"] != GlobalVars.CurrentDay:
        print("Changing Current Day")
        GlobalVars.data["CurrentDay"] = str(GlobalVars.Cal[str(datetime.datetime.now().month)][str(datetime.datetime.now().day)])
        with open(str(GlobalVars.FileName), "w") as f:
            json.dump(GlobalVars.data, f)
            f.close()
LoadConfig()

class data():
    def getClass(i):
        Classes = GlobalVars.data["Classes"]
        CurrentDay = GlobalVars.data["CurrentDay"]
        Schedule = GlobalVars.data["Days"][CurrentDay]["Schedule"]
        key = Schedule[str(i)]
        Class = Classes[key]
        if i == 9999: Class = "end of school"
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
    def getUserSettings():
        Transparency = GlobalVars.data["UserSettings"]["Transparency"]
        PackUpWarning = GlobalVars.data["UserSettings"]["PackUpWarning"]
        WindowPopupMode = GlobalVars.data["UserSettings"]["WindowPopupMode"]
        PackUpWarningTime = GlobalVars.data["UserSettings"]["PackUpWarningTime"]
        return(Transparency,PackUpWarning,WindowPopupMode,PackUpWarningTime)
    def GetSpacing(i):
        Delta = GlobalVars.SpacingGoal - len(list(data.getClass(i)))
        String=""
        for d in range(Delta):
            String = String+" "
        return(String)
    def CalculateSpacingGoal():
        GlobalVars.SpacingGoal = 0
        for i in range(len(data.getSchedule())):
            test = len(list(data.getClass(i)))
            if test > GlobalVars.SpacingGoal:
                GlobalVars.SpacingGoal = test
    def GetDays(i):
        return(GlobalVars.data["Days"][str(i)]["Name"])
    def GetCurrentDay():
        return()
data.CalculateSpacingGoal()
def GetDeltaTime(d):
    CurrentTime = datetime.datetime.strptime(str(datetime.datetime.now().time().isoformat()), "%H:%M:%S.%f")
    EndTime = datetime.datetime.strptime(str(datetime.datetime.strptime((data.getTimes(d,2)),"%I:%M %p",)),"%Y-%d-%m %H:%M:%S",)
    StartTime = datetime.datetime.strptime(str(datetime.datetime.strptime((data.getTimes(d,1)),"%I:%M %p",)), "%Y-%d-%m %H:%M:%S")
    if CurrentTime - EndTime > datetime.timedelta(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0):          DeltaTime = "Done               "
    elif CurrentTime - EndTime < datetime.timedelta(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0):        
        DeltaTime = "Time left:  " + str((EndTime - CurrentTime)- datetime.timedelta(0.0, 0.0, (EndTime - CurrentTime).microseconds, 0.0, 0.0, 0.0, 0.0))
    if CurrentTime < StartTime:                                                                DeltaTime = "Time Until: " + str(((StartTime - CurrentTime)- datetime.timedelta(0.0, 0.0, (StartTime - CurrentTime).microseconds, 0.0, 0.0, 0.0, 0.0))) 
    RawDeltaTime = (EndTime - CurrentTime)- datetime.timedelta(0.0, 0.0, (EndTime - CurrentTime).microseconds, 0.0, 0.0, 0.0, 0.0)
    DeltaString = str((EndTime - CurrentTime)- datetime.timedelta(0.0, 0.0, (EndTime - CurrentTime).microseconds, 0.0, 0.0, 0.0, 0.0))
    if GlobalVars.CurrentDay == "-1":
        return [CurrentTime, "", datetime.timedelta(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),str(datetime.timedelta(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))]
    else:
        return [CurrentTime, DeltaTime, RawDeltaTime,DeltaString]
class MainApp(QWidget):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        LabelUpdateTimer = QTimer(self)
        LabelUpdateTimer.timeout.connect(MainApp.UpdateLabels)
        LabelUpdateTimer.start(250)
        MainApp.ClassLabels = []
        main_widget = QWidget()
        content_layout = QVBoxLayout()
        for i in range(GlobalVars.LabelCount):
            MainApp.ClassLabels.append(QLabel("", alignment=Qt.AlignmentFlag.AlignCenter))
            content_layout.addWidget(self.ClassLabels[i])
            MainApp.ClassLabels[i].hide()
            if data.getUserSettings()[1] == "True": MainApp.ClassLabels[i].setStyleSheet("QLabel {color : white; }")
        main_widget.setLayout(content_layout)
        layout = QHBoxLayout()
        layout.addWidget(main_widget, 1)
        self.setLayout(layout)
        if data.getUserSettings()[2] == "True": self.setWindowFlags(Qt.WindowType.Popup)
        if data.getUserSettings()[1] == "True": self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    @QtCore.Slot()
    def AboutMenu(self):
        About.__init__(self)
    def SystemTray(self):
        systemTray.__init__(self)
    def UpdateLabels(x=1):
        if GlobalVars.CurrentDay != '':
            for i in range(len(data.getSchedule())):
                if i == 0:
                    MainApp.ClassLabels[i].setText(data.getClass(i)+data.GetSpacing(i)+ " | "+ str(GetDeltaTime(i)[1]))
                    MainApp.ClassLabels[i].show()
                else:
                    MainApp.ClassLabels[i].setText(data.getClass(i)+data.GetSpacing(i)+ " | "+ str(GetDeltaTime(i)[1]))
                    MainApp.ClassLabels[i].show()
            for i in range(GlobalVars.LabelCount - (GlobalVars.LabelCount - len(data.getSchedule())),GlobalVars.LabelCount,):
                MainApp.ClassLabels[i].hide()
        else:
            for i in range(GlobalVars.LabelCount):
                MainApp.ClassLabels[i].hide()
class systemTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        self.setIcon(QIcon(GlobalVars.IconPath))
        self.setToolTip("Pluto")
        self.ClassEndTimer = QTimer(self)
        self.ClassEndTimer.timeout.connect(lambda: CheckTime())
        if data.getUserSettings()[1]: self.ClassEndTimer.start(1000)
        self.menu = QMenu()
        self.menu.setTitle("What day is it?")
        #for i in range(len(GlobalVars.data["Days"])): 
        #    self.menu.addAction(str(i)).triggered.connect(lambda: ButtonClicked(str(i)))
        #    self.menu.addSeparator()
        self.menu.addAction("A").triggered.connect(lambda: ButtonClicked("0"))
        self.menu.addAction("B").triggered.connect(lambda: ButtonClicked("1"))
        self.menu.addAction("C").triggered.connect(lambda: ButtonClicked("2"))
        self.menu.addAction("Late Start").triggered.connect(lambda: ButtonClicked("3"))
        self.menu.addAction("Pep Rally").triggered.connect(lambda: ButtonClicked("4"))
        self.menu.addSeparator()
        #Transparency,PackUpWarning,WindowPopupMode
        self.menu.addAction("Toggle Transparency").triggered.connect(lambda: SetConfig(1))
        self.menu.addAction("Toggle PackUpWarning").triggered.connect(lambda: SetConfig(2))
        self.menu.addAction("Toggle WindowPopupMode").triggered.connect(lambda: SetConfig(3))
        self.menu.addAction("Reload Config").triggered.connect(lambda: LoadConfig())
        self.menu.addSeparator()
        self.menu.addAction("About Pluto").triggered.connect(MainApp.AboutMenu)
        self.menu.addSeparator()
        self.menu.addAction("Exit Pluto").triggered.connect(lambda: Exit())
        self.setContextMenu(self.menu)
        self.activated.connect(lambda: StartMain())
        if data.getUserSettings()[1] == "True": self.menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.show()
        
        def StartMain():
            if Main.isVisible(): Main.hide()
            else: Main.show()
        def Notify(Title,Message,ExpireTime):
            T=str(Title)
            M=str(Message)
            E=int(ExpireTime)
            if systemTray.supportsMessages():
                systemTray.showMessage(self,T, M, QIcon(GlobalVars.IconPath),ExpireTime)
        Notify("Pluto","Your system Supports Notifications.",2)
        def CheckTime():
            for i in range(len(data.getSchedule())):
                if GetDeltaTime(i)[2] < datetime.timedelta(GetDeltaTime(i)[2].days, 0.0, 0.0, 0.0, data.getUserSettings()[3], 0.0, 0.0):
                    if data.getClass(i+1) == "End of School": Notify("Pluto", "Warning School Is ending in " + GetDeltaTime(i)[3], 999)
                    else: Notify("Pluto", "Warning " + str(data.getClass(i)) + " Is ending in " + GetDeltaTime(i)[3] + "\n" + "Your next class is: "+str(data.getClass(i+1)), 999)
        def SetConfig(i,Time=0.0):
            match i:
                case 1: 
                    if GlobalVars.data["UserSettings"]["Transparency"] == "False":
                        GlobalVars.data["UserSettings"]["Transparency"] = str("True")
                        with open(str(GlobalVars.FileName), "w") as f:
                            json.dump(GlobalVars.data, f)
                            f.close()
                    elif GlobalVars.data["UserSettings"]["Transparency"] == "True":
                        GlobalVars.data["UserSettings"]["Transparency"] = str("False")
                        with open(str(GlobalVars.FileName), "w") as f:
                            json.dump(GlobalVars.data, f)
                            f.close()
                case 2: 
                    if GlobalVars.data["UserSettings"]["PackUpWarning"] == "False":
                        GlobalVars.data["UserSettings"]["PackUpWarning"] = str("True")
                        with open(str(GlobalVars.FileName), "w") as f:
                            json.dump(GlobalVars.data, f)
                            f.close()
                    elif GlobalVars.data["UserSettings"]["PackUpWarning"] == "True":
                        GlobalVars.data["UserSettings"]["PackUpWarning"] = str("False")
                        with open(str(GlobalVars.FileName), "w") as f:
                            json.dump(GlobalVars.data, f)
                            f.close()
                case 3: 
                    if GlobalVars.data["UserSettings"]["WindowPopupMode"] == "False":
                        GlobalVars.data["UserSettings"]["WindowPopupMode"] = str("True")
                        with open(str(GlobalVars.FileName), "w") as f:
                            json.dump(GlobalVars.data, f)
                            f.close()
                    elif GlobalVars.data["UserSettings"]["WindowPopupMode"] == "True":
                        GlobalVars.data["UserSettings"]["WindowPopupMode"] = str("False")
                        with open(str(GlobalVars.FileName), "w") as f:
                            json.dump(GlobalVars.data, f)
                            f.close()
            Notify("Pluto","Changes to config wont apply until Pluto has been restarted",1500)
            LoadConfig()
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
        if data.getUserSettings()[2] == "True": About.Window.setWindowFlags(Qt.WindowType.Popup)
        if data.getUserSettings()[1] == "True": About.Window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        About.Window.show()

def ButtonClicked(Day):
    print(Day)
    GlobalVars.CurrentDay = Day
    ConfigChecks()
    data.CalculateSpacingGoal()
    MainApp.UpdateLabels()
def Exit():
    sys.exit()
if __name__ == "__main__":
    app = QApplication([])
    tray = QSystemTrayIcon()
    Main = MainApp()
    Main.resize(500, 200)
    app.setApplicationName("Pluto")
    systemTray.__init__(tray)
    app.exec()