import cv2
import numpy as np
import time

class UstaSolution:

    def __init__(self, target, map_dict):
        self.target = target
        self.map_dict = map_dict
        #print(self.map_dict)
    

    def step_ai(self, obs, coord, dist, angle, global_angle):
        #obs = cv2.cvtColor(obs, cv2.COLOR_RGB2BGR) 
        velocidad = 0.0        
        angulo = int(global_angle)
        print("angle:", angulo, "\ncoord:", coord, "\n")
        
        if angulo > 0:
            action = np.array([ velocidad, -0.8])

        elif angulo == 90:
            action = np.array([ velocidad, 0.0])

        self.convertirDirACoor( str(self.target) )
        
        #print(self.target) #objetivo
        # print("ángulo: ",angle,"\nCoordenada: ", coord,"\ndistancia: ",dist,"\n")
        # if dist < 0:
        #     print("Mal")
        #     action = np.array([velocidad, angle - 10])
        #     print("linea")
        # elif dist > 0.88:
        #     action = np.array([velocidad, angle + 5])
        # else:
        #     print("Bueno")
        
        return action 
    
    def convertirDirACoor(self, objetivo):
        x = objetivo[:3]
        y = objetivo[3:]
        if x[:2] == "st":
            if int( x[2:] ) >= 1 and int( x[2:] ) <= 5:
                print(x[:2], x[2:])
            else:
                print("Rango de dirección no permitido")
            
        else:
            if int( y[2:] ) >= 1 and int( y[2:] ) <= 5:
                print(y[:2], y[2:])
            else:
                print("Rango de dirección no permitido")
            

#python3 usta_test.py --map-name city_3x3_s1 --mode ai --target st2av4
#python3 usta_test.py --map-name city_5x5_s1 --mode ai --target av2st1 --manual-control
