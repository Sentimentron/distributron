#include "dst_internal.h"
#include <stdio.h>
#include <string.h>

int dst_register(const char *hostname,
                 const int port,
                 const char *service) {
  /* Form the payload message */

  char buf[1024], out[1024];
  int ret;

  const int fmt_chars = 5 /* port */ + 2 /* seperators */
    + 1 /* terminator */ + 8 /* command */ + 4; /* length */

  size_t hostsz = strlen(hostname);
  size_t servsz = strlen(service);

  if (hostsz + servsz >= 1024 - fmt_chars) {
    return -1; /* bad size */
  }

  if (!port || port >= 65536)
    return -2; /* bad port size */

  /* Format the payload */
  snprintf(buf, 1024, "%s:%d:%s,", hostname, port, service);

  /* Execute the command */
  ret = dst_trans_payload("REGISTER", buf, out);

  if (ret) return ret; /* send error */

  if (strcmp(out, "OK")) return -3;

  return 0; /* SUCCESS */
}
