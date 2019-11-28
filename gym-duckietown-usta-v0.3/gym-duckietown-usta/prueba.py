import random

origen =  random.randint(1,9),random.randint(1,9)
objetivo =  random.randint(1,9),random.randint(1,9)
# origen =  1,5
# objetivo = 1,7
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

print(origen, objetivo,"\n", cola)

