#include <stdio.h>
#include "config.h"
#include "hint.h"
int compute(void);
int main(void){const char *note=HINT_NOTE;(void)note;printf("%d\n", VALUE + compute());return 0;}
