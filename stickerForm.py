from PySide6 import QtCore, QtWidgets, QtGui
from PIL import ImageQt
import os

from generator import render3D, convert_angles_to_direction, makeLinesThicker, generateLabel  # Import generateLabel function


class StickerForm(QtWidgets.QWidget):

    sticker = None

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QtWidgets.QGridLayout(self)
        currentLayoutLine = 0

        # Sticker size
        self.layout.addWidget(QtWidgets.QLabel("Size:"), currentLayoutLine, 0)
        self.layout.addWidget(QtWidgets.QLabel("width"), currentLayoutLine, 1)
        self.widthField = QtWidgets.QSpinBox(self, minimum=0, maximum=1000, value=37)
        self.layout.addWidget(self.widthField, currentLayoutLine, 2)
        self.layout.addWidget(QtWidgets.QLabel("mm"), currentLayoutLine, 3)
        self.layout.addWidget(QtWidgets.QLabel("height"), currentLayoutLine, 4)
        self.heightField = QtWidgets.QSpinBox(self, minimum=0, maximum=1000, value=13)
        self.layout.addWidget(self.heightField, currentLayoutLine, 5)
        self.layout.addWidget(QtWidgets.QLabel("mm"), currentLayoutLine, 6)

        currentLayoutLine += 1

        # Rounded corners top
        self.layout.addWidget(QtWidgets.QLabel("Top corner:"), currentLayoutLine, 0)
        self.layout.addWidget(QtWidgets.QLabel("left"), currentLayoutLine, 1)
        self.topLeftRoundedCorner = QtWidgets.QSpinBox(self, minimum=0, maximum=100, value=4)
        self.layout.addWidget(self.topLeftRoundedCorner, currentLayoutLine, 2)
        self.layout.addWidget(QtWidgets.QLabel("mm"), currentLayoutLine, 3)
        self.layout.addWidget(QtWidgets.QLabel("right"), currentLayoutLine, 4)
        self.topRightRoundedCorner = QtWidgets.QSpinBox(self, minimum=0, maximum=100, value=4)
        self.layout.addWidget(self.topRightRoundedCorner, currentLayoutLine, 5)
        self.layout.addWidget(QtWidgets.QLabel("mm"), currentLayoutLine, 6)

        currentLayoutLine += 1

        # Rounded corners bottom
        self.layout.addWidget(QtWidgets.QLabel("Bottom corner:"), currentLayoutLine, 0)
        self.layout.addWidget(QtWidgets.QLabel("left"), currentLayoutLine, 1)
        self.bottomLeftRoundedCorner = QtWidgets.QSpinBox(self, minimum=0, maximum=100, value=0)
        self.layout.addWidget(self.bottomLeftRoundedCorner, currentLayoutLine, 2)
        self.layout.addWidget(QtWidgets.QLabel("mm"), currentLayoutLine, 3)
        self.layout.addWidget(QtWidgets.QLabel("right"), currentLayoutLine, 4)
        self.bottomRightRoundedCorner = QtWidgets.QSpinBox(self, minimum=0, maximum=100, value=0)
        self.layout.addWidget(self.bottomRightRoundedCorner, currentLayoutLine, 5)
        self.layout.addWidget(QtWidgets.QLabel("mm"), currentLayoutLine, 6)

        currentLayoutLine += 1

        # Lines of text
        self.layout.addWidget(QtWidgets.QLabel("Line 1:"), currentLayoutLine, 0)
        self.textLine1 = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.textLine1, currentLayoutLine, 1, 1, -1)

        currentLayoutLine += 1

        self.layout.addWidget(QtWidgets.QLabel("Line 2:"), currentLayoutLine, 0)
        self.textLine2 = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.textLine2, currentLayoutLine, 1, 1, -1)

        currentLayoutLine += 1

        self.layout.addWidget(QtWidgets.QLabel("Line 3:"), currentLayoutLine, 0)
        self.textLine3 = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.textLine3, currentLayoutLine, 1, 1, -1)

        currentLayoutLine += 1

        # Font sizes
        self.layout.addWidget(QtWidgets.QLabel("Font Size 1:"), currentLayoutLine, 0)
        self.fontSize1 = QtWidgets.QSpinBox(self, minimum=1, maximum=100, value=30)
        self.layout.addWidget(self.fontSize1, currentLayoutLine, 1)

        currentLayoutLine += 1

        self.layout.addWidget(QtWidgets.QLabel("Font Size 2:"), currentLayoutLine, 0)
        self.fontSize2 = QtWidgets.QSpinBox(self, minimum=1, maximum=100, value=20)
        self.layout.addWidget(self.fontSize2, currentLayoutLine, 1)

        currentLayoutLine += 1

        self.layout.addWidget(QtWidgets.QLabel("Font Size 3:"), currentLayoutLine, 0)
        self.fontSize3 = QtWidgets.QSpinBox(self, minimum=1, maximum=100, value=20)
        self.layout.addWidget(self.fontSize3, currentLayoutLine, 1)

        currentLayoutLine += 1

        # QR Code URL
        self.layout.addWidget(QtWidgets.QLabel("QR code:"), currentLayoutLine, 0)
        self.qrCodeUrl = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.qrCodeUrl, currentLayoutLine, 1, 1, -1)

        currentLayoutLine += 1

        # 3D model
        self.layout.addWidget(QtWidgets.QLabel("3D model:"), currentLayoutLine, 0)
        self.modelPath = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.modelPath, currentLayoutLine, 1, 1, 5)
        self.modelBrowsButton = QtWidgets.QPushButton(self, text="Browse")
        self.modelBrowsButton.clicked.connect(self.selectModel)
        self.layout.addWidget(self.modelBrowsButton, currentLayoutLine, 6)

        currentLayoutLine += 1

        # 3D view
        self.graphicsView = QtWidgets.QGraphicsView(self)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.layout.addWidget(self.graphicsView, currentLayoutLine, 0, 3, 4)

        # Load PNG image from disk (temporary)
        pixmap = QtGui.QPixmap("/home/karlito/creation/gridfinity/labelGenerator/tmp3D.png")
        self.scene.addPixmap(pixmap)
        self.graphicsView.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

        # 3d view controls
        self.layout.addWidget(QtWidgets.QLabel("Alpha:"), currentLayoutLine, 4)
        self.alphaSlider = QtWidgets.QSlider(self, orientation=QtCore.Qt.Horizontal, minimum=0, maximum=359, value=180)
        self.alphaSlider.valueChanged.connect(self.refresh3DViewQuick)
        self.alphaSlider.sliderReleased.connect(self.refresh3DViewFull)
        self.layout.addWidget(self.alphaSlider, currentLayoutLine, 5, 1, 2)
        
        self.layout.addWidget(QtWidgets.QLabel("Beta:"), currentLayoutLine+1, 4)
        self.betaSlider = QtWidgets.QSlider(self, orientation=QtCore.Qt.Horizontal, minimum=0, maximum=359, value=180)
        self.betaSlider.valueChanged.connect(self.refresh3DViewQuick)
        self.betaSlider.sliderReleased.connect(self.refresh3DViewFull)
        self.layout.addWidget(self.betaSlider, currentLayoutLine+1, 5, 1, 2)

        self.hideObstructedCheckbox = QtWidgets.QCheckBox(self, text="Hide obstructed lines", checked=True)
        self.layout.addWidget(self.hideObstructedCheckbox, currentLayoutLine+2, 4, 1, 3)
        self.hideObstructedCheckbox.stateChanged.connect(self.refresh3DViewFull)

        currentLayoutLine += 3  # Move to the next row after adding 3D view controls

        # Preview section
        self.layout.addWidget(QtWidgets.QLabel("Preview:"), currentLayoutLine, 0)
        self.previewLabel = QtWidgets.QLabel(self)  # QLabel to display the preview image
        self.layout.addWidget(self.previewLabel, currentLayoutLine, 1, 1, 5)
        self.refreshButton = QtWidgets.QPushButton(self, text="Refresh Preview")  # Button to refresh the preview
        self.refreshButton.clicked.connect(self.refreshPreview)  # Connect the button click to the refreshPreview function
        self.layout.addWidget(self.refreshButton, currentLayoutLine, 6)

        currentLayoutLine += 1

    @QtCore.Slot()
    def selectModel(self):
        modelFilePaths = QtWidgets.QFileDialog.getOpenFileName(self, "Select 3D model", "", "3D model (*)")

        if len(modelFilePaths) == 0:
            return
        
        self.modelPath.setText(modelFilePaths[0])

        self.refresh3DViewFull()

    @QtCore.Slot()
    def refresh3DViewQuick(self):

        if not os.path.exists(self.modelPath.text()):
            return
       
        orientation = convert_angles_to_direction(self.alphaSlider.value(), self.betaSlider.value())
        hideObstructed = False

        render3D(self.modelPath.text(), orientation, hideObstructed)    # 0.11s

        img = makeLinesThicker("tmp3D.png") # 0.49s

        self.scene.clear()

        self.imgQ = ImageQt.ImageQt(img)
        pixMap = QtGui.QPixmap.fromImage(self.imgQ)
        self.scene.addPixmap(pixMap)

        self.graphicsView.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

    @QtCore.Slot()
    def refresh3DViewFull(self):

        if not os.path.exists(self.modelPath.text()):
            return

        orientation = convert_angles_to_direction(self.alphaSlider.value(), self.betaSlider.value())
        hideObstructed = self.hideObstructedCheckbox.isChecked()

        render3D(self.modelPath.text(), orientation, hideObstructed)

        img = makeLinesThicker("tmp3D.png")

        self.scene.clear()

        self.imgQ = ImageQt.ImageQt(img)
        pixMap = QtGui.QPixmap.fromImage(self.imgQ)
        self.scene.addPixmap(pixMap)

        self.graphicsView.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

    @QtCore.Slot()
    def refreshPreview(self):
        # Logic to refresh the preview image
        label_data = {
            "width": self.widthField.value(),
            "height": self.heightField.value(),
            "topLeftRoundedCorner": self.topLeftRoundedCorner.value(),
            "topRightRoundedCorner": self.topRightRoundedCorner.value(),
            "bottomLeftRoundedCorner": self.bottomLeftRoundedCorner.value(),
            "bottomRightRoundedCorner": self.bottomRightRoundedCorner.value(),
            "textLine1": self.textLine1.text(),
            "textLine2": self.textLine2.text(),
            "textLine3": self.textLine3.text(),
            "fontSize1": self.fontSize1.value(),
            "fontSize2": self.fontSize2.value(),
            "fontSize3": self.fontSize3.value(),
            "qrCodeUrl": self.qrCodeUrl.text(),
            "modelPath": self.modelPath.text(),  # Add modelPath to the label_data dictionary
            "alpha": self.alphaSlider.value(),  # Add alpha to the label_data dictionary
            "beta": self.betaSlider.value(),  # Add beta to the label_data dictionary
            "hideObstructed": self.hideObstructedCheckbox.isChecked()  # Add hideObstructed to the label_data dictionary
        }

        # Generate the label image
        img = generateLabel(label_data)

        # Convert the image to QPixmap and set it to the preview label
        self.imgQ = ImageQt.ImageQt(img)
        pixMap = QtGui.QPixmap.fromImage(self.imgQ)
        self.previewLabel.setPixmap(pixMap)  # Set the pixmap to the preview label

    def loadData(self, sticker):
        self.sticker = sticker

        if self.sticker is None:
            return

        self.widthField.setValue(self.sticker.width)
        self.heightField.setValue(self.sticker.height)

        self.topLeftRoundedCorner.setValue(self.sticker.topLeftRoundedCorner)
        self.topRightRoundedCorner.setValue(self.sticker.topRightRoundedCorner)
        self.bottomLeftRoundedCorner.setValue(self.sticker.bottomLeftRoundedCorner)
        self.bottomRightRoundedCorner.setValue(self.sticker.bottomRightRoundedCorner)

        self.textLine1.setText(self.sticker.textLine1)
        self.textLine2.setText(self.sticker.textLine2)
        self.textLine3.setText(self.sticker.textLine3)

        self.fontSize1.setValue(self.sticker.fontSize1)  # Load the font size for the first line
        self.fontSize2.setValue(self.sticker.fontSize2)  # Load the font size for the second line
        self.fontSize3.setValue(self.sticker.fontSize3)  # Load the font size for the third line

        self.qrCodeUrl.setText(self.sticker.qrCodeUrl)
        self.modelPath.setText(self.sticker.modelPath)

        self.alphaSlider.setValue(self.sticker.alpha)
        self.betaSlider.setValue(self.sticker.beta)

        self.hideObstructedCheckbox.setChecked(self.sticker.hideObstructed)

        self.graphicsView.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

        self.refresh3DViewFull()


    def saveData(self):

        if self.sticker is None:
            return

        self.sticker.width = self.widthField.value()
        self.sticker.height = self.heightField.value()

        self.sticker.topLeftRoundedCorner = self.topLeftRoundedCorner.value()
        self.sticker.topRightRoundedCorner = self.topRightRoundedCorner.value()
        self.sticker.bottomLeftRoundedCorner = self.bottomLeftRoundedCorner.value()
        self.sticker.bottomRightRoundedCorner = self.bottomRightRoundedCorner.value()

        self.sticker.textLine1 = self.textLine1.text()
        self.sticker.textLine2 = self.textLine2.text()
        self.sticker.textLine3 = self.textLine3.text()

        self.sticker.fontSize1 = self.fontSize1.value()  # Save the font size for the first line
        self.sticker.fontSize2 = self.fontSize2.value()  # Save the font size for the second line
        self.sticker.fontSize3 = self.fontSize3.value()  # Save the font size for the third line

        self.sticker.qrCodeUrl = self.qrCodeUrl.text()
        self.sticker.modelPath = self.modelPath.text()

        self.sticker.alpha = self.alphaSlider.value()
        self.sticker.beta = self.betaSlider.value()

        self.sticker.hideObstructed = self.hideObstructedCheckbox.isChecked()

        self.sticker.valueChanged()
