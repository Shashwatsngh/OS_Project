# main.py
#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from ui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53,53,53))
    palette.setColor(QPalette.WindowText, QColor(255,255,255))
    palette.setColor(QPalette.Base, QColor(35,35,35))
    palette.setColor(QPalette.AlternateBase, QColor(53,53,53))
    palette.setColor(QPalette.ToolTipBase, QColor(255,255,255))
    palette.setColor(QPalette.ToolTipText, QColor(255,255,255))
    palette.setColor(QPalette.Text, QColor(255,255,255))
    palette.setColor(QPalette.Button, QColor(53,53,53))
    palette.setColor(QPalette.ButtonText, QColor(255,255,255))
    palette.setColor(QPalette.BrightText, QColor(255,0,0))
    palette.setColor(QPalette.Highlight, QColor(142,45,197))
    palette.setColor(QPalette.HighlightedText, QColor(255,255,255))
    app.setPalette(palette)

    win = MainWindow()
    win.resize(900, 600)
    win.show()
    sys.exit(app.exec_())

