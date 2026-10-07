#include "state_machine.h"
#include <string.h>
void FSM_Init(ConvFSM_t *f) { f->state = ST_IDLE; f->fault_code = 0; }
bool FSM_RequestMode(ConvFSM_t *f, const char *mode) {
    if (f->state == ST_FAULT) return false;
    bool buck = (strcmp(mode, "buck") == 0);
    bool boost = (strcmp(mode, "boost") == 0);
    if (strcmp(mode, "idle") == 0) { f->state = ST_IDLE; return true; }
    if ((f->state == ST_IDLE || f->state == ST_STARTUP) && (buck || boost)) {
        f->state = buck ? ST_BUCK : ST_BOOST; return true;
    }
    if (f->state == ST_BUCK && buck) return true;
    if (f->state == ST_BOOST && boost) return true;
    return false; /* cross-direction change requires ST_IDLE first */
}
void FSM_Start(ConvFSM_t *f) { if (f->state == ST_IDLE) f->state = ST_PRECHARGE; }
void FSM_PrechargeDone(ConvFSM_t *f) { if (f->state == ST_PRECHARGE) f->state = ST_STARTUP; }
void FSM_StartupDone(ConvFSM_t *f, const char *mode) { if (f->state == ST_STARTUP) FSM_RequestMode(f, mode); }
void FSM_Trip(ConvFSM_t *f, int code) { f->fault_code = code; f->state = ST_FAULT; }
void FSM_Recover(ConvFSM_t *f) { if (f->state == ST_FAULT) f->state = ST_SHUTDOWN; }
void FSM_Reset(ConvFSM_t *f) { f->state = ST_IDLE; f->fault_code = 0; }
