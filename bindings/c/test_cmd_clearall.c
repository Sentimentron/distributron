#include "dst.h"

/* The CLEARALL command removes all records from
   Distributron.*/

int main(int argc, char **argv) {
  if(clearall() < 0) return 1;
  return 0;
}
