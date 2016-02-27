#include <string.h>
#include "dst_internal.h"

int puck(void) {
  char buf[1024];
  if(dst_trans_fixed_out("PUCK    ", buf) == 0) {
    if (strncmp(buf, "OK", 2) == 0) {
      return 1;
    }
  }
  return 0;
}

int clearall(void) {
  char buf[1024];
  if(dst_trans_fixed_out("CLEARALL", buf) == 0) {
    if (strncmp(buf, "OK", 2) == 0) {
      return 0;
    }
  }
  return -1;
}
