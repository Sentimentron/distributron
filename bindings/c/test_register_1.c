#include "dst.h"

int main(int argc, char **argv) {

  int status;
  clearall();
  status = dst_register("localhost", 8008, "testService1");
  clearall();

  if (status) return 1;

  return 0;

}
