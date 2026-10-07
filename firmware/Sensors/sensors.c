#include "sensors.h"
#include <math.h>
static float adc_volts(unsigned short raw) { return ((float)raw / ADC_MAX) * VREF; }
float Sensor_BusVoltage(unsigned short raw, float divider) { return adc_volts(raw) * divider; }
float Sensor_Current(unsigned short raw, unsigned short offset_raw) {
    float v = adc_volts(raw > offset_raw ? raw - offset_raw : offset_raw - raw);
    if (raw < offset_raw) v = -v;
    return v / (SHUNT_GAIN * SHUNT_OHM);
}
float Sensor_TempC(unsigned short raw) {
    float v = adc_volts(raw);
    if (v <= 0.01f || v >= VREF - 0.01f) return -273.0f; /* rail fault */
    float r = R_SERIES * v / (VREF - v);
    float inv_t = (1.0f / 298.15f) + (1.0f / NTC_BETA) * logf(r / NTC_NOM);
    return (1.0f / inv_t) - 273.15f;
}
