#ifndef __H_DST__
#define __H_DST__

/* dst_puck: check if Distributron is accessible.
  Returns 1 if it is, 0 otherwise.*/
int dst_puck(void);
/* dst_clearall: clear all Distributron records.
  Returns 0 on success, -1 otherwise. */
int dst_clearall(void);

int dst_register(const char *, int port, const char *);

#endif
