# Developing of new utility

## Code development
Each developer can evaluate his own macros library for using inside PipeCAD. In this case all macros have to be placed in dedicated folder inside folder **%PYTHONPATH%**. For example, developer's library will be named **omp** and placed in default library folder of PipeCAD:
![Developer's Library Folder](../../images/development/new_utility/sample_file.png)  

Inside sample.py will write next code of new utility:
```python 
from PythonQt.QtCore import *
from PythonQt.QtGui import *

from pipecad import *

class dlgSample(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(500, 30)
        self.setWindowTitle(self.tr("PipeCAD - Sample Utility"))

        self.verticalLayout = QVBoxLayout(self)
        self.lblText = QLabel("Sample Form Text")
        self.verticalLayout.addWidget(self.lblText)
    # setupUi

# Singleton Instance.
aSample = dlgSample(PipeCad)

def ShowSample():
    aSample.show()
# Show
```

## Calling Utility in PipeCAD
For loading utility there needs to run command for importing utility module into PipeCAD:
```python 
import omp.sample as sm
```
Abbreviation **sm** is used  to simplify next using of this module. After importing module there will be possible to show utility form on screen:
```python 
sm.ShowSample()
```

![Commands in Python console](../../images/development/new_utility/python_console.png)  

In result form will be shown: 

![Sample Utility Window](../../images/development/new_utility/sample_window.png)


