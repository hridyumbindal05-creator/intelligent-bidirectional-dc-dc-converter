/* telemetry.h — packs sensor values into a UART/USB frame (mock-transportable) */
#ifndef TELEMETRY_H
#define TELEMETRY_H
#include <stddef.h>
typedef struct {
    float v48, v12, i12, tempC;
    int state, fault;
} Telemetry_t;
size_t Telemetry_Pack(char *buf, size_t cap, const Telemetry_t *t);
#endif
