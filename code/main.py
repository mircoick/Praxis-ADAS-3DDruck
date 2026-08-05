from step_motor import MotorDriver,MotorDriverConf
import random as r


meine_config = MotorDriverConf()



cam = MotorDriver(config=meine_config)
#cam.auto_test()
#cam.self_test()
#cam.step_impulse(5,"motor1")


coords = []

for _ in range(4):
    coords.append(r.randint(-10, 10))
    
#print(coords)
cam.bresenham_step(coords[0],coords[1],coords[2],coords[3],.01)
#cam.bresenham_step(-5,0,6,-4,.25)

cam.stop()