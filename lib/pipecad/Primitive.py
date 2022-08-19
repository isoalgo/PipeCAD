# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :: Welcome to PipeCAD!                                      ::
# ::  ____                        ____     ______  ____       ::
# :: /\  _`\   __                /\  _`\  /\  _  \/\  _`\     ::
# :: \ \ \L\ \/\_\  _____      __\ \ \/\_\\ \ \L\ \ \ \/\ \   ::
# ::  \ \ ,__/\/\ \/\ '__`\  /'__`\ \ \/_/_\ \  __ \ \ \ \ \  ::
# ::   \ \ \/  \ \ \ \ \L\ \/\  __/\ \ \L\ \\ \ \/\ \ \ \_\ \ ::
# ::    \ \_\   \ \_\ \ ,__/\ \____\\ \____/ \ \_\ \_\ \____/ ::
# ::     \/_/    \/_/\ \ \/  \/____/ \/___/   \/_/\/_/\/___/  ::
# ::                  \ \_\                                   ::
# ::                   \/_/                                   ::
# ::                                                          ::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# PipeCAD - Piping Design Software.
# Copyright (C) 2022 Wuhan OCADE IT. Co., Ltd.
# Author: Shing Liu(eryar@163.com)
# Date: 12:20 2022-04-21

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *


class BoxDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.boxItem = None
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Create Box"))

        self.horizontalLayout = QHBoxLayout(self)
        self.verticalLayout = QVBoxLayout()

        self.formLayout = QFormLayout()

        # Name
        self.comboName = QComboBox()
        self.textName = QLineEdit()
        self.textName.setMinimumWidth(150)

        self.comboName.addItem(QT_TRANSLATE_NOOP("Design", "Create"))
        self.comboName.addItem(QT_TRANSLATE_NOOP("Design", "Modify"))
        self.comboName.activated.connect(self.activateName)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.comboName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelNegative = QLabel(QT_TRANSLATE_NOOP("Design", "Negative"))
        self.checkNegative = QCheckBox()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelNegative)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.checkNegative)

        self.verticalLayout.addLayout(self.formLayout)

        # Horizontal Line
        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Dimensions.
        self.formLayout = QFormLayout()

        self.labelXlen = QLabel(QT_TRANSLATE_NOOP("Design", "X Length"))
        self.textXlen = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelXlen)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textXlen)
        
        self.labelYlen = QLabel(QT_TRANSLATE_NOOP("Design", "Y Length"))
        self.textYlen = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelYlen)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textYlen)
        
        self.labelZlen = QLabel(QT_TRANSLATE_NOOP("Design", "Z Length"))
        self.textZlen = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelZlen)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textZlen)

        self.verticalLayout.addLayout(self.formLayout)

        # Horizontal Line
        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Position.
        self.formLayout = QFormLayout()

        self.labelPx = QLabel(QT_TRANSLATE_NOOP("Design", "East"))
        self.textPx = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelPx)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textPx)

        self.labelPy = QLabel(QT_TRANSLATE_NOOP("Design", "North"))
        self.textPy = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPy)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textPy)

        self.labelPz = QLabel(QT_TRANSLATE_NOOP("Design", "Up"))
        self.textPz = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPz)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPz)

        self.verticalLayout.addLayout(self.formLayout)

        # Vertical Spacer.
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)

        self.horizontalLayout.addLayout(self.verticalLayout)

        # Diagram
        self.labelDiagram = QLabel()
        self.labelDiagram.setMinimumSize(QSize(280, 360))
        self.labelDiagram.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/box-diagram.png"))
        self.horizontalLayout.addWidget(self.labelDiagram)
    # setupUi

    def activateName(self):
        self.boxItem = None

        aIndex = self.comboName.currentIndex
        if aIndex == 1:
            # modify box
            self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Modify Box"))

            aTreeItem = PipeCad.CurrentItem()
            if aTreeItem.Type not in {"BOX", "NBOX"}:
                QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Design", "Please select BOX/NBOX to modify!"))
                return
            # if

            self.boxItem = aTreeItem

            self.textName.setText(aTreeItem.Name)
            self.checkNegative.setChecked(aTreeItem.Type == "NBOX")
            self.checkNegative.setEnabled(False)

            self.textXlen.setText(str(aTreeItem.Xlength))
            self.textYlen.setText(str(aTreeItem.Ylength))
            self.textZlen.setText(str(aTreeItem.Zlength))

            aPosition = aTreeItem.Position
            self.textPx.setText(str(aPosition.X))
            self.textPy.setText(str(aPosition.Y))
            self.textPz.setText(str(aPosition.Z))
        else:
            self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Create Box"))
            self.checkNegative.setEnabled(True)
        # if
    # activateName

    def createBox(self):
        aName = self.textName.text

        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        try:
            PipeCad.StartTransaction("Create Box")

            if self.checkNegative.checked:
                PipeCad.CreateItem("NBOX", aName)
            else:
                PipeCad.CreateItem("BOX", aName)
            # if

            aTreeItem = PipeCad.CurrentItem()
            aTreeItem.Xlength = float(self.textXlen.text)
            aTreeItem.Ylength = float(self.textYlen.text)
            aTreeItem.Zlength = float(self.textZlen.text)
            aTreeItem.Position = Position(aPx, aPy, aPz, aTreeItem.Owner)

            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try
    # createBox

    def modifyBox(self):
        if self.boxItem is None:
            return
        # if

        aName = self.textName.text

        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        PipeCad.StartTransaction("Modify Box")

        aTreeItem = self.boxItem
        aTreeItem.Xlength = float(self.textXlen.text)
        aTreeItem.Ylength = float(self.textYlen.text)
        aTreeItem.Zlength = float(self.textZlen.text)
        aTreeItem.Position = Position(aPx, aPy, aPz, aTreeItem.Owner)

        PipeCad.CommitTransaction()
    # modifyBox

    def accept(self):
        aIndex = self.comboName.currentIndex
        if aIndex == 0:
            self.createBox()
        else:
            self.modifyBox()
        # if

        QDialog.accept(self)
    # accept
