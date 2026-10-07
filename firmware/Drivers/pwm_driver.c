#include "pwm_driver.h"
void PWM_Init(PwmPair_t *p) { p->duty = 0.0f; p->enabled = false; p->deadtime_ns = 200; }
void PWM_SetDuty(PwmPair_t *p, float duty) {
    if (duty < 0.02f) duty = 0.02f;
    if (duty > 0.98f) duty = 0.98f;
    p->duty = duty;   /* HRTIM complementary channels get (1-duty) with 200 ns deadtime */
}
void PWM_Enable(PwmPair_t *p, bool en) { p->enabled = en; }
