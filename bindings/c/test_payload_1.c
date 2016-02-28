#include "dst_internal.h"
#include <string.h>

int main(int argc, char **argv) {

  const char *cmd = "REGISTER";
  const char *payload = "localhost:8808:testService,";

  char buf[1024];

  int s = dst_trans_payload(cmd, payload, buf);
  if (s != 0) return 1;

  if (strcmp(buf, "OK")) return 2;

  return 0;

}
