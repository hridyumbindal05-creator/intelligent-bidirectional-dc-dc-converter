/* main.c — firmware entry point (logic skeleton; requires STM32 HAL + HRTIM
 * ADC/UART to compile for target. Clearly marked: logic-complete, NOT flashed. */
#include <stdio.h>
#include "../Control/pi.h"
#include "../Protection/protection.h"
#include "../Sensors/sensors.h"
#include "state_machine.h"
#include "../Drivers/pwm_driver.h"
#include "../Communication/telemetry.h"

int main(void) {
    ConvFSM_t fsm; FSM_Init(&fsm);
    PwmPair_t pwm; PWM_Init(&pwm);
    PI_t pi; PI_Init(&pi, 0.001f, 0.5f, 0.02f, 0.98f, 2e-6f);
    FSM_Start(&fsm);
    FSM_PrechargeDone(&fsm);
    FSM_StartupDone(&fsm, "buck");
    /* closed-loop body (runs from ADC EOC interrupt in real firmware) */
    float v48 = 48.0f, v12 = 12.0f, i12 = 5.0f, t = 40.0f;
    FaultCode_t fc = Protection_Check(i12, v48, v12, t, true);
    if (fc != FAULT_NONE) FSM_Trip(&fsm, (int)fc);
    else {
        float d = PI_Update(&pi, 12.0f, v12);
        PWM_SetDuty(&pwm, d);
        PWM_Enable(&pwm, true);
    }
    Telemetry_t te = {v48, v12, i12, t, (int)fsm.state, fsm.fault_code};
    char buf[128]; Telemetry_Pack(buf, sizeof buf, &te);
    return 0;
}
