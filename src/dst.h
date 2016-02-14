#ifndef __H_DST__
#define __H_DST__

#include <stdio.h>
#include <string.h>

#define DST_LOG(args, ...) fprintf(stderr, "dst: " args "\n", __VA_ARGS__);
#define DST_PERROR(args, ...) do { \
		fprintf(stderr, "dst: " args "\n", ##__VA_ARGS__); \
		perror("dst: error was"); \
	} while(0)

#endif /* __H_DST__ */
