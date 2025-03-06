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

    def __init__(self, data=None):
        super().__init__()
        self.setFlags(self.flags() | QtCore.Qt.ItemIsUserCheckable)
        self.setCheckState(QtCore.Qt.Checked)  # Checked by default

        if data:
            self.loadFromJson(data)
        else:
            self.name = "sticker"  # Default name
            self.width = 37
            self.height = 13
            self.topLeftRoundedCorner = 4
            self.topRightRoundedCorner = 4
            self.bottomLeftRoundedCorner = 0
            self.bottomRightRoundedCorner = 0
            self.textLine1 = ""
            self.textLine2 = ""
            self.textLine3 = ""
            self.fontSize1 = 30
            self.fontSize2 = 20
            self.fontSize3 = 20
            self.qrCodeUrl = ""
            self.modelPath = ""
            self.alpha = 180
            self.beta = 180
            self.hideObstructed = True

        self.valueChanged()  # Ensure the display text is set initially

    def loadFromJson(self, data):
        self.name = data.get("name", "sticker")
        self.width = data.get("width", 37)
        self.height = data.get("height", 13)
        self.topLeftRoundedCorner = data.get("topLeftRoundedCorner", 4)
        self.topRightRoundedCorner = data.get("topRightRoundedCorner", 4)
        self.bottomLeftRoundedCorner = data.get("bottomLeftRoundedCorner", 0)
        self.bottomRightRoundedCorner = data.get("bottomRightRoundedCorner", 0)
        self.textLine1 = data.get("textLine1", "")
        self.textLine2 = data.get("textLine2", "")
        self.textLine3 = data.get("textLine3", "")
        self.fontSize1 = data.get("fontSize1", 30)
        self.fontSize2 = data.get("fontSize2", 20)
        self.fontSize3 = data.get("fontSize3", 20)
        self.qrCodeUrl = data.get("qrCodeUrl", "")
        self.modelPath = data.get("modelPath", "")
        self.alpha = data.get("alpha", 180)
        self.beta = data.get("beta", 180)
        self.hideObstructed = data.get("hideObstructed", True)

        self.valueChanged()  # Ensure the display text is updated after loading from JSON

    @QtCore.Slot()
    def valueChanged(self):

        if self.textLine1 == "":
            self.setText("Sticker")
            return
        
        self.setText(self.textLine1 + " " + self.textLine2 + " " + self.textLine3)  # Update to include the third line

    def getJson(self):
        return {
            "name": self.name,
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
