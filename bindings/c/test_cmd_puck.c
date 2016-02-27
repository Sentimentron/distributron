#include "dst.h"

/* The PUCK command is used to check if a server
   is accessible */

int main(int argc, char **argv) {
  if (puck()) return 0;
  return 1;
}
