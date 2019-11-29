import cv2
import numpy as np
import time

class UstaSolution:

    def __init__(self, target, map_dict):
        self.target = target
        self.map_dict = map_dict
        self.imprimirLogro = True
        self.origenSetted = False
        self.origen = tuple()
        self.viejaCoord = tuple()  
        self.nuevaCoord = tuple()
        self.viejoSentido = str()
        self.nuevoSentido = str()
        self.colaBusqueda = list()
        self.alineamiento = False

    def step_ai(self, obs, coord, dist, angle, global_angle):                 
        objetivo = self.convertirDirACoor( str(self.target) )
        action = np.array([0.0, 0.0])                
        posActual = coord
        velocidad = 0.8    
        """El punto de origen sólo lo va a tomar una vez el primer fotograma cuando inicie
        el programa. Si el punto de origen se modifica cada fotograma, no podrá alcanzar
        el punto objetivo.
        """
        if not self.origenSetted:            
            self.origen = coord
            self.colaBusqueda = self.BFSSearch(self.origen, objetivo)  
            self.origenSetted = True

        if not posActual == objetivo:  
            self.nuevaCoord = coord
            if len(self.colaBusqueda) != 0:
                action = self.ejecutarBusqueda(self.colaBusqueda[0], angle, global_angle, dist, velocidad) 
            print(self.colaBusqueda)
            print("Coordenada actual: ", posActual, "objetivo", objetivo)
            
            if len(self.viejaCoord) != 0 and len(self.colaBusqueda) != 0:
                if self.viejaCoord != self.nuevaCoord:
                    self.colaBusqueda.pop(0)
                    self.alineamiento = False
        else:
            action = self.acciones(angle, global_angle, dist, velocidad, "det")  
            if self.imprimirLogro:       
                print("\n\nCoordenada actual: ", posActual)         
                print("¡Punto objetivo alcanzado!->", self.target, "Coord: ",objetivo)
                self.imprimirLogro = False
        
        self.viejaCoord = coord        
        return action 
    
    def convertirDirACoor(self, objetivo):
        if objetivo.__len__() == 6:
            x = objetivo[:3]
            y = objetivo[3:]
            coordST = 0
            coordAV = 0
            if x[:2] == "st":
                if int( x[2:] ) >= 1 and int( x[2:] ) <= 5:                
                    coordAV = (int(x[2:]) * 2) - 1
                    coordST = int(y[2:]) * 2

                else:
                    print("Rango de dirección no permitido")
                
            else:
                if int( y[2:] ) >= 1 and int( y[2:] ) <= 5:                
                    coordAV = int(y[2:]) * 2
                    coordST = (int(x[2:]) * 2) - 1

                else:
                    print("Rango de dirección no permitido")
        return coordST, coordAV

    def acciones(self, angle, global_angle, dist, velocidad, accion):
        sensibilidadGiros = 0.3
        #De frente
        if accion == "frente":
            if dist > -0.07 and dist < -0.02:
                if angle > 1:
                    action = np.array([ 0.0,  + 0.5 ])
                elif angle < - 1:
                    action = np.array([ 0.0,  - 0.5 ])
                else:
                    action = np.array([velocidad, 0.0])

            else:                
                if dist < -0.070:
                    action = np.array([ 0.3,  - sensibilidadGiros])

                elif dist > -0.02: 
                    action = np.array([ 0.3,  + sensibilidadGiros ])

        #Izquierda
        elif accion == "izq":
            action = np.array([ 0.0,  + 1 ])

        #Derecha
        elif accion == "der":
            action = np.array([ 0.0,  - 1 ])
        
        #Detenerse
        elif accion == "det":
            action = np.array([ 0.0,  0.0 ])

        return action

    def BFSSearch(self, origen, objetivo):
        cola = list()
        def diferencia(coord1, coord2, dir1, dir2):
            if coord1 < coord2:
                direccion = dir2
                diferencia = coord2 - coord1
                
            else:
                direccion = dir1
                diferencia = coord1 - coord2

            return diferencia, direccion

        if objetivo[0] == origen[0]:
            cantidad, direccion = diferencia(objetivo[1], origen[1],"S","N")
            for num in range(cantidad):
                cola.append(direccion)  

        elif objetivo[1] == origen[1]:
            cantidad, direccion = diferencia(objetivo[0], origen[0],"E","W") 
            for num in range(cantidad):
                cola.append(direccion) 

        else:            
            cantidad, direccion = diferencia(objetivo[1], origen[1],"S","N")
            for num in range(cantidad):
                cola.append(direccion)
            cantidad, direccion = diferencia(objetivo[0], origen[0],"E","W")
            for num in range(cantidad):
                cola.append(direccion)

        return cola

    def orientacion(self, sentido, angle, global_angle, dist, velocidad):  
        senOrientacion = 3 #Sensibilidad de la orientacion
        if sentido == "E":
            ang = 0.0
            if global_angle > ang and global_angle < ang + senOrientacion:
                action = self.acciones(angle, global_angle, dist, velocidad, "det")
                self.alineamiento = True                
            elif global_angle < 180 :
                action = self.acciones(angle, global_angle, dist, velocidad, "der")
            elif global_angle >= 180 :
                action = self.acciones(angle, global_angle, dist, velocidad, "izq")
        
        elif sentido == "N":
            ang = 90.0 #Ángulo objetivo de orientación
            if (global_angle < ang + senOrientacion) and (global_angle > ang - senOrientacion):
                action = self.acciones(angle, global_angle, dist, velocidad, "det")
                self.alineamiento = True
            elif global_angle > ang :
                action = self.acciones(angle, global_angle, dist, velocidad, "der")
            elif global_angle < ang:
                action = self.acciones(angle, global_angle, dist, velocidad, "izq")
        
        elif sentido == "W":
            ang = 180.0 #Ángulo objetivo de orientación
            if (global_angle < ang + senOrientacion) and (global_angle > ang - senOrientacion):
                action = self.acciones(angle, global_angle, dist, velocidad, "det")
                self.alineamiento = True
            elif global_angle > ang :
                action = self.acciones(angle, global_angle, dist, velocidad, "der")
            elif global_angle < ang:
                action = self.acciones(angle, global_angle, dist, velocidad, "izq")

        elif sentido == "S":
            ang = 270.0 #Ángulo objetivo de orientación
            if (global_angle < ang + senOrientacion) and (global_angle > ang - senOrientacion):
                action = self.acciones(angle, global_angle, dist, velocidad, "det")
                self.alineamiento = True
            elif global_angle > ang :
                action = self.acciones(angle, global_angle, dist, velocidad, "der")
            elif global_angle < ang:
                action = self.acciones(angle, global_angle, dist, velocidad, "izq")

        return action, self.alineamiento

    def ejecutarBusqueda(self, colaItem, angle, global_angle, dist, velocidad):
        action, self.alineamiento = self.orientacion(colaItem, angle, global_angle, dist, velocidad)
        if self.alineamiento:            
            action = self.acciones(angle, global_angle, dist, velocidad, "frente")
        
        return action      

#python3 usta_test.py --map-name city_5x5_s1 --mode ai --target st5av2 
#python3 usta_test.py --map-name city_5x5_s1 --mode ai --target av2st1 --manual-control