# BoxDialog

# Singleton Instance.
aBoxDlg = BoxDialog(PipeCad)

def CreateBox():
    aBoxDlg.show()
# CreateBox

class CylinderDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.cyliItem = None
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Create Cylinder"))

        self.horizontalLayout = QHBoxLayout(self)
        self.verticalLayout = QVBoxLayout()

        self.formLayout = QFormLayout()

        # Name
        self.comboName = QComboBox()
        self.textName = QLineEdit()
        self.textName.setMinimumWidth(150)

        self.comboName.addItem(QT_TRANSLATE_NOOP("Design", "Create"))
        self.comboName.addItem(QT_TRANSLATE_NOOP("Design", "Modify"))
        self.comboName.activated.connect(self.activateName)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.comboName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelNegative = QLabel(QT_TRANSLATE_NOOP("Design", "Negative"))
        self.checkNegative = QCheckBox()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelNegative)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.checkNegative)

        self.verticalLayout.addLayout(self.formLayout)

        # Horizontal Line
        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Dimensions.
        self.formLayout = QFormLayout()

        self.labelDiameter = QLabel(QT_TRANSLATE_NOOP("Design", "Diameter"))
        self.textDiameter = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelDiameter)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textDiameter)
        
        self.labelHeight = QLabel(QT_TRANSLATE_NOOP("Design", "Height"))
        self.textHeight = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelHeight)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textHeight)

        self.verticalLayout.addLayout(self.formLayout)

        # Horizontal Line
        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Position.
        self.formLayout = QFormLayout()

        self.labelPx = QLabel(QT_TRANSLATE_NOOP("Design", "East"))
        self.textPx = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelPx)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textPx)

        self.labelPy = QLabel(QT_TRANSLATE_NOOP("Design", "North"))
        self.textPy = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPy)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textPy)

        self.labelPz = QLabel(QT_TRANSLATE_NOOP("Design", "Up"))
        self.textPz = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPz)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPz)

        self.verticalLayout.addLayout(self.formLayout)

        # Vertical Spacer.
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)

        self.horizontalLayout.addLayout(self.verticalLayout)

        # Diagram
        self.labelDiagram = QLabel()
        self.labelDiagram.setMinimumSize(QSize(280, 360))
        self.labelDiagram.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/cylinder-diagram.png"))
        self.horizontalLayout.addWidget(self.labelDiagram)
    # setupUi

    def activateName(self):
        self.cyliItem = None

        aIndex = self.comboName.currentIndex
        if aIndex == 1:
            # modify cylinder
            self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Modify Cylinder"))

            aTreeItem = PipeCad.CurrentItem()
            if aTreeItem.Type not in {"CYLI", "NCYL"}:
                QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Design", "Please select CYLI/NCYL to modify!"))
                return
            # if

            self.cyliItem = aTreeItem

            self.textName.setText(aTreeItem.Name)
            self.checkNegative.setChecked(aTreeItem.Type == "NCYL")
            self.checkNegative.setEnabled(False)

            self.textDiameter.setText(str(aTreeItem.Diameter))
            self.textHeight.setText(str(aTreeItem.Height))

            aPosition = aTreeItem.Position
            self.textPx.setText(str(aPosition.X))
            self.textPy.setText(str(aPosition.Y))
            self.textPz.setText(str(aPosition.Z))

        else:
            # create cylinder
            self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Create Cylinder"))
            self.checkNegative.setEnabled(True)
        # if

    # activateName

    def createCylinder(self):
        aName = self.textName.text

        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        try:
            PipeCad.StartTransaction("Create Cylinder")

            if self.checkNegative.checked:
                PipeCad.CreateItem("NCYL", aName)
            else:
                PipeCad.CreateItem("CYLI", aName)
            # if

            aTreeItem = PipeCad.CurrentItem()
            aTreeItem.Diameter = float(self.textDiameter.text)
            aTreeItem.Height = float(self.textHeight.text)
            aTreeItem.Position = Position(aPx, aPy, aPz, aTreeItem.Owner)

            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try
    # createCylinder

    def modifyCylinder(self):
        if self.cyliItem is None:
            return
        # if

        aName = self.textName.text

        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        PipeCad.StartTransaction("Modify Cylinder")

        aTreeItem = self.cyliItem
        aTreeItem.Diameter = float(self.textDiameter.text)
        aTreeItem.Height = float(self.textHeight.text)
        aTreeItem.Position = Position(aPx, aPy, aPz, aTreeItem.Owner)

        PipeCad.CommitTransaction()
    # modifyCylinder

    def accept(self):
        aIndex = self.comboName.currentIndex
        if aIndex == 0:
            self.createCylinder()
        else:
            self.modifyCylinder()
        # if

        QDialog.accept(self)
    # accept
