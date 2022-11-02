import numpy as np
def calculate_angle(a,b,c):
    a = np.array(a) # First point.
    b = np.array(b) # Mid point.
    c = np.array(c) # End point
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
    # angle = radians*180.0/np.pi if radians*180.0/np.pi > 0 else 360+radians*180.0/np.pi
    return angle
        
        

def slopee(pos1 , pos2):
    """
    @param pos1: (x,y)
    @param pos2: (x,y)
    """
    if pos2.x == pos1.x:
        return 0
    x = (pos2.y - pos1.y) / (pos2.x - pos1.x)
    return x