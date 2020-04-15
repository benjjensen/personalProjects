import numpy as np
import pyqtgraph as pg 
import pyqtgraph.opengl as gl
import pyqtgraph.Vector as Vector


class spacecraft_animator():

    def __init__(self):
        self.app = pg.QtGui.QApplication([])
        self.window = gl.GLViewWidget() 
        self.window.setWindowTitle('Spacecraft Animator')
        self.window.setGeometry(100, 100, 1000, 1000)
        grid = gl.GLGridItem()
        grid.scale(20, 20, 20)
        self.window.addItem(grid)
        self.window.setCameraPosition(distance = 200)
        self.window.setBackgroundColor('k')
        self.window.show()
        self.window.raise_()
        self.plot_initialized = False

        self.points, self.meshColors = self._get_spacecraft_points()


    def update(self, state):
        spacecraft_position = np.array([ [state.pn], [state.pe], [-state.h] ])
        R = self._Euler2Rotation(state.phi, state.theta, state.psi)
        rotated_points = self._rotate_points(self.points, R)
        translated_points = self._translate_points(rotated_points, spacecraft_position)

        # translated_points = self._translate_points(self.points, spacecraft_position)
        # rotated_points = self._rotate_points(translated_points, R)

        # Convert for rendering to East-North-Up
        R = np.array([ [0,1,0], [1,0,0], [0,0,-1]])
        translated_points = R @ translated_points
        # translated_points = R @ rotated_points

        mesh = self._points_to_mesh(translated_points)

        if not self.plot_initialized:
            self.body = gl.GLMeshItem(vertexes = mesh, 
                                        vertexColors = self.meshColors,
                                        drawEdges = True,
                                        smooth = False,
                                        computeNormals = False)
            self.window.addItem(self.body)
            self.plot_initialized = True

        else:
            self.body.setMeshData(vertexes =  mesh, vertexColors = self.meshColors)

        view_location = Vector(state.pe, state.pn, state.h)
        self.window.opts['center'] = view_location
        self.app.processEvents()

    def _rotate_points(self, points, R):
        "Rotate points by the rotation matrix R"
        rotated_points = R @ points
        return rotated_points

    def _translate_points(self, points, translation):
        "Translate points by the vector translation"
        translated_points = points + np.dot(translation, np.ones([1, points.shape[1]]))
        return translated_points

    def _get_spacecraft_points(self):
        # points = np.array([ [5, 0, -3],
        #                     [4, 0, 0],
        #                     [4, -2, 0],
        #                     [5, -2, 0],
        #                     [5, 2, 0],
        #                     [4, 2, 0],
        #                     [-2, -5, 0],
        #                     [0, -5, 0],
        #                     [0, 5, 0],
        #                     [-2, 5, 0],
        #                     [5, 0, 0],
        #                     [-5, 1, 1],
        #                     [-5, -1, 1],
        #                     [-5, -1, -1],
        #                     [-5, 1, -1],
        #                     [-7, 0, 0]        ]).T

        points = np.array([ [7, 0, 0],  # Pt 1
                            [5, -1, -1],
                            [5, 1, -1],
                            [5, 1, 1],
                            [5, -1, 1],  # Pt 5
                            [-5, 0, 0],
                            [2, -5, 0],
                            [0, -5, 0],
                            [0, 5, 0],
                            [2, 5, 0], # Pt 10
                            [-4, -2, 0],
                            [-5, -2, 0],
                            [-5, 2, 0],
                            [-4, 2, 0],
                            [-4, 0, 0],  # Pt 15
                            [-5, 0, -3]                             
                            ]).T 
        scale = 2
        points = scale * points

        # Define Colors
        red = np.array([1, 0, 0, 1])
        green = np.array([0, 1, 0, 1])
        blue = np.array([0, 0, 1, 1])
        yellow = np.array([1, 1, 0, 1])

        meshColors = np.empty((13, 3, 4), dtype = np.float32)
        meshColors[0] = yellow   # Nose of the plane
        meshColors[1] = yellow
        meshColors[2] = yellow
        meshColors[3] = yellow
        meshColors[4] = blue     # Body of the plane
        meshColors[5] = blue
        meshColors[6] = blue
        meshColors[7] = blue
        meshColors[8] = red      # Front wings
        meshColors[9] = red 
        meshColors[10] = green   # Back wings
        meshColors[11] = green
        meshColors[12] = yellow  # Tail fin

        return points, meshColors

    def _points_to_mesh(self, points):
        points = points.T 
        mesh = np.array([ [points[0], points[2], points[3]],   # Nose of plane
                            [points[0], points[3], points[4]],
                            [points[0], points[4], points[1]],
                            [points[0], points[1], points[2]],
                            [points[2], points[3], points[5]],     # Body of plane
                            [points[1], points[2], points[5]],
                            [points[1], points[4], points[5]],
                            [points[4], points[5], points[3]],
                            [points[6], points[7], points[8]],        # Front wings
                            [points[6], points[9], points[8]],
                            [points[10], points[11], points[12]],     # Back wings
                            [points[10], points[13], points[12]],
                            [points[14], points[5], points[15]]      # Tail fin
                            ])

        return mesh

    def _Euler2Rotation(self, phi, theta, psi):
        # Euler to R_b^i
        c_phi = np.cos(phi)
        s_phi = np.sin(phi)
        c_theta = np.cos(theta)
        s_theta = np.sin(theta)
        c_psi = np.cos(psi)
        s_psi = np.sin(psi)

        R_roll = np.array([ [1, 0, 0],
                            [0, c_phi, s_phi],
                            [0, -s_phi, c_phi]])
        R_pitch = np.array([ [c_theta, 0, -s_theta],
                                [0, 1, 0],
                                [s_theta, 0, c_theta] ])
        R_yaw = np.array([ [c_psi, s_psi, 0],
                            [-s_psi, c_psi, 0],
                            [0, 0, 1] ])

        R = R_roll @ R_pitch @ R_yaw
        return R.T # Body to inertial
