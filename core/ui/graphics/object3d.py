import json
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
from OpenGL.arrays import vbo
from core.logic.models import load_model


class Object3D:
    def __init__(self, path):
        self.vertices, self.triangles, self.keypoints_indexes, _, _ = load_model(path)
        self.rotation = [0.0, 0.0, 0.0]
        self.position = [0.0, 0.0, -10.0]
        self.quadObj = glu.gluNewQuadric()
        glu.gluQuadricDrawStyle(self.quadObj, glu.GLU_FILL)

    def draw(self, color = (1.0, 1.0, 1.0)):
        gl.glEnable(gl.GL_DEPTH_TEST)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()

        gl.glTranslate(self.position[0], self.position[1], self.position[2])
        gl.glRotate(self.rotation[0], 1.0, 0.0, 0.0)
        gl.glRotate(self.rotation[1], 0.0, 1.0, 0.0)
        gl.glRotate(180.0 + self.rotation[2], 0.0, 0.0, 1.0)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        # gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glEnableClientState(gl.GL_NORMAL_ARRAY)

        gl.glColor3f(*color)

        vertVBO = vbo.VBO(np.reshape(self.vertices, (1, -1)).astype(np.float32))
        vertVBO.bind()

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, vertVBO)
        # gl.glColorPointer(3, gl.GL_FLOAT, 0, vertVBO)
        gl.glNormalPointer(gl.GL_FLOAT, 0, vertVBO)

        triangles = np.reshape(self.triangles, (-1)).astype(np.float32)
        gl.glDrawElements(gl.GL_TRIANGLES, len(triangles), gl.GL_UNSIGNED_INT, triangles)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        # gl.glDisableClientState(gl.GL_COLOR_ARRAY)
        gl.glDisableClientState(gl.GL_NORMAL_ARRAY)

        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()

    def draw_sphere(self, pos, radius=0.1, color = (1.0, 0.0, 0.0)):
        gl.glPushMatrix()
        gl.glTranslate(pos[0], pos[1], pos[2])
        gl.glColor3f(*color)
        glu.gluSphere(self.quadObj, radius, 16, 16)
        gl.glPopMatrix()

    def draw_keypoints(self, keys, color = (1.0, 0.0, 0.0)):
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()

        gl.glTranslate(self.position[0], self.position[1], self.position[2])
        gl.glRotate(self.rotation[0], 1.0, 0.0, 0.0)
        gl.glRotate(self.rotation[1], 0.0, 1.0, 0.0)
        gl.glRotate(180.0 + self.rotation[2], 0.0, 0.0, 1.0)

        if keys:
            coords = self.vertices[[self.keypoints_indexes[key] for key in keys]]
            for pt in coords:
                self.draw_sphere((pt[0], pt[1], pt[2]), radius=0.075, color=color)

        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glPopMatrix()