# CylinderDialog

# Singleton Instance.
aCylinderDlg = CylinderDialog(PipeCad)

def CreateCylinder():
    aCylinderDlg.show()
# CreateCylinder


class ConeDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(self.tr("Create Cone"))

        self.horizontalLayout = QHBoxLayout(self)
        self.verticalLayout = QVBoxLayout()

        self.formLayout = QFormLayout()

        # Name
        self.comboName = QComboBox()
        self.textName = QLineEdit()
        self.textName.setMinimumWidth(150)

        self.comboName.addItem(self.tr("Create"))
        self.comboName.addItem(self.tr("Modify"))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.comboName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelNegative = QLabel(self.tr("Negative"))
        self.checkNegative = QCheckBox()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelNegative)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.checkNegative)

        self.verticalLayout.addLayout(self.formLayout)

        # Horizontal Line
        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Dimensions.
        self.formLayout = QFormLayout()

        self.labelTdiameter = QLabel(self.tr("Top Diameter"))
        self.textTdiameter = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelTdiameter)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textTdiameter)
        
        self.labelBdiameter = QLabel(self.tr("Bottom Diameter"))
        self.textBdiameter = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelBdiameter)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textBdiameter)
        
        self.labelHeight = QLabel(self.tr("Height"))
        self.textHeight = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelHeight)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textHeight)

        self.verticalLayout.addLayout(self.formLayout)

        # Horizontal Line
        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Position.
        self.formLayout = QFormLayout()

        self.labelPx = QLabel(self.tr("East"))
        self.textPx = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelPx)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textPx)

        self.labelPy = QLabel(self.tr("North"))
        self.textPy = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPy)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textPy)

        self.labelPz = QLabel(self.tr("Up"))
        self.textPz = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPz)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPz)

        self.verticalLayout.addLayout(self.formLayout)

        # Vertical Spacer.
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)

        self.horizontalLayout.addLayout(self.verticalLayout)

        # Diagram
        self.labelDiagram = QLabel()
        self.labelDiagram.setMinimumSize(QSize(280, 360))
        self.labelDiagram.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/cone-diagram.png"))
        self.horizontalLayout.addWidget(self.labelDiagram)
    # setupUi

    def accept(self):
        aName = self.textName.text

        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        try:
            PipeCad.StartTransaction("Create Cone")

            PipeCad.CreateItem("CONE", aName)

            aTreeItem = PipeCad.CurrentItem()
            aTreeItem.Tdiameter = float(self.textTdiameter.text)
            aTreeItem.Bdiameter = float(self.textBdiameter.text)
            aTreeItem.Height = float(self.textHeight.text)
            aTreeItem.Position = Position(aPx, aPy, aPz, aTreeItem.Owner)

            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try

        QDialog.accept(self)
    # accept
