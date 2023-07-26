from robot import Robot
from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def read_root():
    return({"welcome":"hola, saludos a todos, bendiciones"})

@app.get("/excecRobot")
def execRobot():
    produc = False
    if produc:
        robot = Robot(produccion = True)
    else:
        robot = Robot(produccion = False)

    robot.getDatos()
    robot.processDatos()
    return ({"finalizacion":"termino exitosamente"})
