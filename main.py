from sys import exit as sysExit
from PySide6.QtGui import QScreen, QIcon
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets \
    import QApplication, QListWidgetItem, QMessageBox
from json import load as jsonLoad

class Main:
    class AccountScrollItem(QListWidgetItem):
        def __init__(self, data):
            super(Main.AccountScrollItem, self).__init__()
            # 将数据中的 title 渲染为条目
            try:
                self.setText(data["title"])
            except KeyError as e:
                # print(e)
                self.setText("[空标题]")
            # 将数据绑定在 addon 上
            self.addon = data
            # 在 loadAccountFromData 时赋值
            # self.index = -1

    def __init__(self):
        super(Main, self).__init__()
        self.currentIndex = -1
        self.data = list()

        # 从ui文件中加载UI定义
        uiFile = QFile("./ui-file/t1.ui")
        uiFile.open(QFile.ReadOnly)
        uiFile.close()

        # 从UI定义中动态创建一个相应的窗口对象
        self.ui = QUiLoader().load(uiFile)
        uiIcon = QIcon("./ui-file/favicon.ico")
        self.ui.setWindowIcon(uiIcon)
        if not self.ui:
            print(QUiLoader().errorString())
            sysExit(-1)

        self.eventBinding()

        self.loadDateFromFile()

        self.loadAccountScrollFromData()

        self.displayCenter()

    def loadDateFromFile(self):
        try:
            with open('./data.json', 'r', encoding='utf8') as file:
                self.data = jsonLoad(file)
        except IOError as e:
            with open('./data.json', 'w', encoding='utf8') as temp:
                temp.write(str(list()).replace("'", "\"")
                           .replace("},", "},\n ")
                           .replace("[", "[\n  ")
                           .replace("}]", "}\n]"))


    def eventBinding(self):
        # 信号处理 & 事件绑定
        # self.ui.buttonEdit = self.ui.findChild(QPushButton, "buttonEdit")
        self.ui.buttonEdit.clicked.connect(self.editData)
        self.ui.buttonDelete.clicked.connect(self.deleteAccount)
        self.ui.accountScrollObj.itemClicked.connect(self.accountScrollSelect)
        self.ui.buttonAbout.clicked.connect(self.about)
        self.ui.buttonAdd.clicked.connect(self.addAccount)

    def loadAccountScrollFromData(self):
        data = self.data
        _count = 0
        _first = True

        for item in data:
            # 这里不是方法，而是一个内部类 AccountScrollItem
            temp = self.AccountScrollItem(item)

            # temp.addon["index"] = _count
            temp.index = _count
            temp.setToolTip(item["info"])
            _count += 1
            self.ui.accountScrollObj.addItem(temp)
            # self.ui.gb_list_scroll_list.accountScrollSelected(temp)
            if _first:
                self.accountScrollSelect(temp)
                _first = False

    def editData(self):
        index = self.currentIndex
        data = self.data

        data[index]["title"] = self.ui.titleObj.text()
        data[index]["account"] = self.ui.accountObj.text()
        data[index]["password"] = self.ui.pwdObj.text()
        data[index]["info"] = self.ui.tipObj.toPlainText()
        # print("保存")
        self.saveDataToFileAndReload()

    def saveDataToFileAndReload(self):
        data = self.data
        with open('./data.json', 'w', encoding='utf8') as temp:
            temp.write(str(data).replace("'", "\"")
                       .replace("},", "},\n ")
                       .replace("[", "[\n  ")
                       .replace("}]", "}\n]"))

        # 清空列表重新加载
        self.ui.accountScrollObj.clear()
        self.loadAccountScrollFromData()

    def accountScrollSelect(self, obj):
        # print(self, obj.text(), obj.addon)
        title = self.ui.titleObj
        account = self.ui.accountObj
        pwd = self.ui.pwdObj
        tip = self.ui.tipObj
        data = obj.addon

        try:
            title.setText(data["title"])
            account.setText(data["account"])
            pwd.setText(data["password"])
            tip.setText(data["info"])
        except KeyError as e:
            data[e] = ""
            obj.addon = data
            pass

        self.currentIndex = obj.index

    def about(self):
        temp = QMessageBox()
        temp.about(self.ui, "About Me", "AccountBox v1.1  \n鲸某人 \ heheking\n2022.03.19")

    def addAccount(self):
        temp = dict()
        if len(self.ui.newTitleObj.text()) == 0 or self.ui.newTitleObj.text().isspace():
            QMessageBox().about(self.ui, "添加失败", "标题不能为空")
            return
        else:
            temp["title"] = self.ui.newTitleObj.text()
        temp["account"] = self.ui.newAccountObj.text()
        temp["password"] = self.ui.newPwdObj.text()
        temp["info"] = self.ui.newTipObj.toPlainText()
        self.data.append(temp)

        self.saveDataToFileAndReload()

        print(self.data)

        QMessageBox().about(self.ui, "添加账号", "添加成功")
        # 输入框清空
        self.ui.newTitleObj.setText("")
        self.ui.newAccountObj.setText("")
        self.ui.newPwdObj.setText("")
        self.ui.newTipObj.setPlainText("")

        # 跳回编辑页
        self.ui.actionTab.setCurrentIndex(0)
        # 列表选中最后一个（刚添加的）
        # self.ui.accountScrollObj. setCurrentRow(len(self.data) - 1)
        
    def deleteAccount(self):
        data = self.data
        cur = self.currentIndex
        del data[cur]
        
        # 清空列表重新加载
        self.saveDataToFileAndReload()
        self.ui.titleObj.setText("")
        self.ui.accountObj.setText("")
        self.ui.pwdObj.setText("")
        self.ui.tipObj.setPlainText("")

    # 居中显示
    def displayCenter(self):
        # Get Screen geometry
        SrcSize = QScreen.availableGeometry(QApplication.primaryScreen())
        # Set X Position Center
        frmX = (SrcSize.width() - self.ui.width()) / 2
        # Set Y Position Center
        frmY = (SrcSize.height() - self.ui.height()) / 2
        # Set Form's Center Location
        self.ui.move(frmX, frmY)