# ConeDialog

# Singleton Instance.
aConeDlg = ConeDialog(PipeCad)

def CreateCone():
    aConeDlg.show()
# CreateCone


class DishDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(self.tr("Create Dish"))

        self.horizontalLayout = QHBoxLayout(self)
        self.verticalLayout = QVBoxLayout()

        self.formLayout = QFormLayout()

        # Name
        self.comboName = QComboBox()
        self.textName = QLineEdit()
        self.textName.setMinimumWidth(150)

        self.comboName.addItem(self.tr("Create"))
        self.comboName.addItem(self.tr("Modify"))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.comboName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelNegative = QLabel(self.tr("Negative"))
        self.checkNegative = QCheckBox()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelNegative)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.checkNegative)

        self.verticalLayout.addLayout(self.formLayout)

        # Horizontal Line
        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Dimensions.
        self.formLayout = QFormLayout()

        self.labelDiameter = QLabel(self.tr("Diameter"))
        self.textDiameter = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelDiameter)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textDiameter)
        
        self.labelRadius = QLabel(self.tr("Radius"))
        self.textRadius = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelRadius)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textRadius)
        
        self.labelHeight = QLabel(self.tr("Height"))
        self.textHeight = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelHeight)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textHeight)

        self.verticalLayout.addLayout(self.formLayout)

        # Horizontal Line
        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Position.
        self.formLayout = QFormLayout()

        self.labelPx = QLabel(self.tr("East"))
        self.textPx = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelPx)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textPx)

        self.labelPy = QLabel(self.tr("North"))
        self.textPy = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPy)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textPy)

        self.labelPz = QLabel(self.tr("Up"))
        self.textPz = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPz)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPz)

        self.verticalLayout.addLayout(self.formLayout)

        # Vertical Spacer.
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)

        self.horizontalLayout.addLayout(self.verticalLayout)

        # Diagram
        self.labelDiagram = QLabel()
        self.labelDiagram.setMinimumSize(QSize(280, 360))
        self.labelDiagram.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/dish-diagram.png"))
        self.horizontalLayout.addWidget(self.labelDiagram)
    # setupUi

    def accept(self):
        aName = self.textName.text

        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        try:
            PipeCad.StartTransaction("Create Dish")

            PipeCad.CreateItem("DISH", aName)

            aTreeItem = PipeCad.CurrentItem()
            aTreeItem.Diameter = float(self.textDiameter.text)
            aTreeItem.Radius = float(self.textRadius.text)
            aTreeItem.Height = float(self.textHeight.text)
            aTreeItem.Position = Position(aPx, aPy, aPz, aTreeItem.Owner)

            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try

        QDialog.accept(self)
    # accept
