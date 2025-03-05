from PySide6 import QtCore, QtWidgets, QtGui


class Sticker(QtWidgets.QListWidgetItem):

    width = 37
    height = 13

    topLeftRoundedCorner = 4
    topRightRoundedCorner = 4
    bottomLeftRoundedCorner = 0
    bottomRightRoundedCorner = 0

    textLine1 = ""
    textLine2 = ""
    textLine3 = ""  # New attribute for the third line of text
    fontSize1 = 30  # New attribute for the font size of the first line
    fontSize2 = 20  # New attribute for the font size of the second line
    fontSize3 = 20  # New attribute for the font size of the third line
    qrCodeUrl = ""
    modelPath = ""

    alpha = 180
    beta = 180
    
    hideObstructed = True

    def __init__(self, jsonData={}, parent=None):
        super().__init__(parent)

        if jsonData:
            self.width = jsonData["width"]
            self.height = jsonData["height"]
            self.topLeftRoundedCorner = jsonData["topLeftRoundedCorner"]
            self.topRightRoundedCorner = jsonData["topRightRoundedCorner"]
            self.bottomLeftRoundedCorner = jsonData["bottomLeftRoundedCorner"]
            self.bottomRightRoundedCorner = jsonData["bottomRightRoundedCorner"]
            self.textLine1 = jsonData["textLine1"]
            self.textLine2 = jsonData["textLine2"]
            self.textLine3 = jsonData["textLine3"]  # Initialize the third line of text
            self.fontSize1 = jsonData.get("fontSize1", 30)  # Initialize the font size for the first line
            self.fontSize2 = jsonData.get("fontSize2", 20)  # Initialize the font size for the second line
            self.fontSize3 = jsonData.get("fontSize3", 20)  # Initialize the font size for the third line
            self.qrCodeUrl = jsonData["qrCodeUrl"]
            self.modelPath = jsonData["modelPath"]
            self.alpha = jsonData["alpha"]
            self.beta = jsonData["beta"]
            self.hideObstructed = jsonData["hideObstructed"]

        self.valueChanged()

    @QtCore.Slot()
    def valueChanged(self):

        if self.textLine1 == "":
            self.setText("Sticker")
            return
        
        self.setText(self.textLine1 + " " + self.textLine2 + " " + self.textLine3)  # Update to include the third line

    def getJson(self):
        return {
            "width": self.width,
            "height": self.height,
            "topLeftRoundedCorner": self.topLeftRoundedCorner,
            "topRightRoundedCorner": self.topRightRoundedCorner,
            "bottomLeftRoundedCorner": self.bottomLeftRoundedCorner,
            "bottomRightRoundedCorner": self.bottomRightRoundedCorner,
            "textLine1": self.textLine1,
            "textLine2": self.textLine2,
            "textLine3": self.textLine3,  # Include the third line in the JSON output
            "fontSize1": self.fontSize1,  # Include the font size for the first line in the JSON output
            "fontSize2": self.fontSize2,  # Include the font size for the second line in the JSON output
            "fontSize3": self.fontSize3,  # Include the font size for the third line in the JSON output
            "qrCodeUrl": self.qrCodeUrl,
            "modelPath": self.modelPath,
            "alpha": self.alpha,
            "beta": self.beta,
            "hideObstructed": self.hideObstructed
        }
