#include <assert.h>
#include <string.h>
#include "dst_internal.h"

/* The PUCK command is used to check if a server
   is accessible */

int main(int argc, char **argv) {

  char buf[1024];
  assert(dst_trans_fixed_out("PUCK    ", buf) == 0);
  assert(strncmp(buf, "OK", 2) == 0);

  return 0;
}