# DishDialog

# Singleton Instance.
aDishDlg = DishDialog(PipeCad)

def CreateDish():
    aDishDlg.show()
# CreateDish


class CircularDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(self.tr("Create Circular Torus"))

        self.horizontalLayout = QHBoxLayout(self)
        self.verticalLayout = QVBoxLayout()

        self.formLayout = QFormLayout()

        # Name
        self.comboName = QComboBox()
        self.textName = QLineEdit()
        self.textName.setMinimumWidth(150)

        self.comboName.addItem(self.tr("Create"))
        self.comboName.addItem(self.tr("Modify"))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.comboName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelNegative = QLabel(self.tr("Negative"))
        self.checkNegative = QCheckBox()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelNegative)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.checkNegative)

        self.verticalLayout.addLayout(self.formLayout)

        # Horizontal Line
        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Dimensions.
        self.formLayout = QFormLayout()

        self.labelRi = QLabel(self.tr("Inside Radius"))
        self.textRi = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelRi)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textRi)
        
        self.labelRo = QLabel(self.tr("Outside Radius"))
        self.textRo = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelRo)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textRo)
        
        self.labelAngle = QLabel(self.tr("Angle"))
        self.textAngle = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelAngle)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textAngle)

        self.verticalLayout.addLayout(self.formLayout)

        # Horizontal Line
        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Position.
        self.formLayout = QFormLayout()

        self.labelPx = QLabel(self.tr("East"))
        self.textPx = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelPx)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textPx)

        self.labelPy = QLabel(self.tr("North"))
        self.textPy = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPy)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textPy)

        self.labelPz = QLabel(self.tr("Up"))
        self.textPz = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPz)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPz)

        self.verticalLayout.addLayout(self.formLayout)

        # Vertical Spacer.
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)

        self.horizontalLayout.addLayout(self.verticalLayout)

        # Diagram
        self.labelDiagram = QLabel()
        self.labelDiagram.setMinimumSize(QSize(280, 360))
        self.labelDiagram.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/ctorus-diagram.png"))
        self.horizontalLayout.addWidget(self.labelDiagram)
    # setupUi

    def accept(self):
        aName = self.textName.text

        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        try:
            PipeCad.StartTransaction("Create Circular Torus")

            PipeCad.CreateItem("CTOR", aName)

            aTreeItem = PipeCad.CurrentItem()
            aTreeItem.InsideRadius = float(self.textRi.text)
            aTreeItem.OutsideRadius = float(self.textRo.text)
            aTreeItem.Angle = float(self.textAngle.text)
            aTreeItem.Position = Position(aPx, aPy, aPz, aTreeItem.Owner)

            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try

        QDialog.accept(self)
    # accept
# CircularDialog

# Singleton Instance.
aCircularTorusDlg = CircularDialog(PipeCad)

def CreateCircularTorus():
    aCircularTorusDlg.show()
# CreateCircularTorus


class RectangularDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(self.tr("Create Rectangular Torus"))

        self.horizontalLayout = QHBoxLayout(self)
        self.verticalLayout = QVBoxLayout()

        self.formLayout = QFormLayout()

        # Name
        self.comboName = QComboBox()
        self.textName = QLineEdit()
        self.textName.setMinimumWidth(150)

        self.comboName.addItem(self.tr("Create"))
        self.comboName.addItem(self.tr("Modify"))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.comboName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelNegative = QLabel(self.tr("Negative"))
        self.checkNegative = QCheckBox()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelNegative)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.checkNegative)

        self.verticalLayout.addLayout(self.formLayout)

        # Horizontal Line
        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Dimensions.
        self.formLayout = QFormLayout()

        self.labelRi = QLabel(self.tr("Inside Radius"))
        self.textRi = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelRi)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textRi)
        
        self.labelRo = QLabel(self.tr("Outside Radius"))
        self.textRo = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelRo)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textRo)
        
        self.labelHeight = QLabel(self.tr("Height"))
        self.textHeight = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelHeight)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textHeight)
        
        self.labelAngle = QLabel(self.tr("Angle"))
        self.textAngle = QLineEdit("0.0")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelAngle)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.textAngle)

        self.verticalLayout.addLayout(self.formLayout)

        # Horizontal Line
        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Position.
        self.formLayout = QFormLayout()

        self.labelPx = QLabel(self.tr("East"))
        self.textPx = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelPx)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textPx)

        self.labelPy = QLabel(self.tr("North"))
        self.textPy = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPy)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textPy)

        self.labelPz = QLabel(self.tr("Up"))
        self.textPz = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPz)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPz)

        self.verticalLayout.addLayout(self.formLayout)

        # Vertical Spacer.
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)

        self.horizontalLayout.addLayout(self.verticalLayout)

        # Diagram
        self.labelDiagram = QLabel()
        self.labelDiagram.setMinimumSize(QSize(280, 360))
        self.labelDiagram.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/rtorus-diagram.png"))
        self.horizontalLayout.addWidget(self.labelDiagram)
    # setupUi

    def accept(self):
        aName = self.textName.text

        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        try:
            PipeCad.StartTransaction("Create Rectangular Torus")

            PipeCad.CreateItem("RTOR", aName)

            aTreeItem = PipeCad.CurrentItem()
            aTreeItem.InsideRadius = float(self.textRi.text)
            aTreeItem.OutsideRadius = float(self.textRo.text)
            aTreeItem.Height = float(self.textHeight.text)
            aTreeItem.Angle = float(self.textAngle.text)
            aTreeItem.Position = Position(aPx, aPy, aPz, aTreeItem.Owner)

            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try

        QDialog.accept(self)
    # accept
# RectangularDialog

# Singleton Instance.
aRectangularTorusDlg = RectangularDialog(PipeCad)

def CreateRectangularTorus():
    aRectangularTorusDlg.show()
# CreateCircularTorus


class ExtrusionDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)

        self.aidNumber = PipeCad.NextAidNumber()

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Primitive", "Create Extrusion"))

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        # Name
        self.labelName = QLabel(QT_TRANSLATE_NOOP("Primitive", "Name"))
        self.textName = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        # Thickness
        self.labelThickness = QLabel(QT_TRANSLATE_NOOP("Primitive", "Thickness"))
        self.textThickness = QLineEdit("10")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelThickness)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textThickness)

        self.verticalLayout.addLayout(self.formLayout)

        # Polyline vertex.
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["X", "Y", "Z", "Radius"])
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(68)
        self.tableWidget.verticalHeader().setMinimumSectionSize(16)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)

        self.verticalLayout.addWidget(self.tableWidget)

        # Action box.
        self.horizontalLayout = QHBoxLayout()

        # Add, Remove
        self.buttonAdd = QPushButton(QT_TRANSLATE_NOOP("Primitive", "Add"))
        self.buttonAdd.clicked.connect(self.addVertex)

        self.buttonRemove = QPushButton(QT_TRANSLATE_NOOP("Primitive", "Remove"))
        self.buttonRemove.clicked.connect(self.removeVertex)

        self.buttonPreview = QPushButton(QT_TRANSLATE_NOOP("Primitive", "Preview"))
        self.buttonPreview.clicked.connect(self.previewLoop)

        self.horizontalLayout.addWidget(self.buttonAdd)
        self.horizontalLayout.addWidget(self.buttonRemove)
        self.horizontalLayout.addWidget(self.buttonPreview)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)
    # setupUi

    def addVertex(self):
        aRow = self.tableWidget.currentRow()
        if aRow == -1:
            aRow = self.tableWidget.rowCount
        else:
            aRow = aRow + 1
        # if

        self.tableWidget.insertRow(aRow)
        self.tableWidget.setItem(aRow, 0, QTableWidgetItem("0"))
        self.tableWidget.setItem(aRow, 1, QTableWidgetItem("0"))
        self.tableWidget.setItem(aRow, 2, QTableWidgetItem("0"))
        self.tableWidget.setItem(aRow, 3, QTableWidgetItem("0"))
    # addVertex

    def removeVertex(self):
        aRow = self.tableWidget.currentRow()

        if QMessageBox.question(self, "", QT_TRANSLATE_NOOP("Primitive", "Are you to remove the selected vertex?")) == QMessageBox.Yes:
            self.tableWidget.removeRow(aRow)
        # if
    # removeVertex

    def previewLoop(self):

        PipeCad.RemoveAid(self.aidNumber)

        aPointList = list()

        for r in range(self.tableWidget.rowCount):
            aX = float(self.tableWidget.item(r, 0).text())
            aY = float(self.tableWidget.item(r, 1).text())
            aZ = float(self.tableWidget.item(r, 2).text())
            aR = float(self.tableWidget.item(r, 3).text())

            aPoint = Position(aX, aY, aZ)
            aPointList.append(aPoint)
        # for

        PipeCad.AddAidPolygon(aPointList, self.aidNumber)
        PipeCad.UpdateViewer()

    # previewPanel

    def accept(self):

        PipeCad.StartTransaction("Create Extrusion")

        PipeCad.CreateItem("EXTR", self.textName.text)

        aPaneItem = PipeCad.CurrentItem()
        aPaneItem.Height = float(self.textThickness.text)

        PipeCad.CreateItem("LOOP")

        for r in range(self.tableWidget.rowCount):
            aX = float(self.tableWidget.item(r, 0).text())
            aY = float(self.tableWidget.item(r, 1).text())
            aZ = float(self.tableWidget.item(r, 2).text())
            aR = float(self.tableWidget.item(r, 3).text())

            PipeCad.CreateItem("VERT")
            aVertItem = PipeCad.CurrentItem()
            aVertItem.Position = Position(aX, aY, aZ)
            aVertItem.Radius = aR
        # for

        PipeCad.CommitTransaction()

        PipeCad.RemoveAid(self.aidNumber)
        PipeCad.UpdateViewer()

        QDialog.accept(self)
    # accept

    def reject(self):
        PipeCad.RemoveAid(self.aidNumber)
        QDialog.reject(self)
    # reject

# ExtrusionDialog

# Singleton Instance.
aExtrDlg = ExtrusionDialog(PipeCad)

def CreateExtrusion():
    aExtrDlg.show()
# CreateExtrusion


def CreateRevolution():
    QMessageBox.warning(PipeCad, "", QT_TRANSLATE_NOOP("Primitive", "Not implement yet!"))
# CreateRevolution


def ConnectPoint():
    QMessageBox.warning(PipeCad, "", QT_TRANSLATE_NOOP("Primitive", "Not implement yet!"))
# ConnectPoint


