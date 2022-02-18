import numpy as np
import math

def IK3dof(l1, l2, l3, phi, ex, ey):
    phi = np.deg2rad(phi)
    # Equations for Inverse kinematics
    wx = ex - l3*np.cos(phi)
    wy = ey - l3*np.sin(phi)

    delta = wx**2 + wy**2
    c2 = (delta - l1**2 - l2**2)/(2*l1*l2)
    s2 = np.sqrt(1-(c2**2))  # elbow down
    theta_2 = np.arctan2(s2, c2)
    s1 = ((l1+l2*c2)*wy - l2*s2*wx)/delta
    c1 = ((l1+l2*c2)*wx + l2*s2*wy)/delta
    theta_1 = np.arctan2(s1, c1)
    theta_3 = phi-theta_1-theta_2

    theta_1 = np.rad2deg(theta_1)
    theta_2 = np.rad2deg(theta_2)
    theta_3 = np.rad2deg(theta_3)

    return theta_1, theta_2, theta_3


# Length of links in cm
l1 = 5.2
l2 = 6.9
l3 = 6.8

# Desired Position of End effector
ex = -14
ey = 3

phi = 120

print(IK3dof(l1,l2,l3,phi,ex,ey))
