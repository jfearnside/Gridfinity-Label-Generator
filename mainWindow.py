from PySide6 import QtCore, QtWidgets, QtGui
import json
import sys
import os
import subprocess
import shutil
from generator import generateLabel
from stickerForm import StickerForm
from sticker import Sticker
from generator import generateLabelSheets


class MainWindow(QtWidgets.QMainWindow):

    stickerList = []
    pageWidth = 210
    pageHeight = 297
    currentFileName = ""

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon("resources/icon.svg"))
        self.setWindowTitle("Hardware Label Maker")

        self.mainWidget = QtWidgets.QSplitter(self)
        self.setCentralWidget(self.mainWidget)

        self.menuBar = self.menuBar()
        fileMenu = self.menuBar.addMenu("&File")

        # New File Action
        newAction = QtGui.QAction("&New", self)
        newAction.setShortcut("Ctrl+N")
        newAction.triggered.connect(self.newFile)
        fileMenu.addAction(newAction)

        # Open File Action
        openAction = QtGui.QAction("&Open...", self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)

        # Save File Action
        saveAction = QtGui.QAction("&Save", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.saveFile)
        fileMenu.addAction(saveAction)

        # Save as File Action
        saveAsAction = QtGui.QAction("&Save as...", self)
        saveAsAction.setShortcut("Ctrl+Shift+S")
        saveAsAction.triggered.connect(self.saveAsFile)
        fileMenu.addAction(saveAsAction)

        # Export Action
        exportAction = QtGui.QAction("&Export to PDF", self)
        exportAction.setShortcut("Ctrl+E")
        exportAction.triggered.connect(self.exportFile)
        fileMenu.addAction(exportAction)

        # Export to PNG Action
        exportToPNGAction = QtGui.QAction("Export to &PNG", self)
        saveAsAction.setShortcut("Ctrl+Shift+E")
        exportToPNGAction.triggered.connect(self.exportToPNG)
        fileMenu.addAction(exportToPNGAction)

        # Quit Action
        quitAction = QtGui.QAction("&Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(self.closeApp)
        fileMenu.addAction(quitAction)

        # Left part of the layout
        self.leftWidget = QtWidgets.QWidget(self)
        self.leftWidget.layout = QtWidgets.QVBoxLayout(self.leftWidget)
        self.mainWidget.addWidget(self.leftWidget)

        self.stickerList = QtWidgets.QListWidget(self)
        self.stickerList.currentItemChanged.connect(self.refresh)
        self.leftWidget.layout.addWidget(self.stickerList)

        # Control buttons at the bottom left
        self.bottomButtons = QtWidgets.QWidget(self)
        self.bottomButtons.layout = QtWidgets.QHBoxLayout(self.bottomButtons)
        self.bottomButtons.layout.setContentsMargins(0, 0, 0, 0)

        self.selectAllButton = QtWidgets.QPushButton("Deselect All", self.bottomButtons)  # Set initial text to "Deselect All"
        self.selectAllButton.clicked.connect(self.toggleSelectAll)
        self.bottomButtons.layout.addWidget(self.selectAllButton)

        self.addStickerButton = QtWidgets.QPushButton("Add", self.bottomButtons)
        self.addStickerButton.clicked.connect(self.newSticker)
        self.bottomButtons.layout.addWidget(self.addStickerButton)

        self.deleteStickerButton = QtWidgets.QPushButton("Delete", self.bottomButtons)
        self.deleteStickerButton.clicked.connect(self.deleteSticker)
        self.bottomButtons.layout.addWidget(self.deleteStickerButton)

        self.printButton = QtWidgets.QPushButton("Export to PDF", self.bottomButtons)
        self.printButton.clicked.connect(self.exportFile)
        self.bottomButtons.layout.addWidget(self.printButton)

        self.exportToPNGButton = QtWidgets.QPushButton("Export to PNG", self.bottomButtons)
        self.exportToPNGButton.clicked.connect(self.exportToPNG)
        self.bottomButtons.layout.addWidget(self.exportToPNGButton)

        # Add Sort Button
        self.sortButton = QtWidgets.QPushButton("Sort", self.bottomButtons)
        self.sortButton.clicked.connect(self.sortStickers)
        self.bottomButtons.layout.addWidget(self.sortButton)

        self.leftWidget.layout.addWidget(self.bottomButtons)

        # Right part of the layout
        self.stickerForm = StickerForm(self)
        self.mainWidget.addWidget(self.stickerForm)

        self.mainWidget.setSizes([20, 80])
        self.resize(800, 500)

        self.show()

        self.newSticker()
        self.selectFirstItem()

    @QtCore.Slot()
    def newFile(self):
        self.currentFileName = ""
        self.stickerList.clear()
        self.stickerForm.loadData(None)

    @QtCore.Slot()
    def openFile(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",
                                                  "JSON Files (*.json)", options=options)
        if fileName:
            self.loadFromFile(fileName)
    
    @QtCore.Slot()
    def saveFile(self):
        self.refresh()
        if self.currentFileName == "":
            self.saveAsFile()
        else:
            self.saveToFile(self.currentFileName)

    @QtCore.Slot()
    def saveAsFile(self):
        self.refresh()
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "",
                                                  "JSON Files (*.json)", options=options)
        if fileName:
            self.saveToFile(fileName)

    def loadFromFile(self, fileName):
        self.showBusyIndicator("Loading file...")
        try:
            with open(fileName, 'r') as file:
                self.currentFileName = fileName
                self.stickerList.clear()
                self.stickerForm.loadData(None)

                data = json.load(file)
                self.pageWidth = data["pageWidth"]
                self.pageHeight = data["pageHeight"]
                self.stickerList.clear()
                for stickerData in data["stickerList"]:
                    self.stickerList.addItem(Sticker(stickerData))
                self.selectFirstItem()
                self.stickerForm.refreshPreview()  # Refresh the preview after loading the first item
        finally:
            self.hideBusyIndicator()

    def getData(self):
        self.refresh()

        dataDict = {
            "pageWidth": self.pageWidth,
            "pageHeight": self.pageHeight,
            "stickerList": []
        }

        for i in range(self.stickerList.count()):
            dataDict["stickerList"].append(self.stickerList.item(i).getJson())

        return dataDict

    def saveToFile(self, fileName):
        self.showBusyIndicator("Saving file...")
        try:
            if fileName:
                with open(fileName, 'w') as file:
                    json.dump(self.getData(), file, indent=4)
                    self.currentFileName = fileName
        finally:
            self.hideBusyIndicator()

    @QtCore.Slot()
    def exportFile(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export", "",
                                                  "PDF Files (*.pdf)", options=options)
        if fileName:
            self.showBusyIndicator("Exporting to PDF...")
            try:
                # Filter the stickers based on their check state
                checked_stickers = []
                for i in range(self.stickerList.count()):
                    sticker = self.stickerList.item(i)
                    if sticker.checkState() == QtCore.Qt.Checked:
                        checked_stickers.append(sticker.getJson())

                # Create a data dictionary with only the checked stickers
                dataDict = {
                    "pageWidth": self.pageWidth,
                    "pageHeight": self.pageHeight,
                    "stickerList": checked_stickers
                }

                generateLabelSheets(dataDict, fileName)
                msgBox = QtWidgets.QMessageBox(self)
                msgBox.setWindowTitle("Export Complete")
                msgBox.setText(f"PDF export complete. File saved to: {fileName}")
                openButton = msgBox.addButton("Open PDF", QtWidgets.QMessageBox.ActionRole)
                msgBox.addButton(QtWidgets.QMessageBox.Ok)
                msgBox.exec()

                if msgBox.clickedButton() == openButton:
                    self.openPDF(fileName)
            finally:
                self.hideBusyIndicator()

    def openPDF(self, filePath):
        if sys.platform == "win32":
            os.startfile(filePath)
        elif sys.platform == "darwin":
            subprocess.call(["open", filePath])
        else:
            subprocess.call(["xdg-open", filePath])

    @QtCore.Slot()
    def closeApp(self):
        self.close()

    @QtCore.Slot()
    def newSticker(self):
        self.stickerList.addItem(Sticker())
        self.selectFirstItem()
        self.stickerForm.refreshPreview()  # Refresh the preview after adding a new sticker

    @QtCore.Slot()
    def deleteSticker(self):
        if self.stickerList.currentItem() is not None:
            self.stickerList.takeItem(self.stickerList.currentRow())
        self.selectFirstItem()
        self.stickerForm.refreshPreview()  # Refresh the preview after deleting a sticker

    @QtCore.Slot()
    def refresh(self):
        if self.stickerList.currentItem() is not None:
            self.stickerForm.saveData()
            self.stickerForm.loadData(self.stickerList.currentItem())
            self.stickerForm.refreshPreview()  # Refresh the preview when the current item changes

    def selectFirstItem(self):
        if self.stickerList.count() > 0:
            self.stickerList.setCurrentRow(0)
            self.refresh()

    def exportToPNG(self):
        # Prompt the user to select a folder for the output
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Folder")

        if not folder:
            return

        self.showBusyIndicator("Exporting to PNG...")
        try:
            # Generate and save the PNGs
            for i in range(self.stickerList.count()):
                sticker = self.stickerList.item(i)
                if sticker.checkState() == QtCore.Qt.Checked:
                    label_data = {
                        "width": sticker.width,
                        "height": sticker.height,
                        "topLeftRoundedCorner": sticker.topLeftRoundedCorner,
                        "topRightRoundedCorner": sticker.topRightRoundedCorner,
                        "bottomLeftRoundedCorner": sticker.bottomLeftRoundedCorner,
                        "bottomRightRoundedCorner": sticker.bottomRightRoundedCorner,
                        "textLine1": sticker.textLine1,
                        "textLine2": sticker.textLine2,
                        "textLine3": sticker.textLine3,
                        "fontSize1": sticker.fontSize1,
                        "fontSize2": sticker.fontSize2,
                        "fontSize3": sticker.fontSize3,
                        "qrCodeUrl": sticker.qrCodeUrl,
                        "modelPath": sticker.modelPath,
                        "alpha": sticker.alpha,
                        "beta": sticker.beta,
                        "hideObstructed": sticker.hideObstructed
                    }

                    img = generateLabel(label_data)
                    filename = f"{sticker.textLine1}_{sticker.textLine2}_{sticker.textLine3}.png".replace(" ", "_")
                    img_path = os.path.join(folder, filename)
                    img.save(img_path)

            # Show a message box to indicate success
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Labels exported to PNG successfully.")
            msgBox.setInformativeText("Do you want to open the folder?")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
            ret = msgBox.exec()

            if ret == QtWidgets.QMessageBox.Yes:
                # Open the folder
                os.startfile(folder)
        finally:
            self.hideBusyIndicator()

    def toggleSelectAll(self):
        select_all = self.selectAllButton.text() == "Select All"
        for i in range(self.stickerList.count()):
            item = self.stickerList.item(i)
            item.setCheckState(QtCore.Qt.Checked if select_all else QtCore.Qt.Unchecked)
        self.selectAllButton.setText("Deselect All" if select_all else "Select All")

    @QtCore.Slot()
    def sortStickers(self):
        self.stickerList.sortItems()

    def showBusyIndicator(self, message):
        self.progressDialog = QtWidgets.QProgressDialog(self)
        self.progressDialog.setWindowTitle("Please Wait")
        self.progressDialog.setLabelText(message)
        self.progressDialog.setCancelButton(None)
        self.progressDialog.setRange(0, 0)
        self.progressDialog.setModal(True)
        self.progressDialog.show()

    def hideBusyIndicator(self):
        if hasattr(self, 'progressDialog'):
            self.progressDialog.close()
            del self.progressDialog

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
