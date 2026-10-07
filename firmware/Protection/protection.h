/* protection.h — protection thresholds (mirrors software/protection.py).
 * Thresholds are DESIGN targets until hardware is measured. */
#ifndef PROTECTION_H
#define PROTECTION_H
#include <stdbool.h>
#define OC_LIMIT_A 90.0f
#define OV_48V 62.0f
#define OV_12V 14.5f
#define UV_48V 32.0f
#define UV_12V 9.5f
#define OT_C 85.0f
typedef enum {
    FAULT_NONE = 0, FAULT_OC, FAULT_OV48, FAULT_OV12, FAULT_UV48,
    FAULT_UV12, FAULT_OT, FAULT_SENSOR, FAULT_SHUTDOWN
} FaultCode_t;
FaultCode_t Protection_Check(float i12, float v48, float v12, float tempC, bool sensor_ok);
#endif
