/* firmware/Tests — host-side test notes.
 * No C compiler is installed in this environment, so firmware logic is
 * verified via the mirrored Python modules (software/*.py) and tests/
 * pytest suite. On a development machine, compile with:
 *   gcc -o fw_test firmware/Core/*.c firmware/Control/*.c \
 *       firmware/Sensors/*.c firmware/Protection/*.c \
 *       firmware/Drivers/*.c firmware/Communication/*.c -lm
 */
