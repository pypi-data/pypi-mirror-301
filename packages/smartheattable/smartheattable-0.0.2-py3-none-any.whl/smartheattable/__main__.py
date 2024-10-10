from smartheattable.application import MainWindow

print(f"executing {__file__}")
from smartheattable.application import *

app = QApplication(sys.argv)
app.setApplicationName('Hancse Smart Scratch')
window = MainWindow()
window.setWindowTitle(app.applicationName())
window.show()
app.exec()