#include "telemetry.h"
#include <stdio.h>
size_t Telemetry_Pack(char *buf, size_t cap, const Telemetry_t *t) {
    return (size_t)snprintf(buf, cap,
        "$TEL,%.2f,%.2f,%.2f,%.1f,%d,%d*\r\n",
        t->v48, t->v12, t->i12, t->tempC, t->state, t->fault);
}
