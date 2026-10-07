/* pi.h — discrete PI controller with anti-windup (mirrors software/pi_controller.py) */
#ifndef PI_H
#define PI_H
typedef struct {
    float kp, ki;
    float out_min, out_max;
    float dt;
    float integral;
} PI_t;
void PI_Init(PI_t *pi, float kp, float ki, float out_min, float out_max, float dt);
void PI_Reset(PI_t *pi);
float PI_Update(PI_t *pi, float setpoint, float measurement);
#endif
