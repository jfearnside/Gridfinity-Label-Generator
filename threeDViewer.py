from PyQt5 import QtWidgets, QtCore
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class ThreeDViewer(QtWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = None
        self.alpha = 0
        self.beta = 0
        self.lastPos = QtCore.QPoint()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glClearColor(1.0, 1.0, 1.0, 1.0)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, width / height, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(self.alpha, 1.0, 0.0, 0.0)
        glRotatef(self.beta, 0.0, 1.0, 0.0)
        self.drawModel()

    def drawModel(self):
        if self.model is not None:
            glBegin(GL_TRIANGLES)
            for face in self.model['faces']:
                for vertex in face:
                    glVertex3fv(self.model['vertices'][vertex])
            glEnd()

    def loadModel(self, model):
        self.model = model
        self.update()

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.alpha += dy
            self.beta += dx
        elif event.buttons() & QtCore.Qt.RightButton:
            self.alpha += dy
            self.beta += dx

        self.lastPos = event.pos()
        self.update()