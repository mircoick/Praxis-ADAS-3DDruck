from step_motor import MotorDriver,MotorDriverConf
import random as r


meine_config = MotorDriverConf()



cam = MotorDriver(config=meine_config)
#cam.auto_test()
#cam.self_test()
#cam.step_impulse(5,"motor1")
#cam.step_double_impulse("forward","backward",.25)

coords = []

for _ in range(4):
    coords.append(r.randint(-10, 10))
    
#print(coords)
#cam.bresenham_step(coords[0],coords[1],coords[2],coords[3],1e6)
#cam.start_pos(3,-4,1e6)
#cam.stop_pos(3,-4,1e6)
#cam.bresenham_step(-5,0,-6,-4,1e6)

cam.read_gcode("../data/test.gcode")

cam.stop()