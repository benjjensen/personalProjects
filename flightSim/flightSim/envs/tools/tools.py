import sys
sys.path.append('..')
import numpy as np
import math

def Euler2Quaternion(phi0, theta0, psi0):
    cphi = np.cos(phi0/2.0)
    ctheta = np.cos(theta0/2.0)
    cpsi = np.cos(psi0/2.0)
    sphi = np.sin(phi0/2.0)
    stheta = np.sin(theta0/2.0)
    spsi = np.sin(psi0/2.0)
    quats = np.array([ (cpsi*ctheta*cphi+spsi*stheta*sphi),
                        (cpsi*ctheta*sphi-spsi*stheta*cphi),
                        (cpsi*stheta*cphi+spsi*ctheta*sphi),
                        (spsi*ctheta*cphi-cpsi*stheta*sphi) ])
    return quats

def Quaternion2Euler(e0, e1, e2, e3):
    phi = math.atan2( 2*(e0*e1 + e2*e3), (e0**2 + e3**2 - (e1**2) - (e2**2)))
    if (2*(e0*e2-e1*e3)) > 1:
        theta = math.asin(1)
    elif (2*(e0*e2-e1*e3)) < -1:
        theta = math.asin(-1)
    else:
        theta = math.asin( 2*(e0*e2-e1*e3))
    psi = math.atan2( 2*(e0*e3 + e1*e2), (e0**2 + e1**2 - (e2**2) - (e3**2)))
    return phi, theta, psi

def Euler2Rotation(phi, theta, psi):
    return Quaternion2Rotation(Euler2Quaternion(phi, theta, psi))
    # ctheta = math.cos(theta)
    # cpsi = math.cos(psi)
    # cphi = math.cos(phi)
    # stheta = math.sin(theta)
    # spsi = math.sin(psi)
    # sphi = math.sin(phi)
    # RV_B = np.array([ [ctheta*cpsi, ctheta*spsi, -stheta],
    #                     [(sphi*stheta*cpsi - cphi*spsi), (sphi*stheta*spsi + cphi*cpsi), (sphi*ctheta)],
    #                     [(cphi*stheta*cpsi + sphi*spsi), (cphi*stheta*spsi - sphi*cpsi), (cphi*ctheta)] ])
    # return RV_B

def Quaternion2Rotation(e):
    """Rotation matrix from body frame to inertial frame.
    The transpose of this matrix is from inertial to body."""
    e0 = e.item(0)
    ex = e.item(1)
    ey = e.item(2)
    ez = e.item(3)
    R = np.array([[e0**2+ex**2-ey**2-ez**2, 2*(ex*ey-e0*ez), 2*(ex*ez+e0*ey)],
                  [2*(ex*ey+e0*ez), e0**2-ex**2+ey**2-ez**2, 2*(ey*ez-e0*ex)],
                  [2*(ex*ez-e0*ey), 2*(ey*ez+e0*ex), e0**2-ex**2-ey**2+ez**2]])
    return R