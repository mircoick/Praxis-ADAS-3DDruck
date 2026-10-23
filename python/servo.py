import time
import lgpio

SERVO_PIN = 12      
PWM_FREQ = 50     
PULSE_MIN = 500     
PULSE_MAX = 2000     
STEP_ANGLE = 10     
STEP_DELAY = 0.5    

h = lgpio.gpiochip_open(4)
lgpio.gpio_claim_output(h, SERVO_PIN)

print(f"{'Zeit (s)':<10} | {'Winkel (°)':<10} | {'Pulsweite (µs)':<15} | {'Duty Cycle (%)':<15}")
print("-" * 58)

start_time = time.time()

try:
    for angle in range(0, 181, STEP_ANGLE):
        pulse_width = PULSE_MIN + (angle / 180.0) * (PULSE_MAX - PULSE_MIN)
        duty_cycle = (pulse_width / 20000.0) * 100
        
        lgpio.tx_pwm(h, SERVO_PIN, PWM_FREQ, duty_cycle)
        
        elapsed = time.time() - start_time
        print(f"{elapsed:<10.2f} | {angle:<10} | {pulse_width:<15.1f} | {duty_cycle:<15.2f}")
        
        time.sleep(STEP_DELAY)

finally:
    lgpio.tx_pwm(h, SERVO_PIN, 0, 0)
    lgpio.gpio_free(h, SERVO_PIN)
    lgpio.gpiochip_close(h)
    print("-" * 58)
    print("Sweep beendet.")