from step_motor import MotorDriver,step_motor_conf

meine_config = step_motor_conf(
    PIN_ENA=18,
    PIN_IN1=22,
    PIN_IN2=23
    )

cam = MotorDriver(config=meine_config)
#cam.auto_test()
cam.self_test()
