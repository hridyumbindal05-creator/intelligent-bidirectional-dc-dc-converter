#include "pi.h"
void PI_Init(PI_t *pi, float kp, float ki, float out_min, float out_max, float dt) {
    pi->kp = kp; pi->ki = ki; pi->out_min = out_min; pi->out_max = out_max;
    pi->dt = dt; pi->integral = 0.0f;
}
void PI_Reset(PI_t *pi) { pi->integral = 0.0f; }
float PI_Update(PI_t *pi, float setpoint, float measurement) {
    float err = setpoint - measurement;
    pi->integral += err * pi->dt;
    float u_unsat = pi->kp * err + pi->ki * pi->integral;
    float u = u_unsat < pi->out_min ? pi->out_min : (u_unsat > pi->out_max ? pi->out_max : u_unsat);
    if (u != u_unsat) {
        float delta = (pi->ki != 0.0f) ? (u - u_unsat) / pi->ki : 0.0f;
        pi->integral += delta;
        u_unsat = pi->kp * err + pi->ki * pi->integral;
        u = u_unsat < pi->out_min ? pi->out_min : (u_unsat > pi->out_max ? pi->out_max : u_unsat);
    }
    return u;
}
