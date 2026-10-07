/* sensors.h — ADC/sensor conversion (mirrors software/sensors.py).
 * Dividender values must stay synchronized with hardware/BOM and docs. */
#ifndef SENSORS_H
#define SENSORS_H
#define ADC_MAX 4095.0f
#define VREF 3.3f
#define DIV_HIGH 10.0f      /* 48 V bus divider */
#define DIV_LOW  4.4255f    /* 12 V bus divider */
#define SHUNT_GAIN 20.0f    /* INA240 gain */
#define SHUNT_OHM 0.001f
#define NTC_BETA 3950.0f
#define NTC_NOM 100000.0f
#define R_SERIES 10000.0f
float Sensor_BusVoltage(unsigned short raw, float divider);
float Sensor_Current(unsigned short raw, unsigned short offset_raw);
float Sensor_TempC(unsigned short raw);
#endif