class ExplicitDialog(QDialog):
    def __init__(self, theFromItem, theToItem, theParent = None):
        QDialog.__init__(self, theParent)

        self.fromItem = theFromItem
        self.fromTag = PipeCad.NextAidNumber()
        self.toItem = theToItem
        self.toTag = PipeCad.NextAidNumber()

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(self.tr("Explicit P-Point Connection"))

        self.verticalLayout = QVBoxLayout(self)

        # Grid layout.
        self.gridLayout = QGridLayout()

        self.labelPoint1 = QLabel(self.tr("Connect Point"))
        self.comboPoint1 = QComboBox()
        self.comboPoint1.setMinimumWidth(60)
        self.comboPoint1.currentIndexChanged.connect(self.point1Changed)
        self.labelItem1 = QLabel("%s %d of %s" % (self.fromItem.Type, self.fromItem.Sequence + 1, self.fromItem.RefNo))
        self.labelItem1.setMinimumWidth(160)

        for i in range(7):
            aKey = ("P%d" % i)
            aPoint = self.fromItem.linkPoint(aKey)
            if aPoint is not None:
                self.comboPoint1.addItem(aKey, aPoint)
            # if
        # for

        self.gridLayout.addWidget(self.labelPoint1, 0, 0)
        self.gridLayout.addWidget(self.comboPoint1, 0, 1)
        self.gridLayout.addWidget(self.labelItem1, 0, 2)

        self.labelPoint2 = QLabel(self.tr("To Point"))
        self.comboPoint2 = QComboBox()
        self.comboPoint2.currentIndexChanged.connect(self.point2Changed)
        self.labelItem2 = QLabel("%s %d of %s" % (self.toItem.Type, self.toItem.Sequence + 1, self.toItem.RefNo))

        for i in range(7):
            aKey = ("P%d" % i)
            aPoint = self.toItem.linkPoint(aKey)
            if aPoint is not None:
                self.comboPoint2.addItem(aKey, aPoint)
            # if
        # for

        self.gridLayout.addWidget(self.labelPoint2, 1, 0)
        self.gridLayout.addWidget(self.comboPoint2, 1, 1)
        self.gridLayout.addWidget(self.labelItem2, 1, 2)

        self.verticalLayout.addLayout(self.gridLayout)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def point1Changed(self):
        aPoint = self.comboPoint1.currentData
        if aPoint is None:
            return
        # if

        PipeCad.RemoveAid(self.fromTag)
        PipeCad.AddAidAxis(aPoint, self.fromTag)
        PipeCad.UpdateViewer()
    # point1Changed

    def point2Changed(self):
        aPoint = self.comboPoint2.currentData
        if aPoint is None:
            return
        # if

        PipeCad.RemoveAid(self.toTag)
        PipeCad.AddAidAxis(aPoint, self.toTag)
        PipeCad.UpdateViewer()
    # point2Changed

    def reject(self):
        PipeCad.RemoveAid(self.fromTag)
        PipeCad.RemoveAid(self.toTag)
        PipeCad.UpdateViewer()

        QDialog.reject(self)
    # reject

    def accept(self):
        if self.fromItem is None or self.toItem is None:
            return
        # if

        aP1 = self.comboPoint1.currentData
        aP2 = self.comboPoint2.currentData

        if aP1 is None or aP2 is None:
            QMessageBox.warning(self, "", self.tr("Please select P-Point to connect!"))
            return
        # if

        try:
            self.fromItem.Connect(aP1, aP2)
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try

        PipeCad.RemoveAid(self.fromTag)
        PipeCad.RemoveAid(self.toTag)
        PipeCad.UpdateViewer()

        QDialog.accept(self)
    # accept

# ExplicitDialog

def ConnectExplicit():
    aTreeItem = PipeCad.CurrentItem()
    if aTreeItem is None:
        return
    # if

    aTypeSet = {"BOX", "CYLI", "SLCY", "SNOU", "DISH", "CONE", "NOZZ", "PYRA", "CTOR", "RTOR",
                "NBOX", "NCYL", "NSLC", "NSNO", "NDIS", "NCON", "NCTO", "NRTO"}

    aType = aTreeItem.Type
    if aType not in aTypeSet:
        QMessageBox.critical(PipeCad, "", PipeCad.tr("You must be positioned at a Primitive level or below!"))
        return
    # if

    if aType in {"EQUI", "TEXT"}:
        QMessageBox.critical(PipeCad, "", PipeCad.tr("You must be positioned at an Equipment Primitive or below!"))
        return
    # if

    aPickItem = PipeCad.PickItem()
    if aPickItem is None:
        return
    # if

    if aTreeItem == aPickItem:
        QMessageBox.critical(PipeCad, "", PipeCad.tr("Cannot connect item to itself!"))
        return
    # if

    aExplicitDlg = ExplicitDialog(aTreeItem, aPickItem, PipeCad)
    aExplicitDlg.show()

# ConnectExplicit
