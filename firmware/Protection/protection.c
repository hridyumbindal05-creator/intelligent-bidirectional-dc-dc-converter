#include "protection.h"
#include <stddef.h>
FaultCode_t Protection_Check(float i12, float v48, float v12, float tempC, bool sensor_ok) {
    if (!sensor_ok) return FAULT_SENSOR;
    if (i12 > OC_LIMIT_A || i12 < -OC_LIMIT_A) return FAULT_OC;
    if (v48 > OV_48V) return FAULT_OV48;
    if (v12 > OV_12V) return FAULT_OV12;
    if (v48 < UV_48V) return FAULT_UV48;
    if (v12 < UV_12V) return FAULT_UV12;
    if (tempC > OT_C) return FAULT_OT;
    return FAULT_NONE;
}
