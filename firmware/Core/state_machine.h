/* state_machine.h — supervisory FSM (mirrors software/state_machine.py) */
#ifndef STATE_MACHINE_H
#define STATE_MACHINE_H
#include <stdbool.h>
typedef enum { ST_IDLE, ST_PRECHARGE, ST_STARTUP, ST_BUCK, ST_BOOST, ST_FAULT, ST_SHUTDOWN } ConvState_t;
typedef struct { ConvState_t state; int fault_code; } ConvFSM_t;
void FSM_Init(ConvFSM_t *f);
bool FSM_RequestMode(ConvFSM_t *f, const char *mode);
void FSM_Start(ConvFSM_t *f);
void FSM_PrechargeDone(ConvFSM_t *f);
void FSM_StartupDone(ConvFSM_t *f, const char *mode);
void FSM_Trip(ConvFSM_t *f, int code);
void FSM_Recover(ConvFSM_t *f);
void FSM_Reset(ConvFSM_t *f);
#endif
