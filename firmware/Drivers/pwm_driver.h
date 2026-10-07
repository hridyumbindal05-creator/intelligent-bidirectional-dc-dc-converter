/* pwm_driver.h — complementary PWM + dead-time (hardware-abstraction level).
 * On STM32G4 this maps to TIM1 HRTIM outputs; here it documents intent. */
#ifndef PWM_DRIVER_H
#define PWM_DRIVER_H
#include <stdbool.h>
typedef struct {
    float duty;          /* 0..1 */
    bool enabled;
    unsigned int deadtime_ns;
} PwmPair_t;
void PWM_Init(PwmPair_t *p);                 /* default 200 ns deadtime */
void PWM_SetDuty(PwmPair_t *p, float duty);  /* clamps 0.02..0.98 */
void PWM_Enable(PwmPair_t *p, bool en);
#endif
