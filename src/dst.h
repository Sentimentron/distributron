#ifndef __H_DST__
#define __H_DST__

#include <stdio.h>
#include <string.h>

#define DST_LOG(args, ...) fprintf(stderr, "dst: " args "\n", __VA_ARGS__);
#define DST_PERROR(args, ...) do { \
		fprintf(stderr, "dst: " args "\n", ##__VA_ARGS__); \
		perror("dst: error was"); \
	} while(0)

#define DST_COMMAND_MAX_LENGTH 8

typedef enum {
	DST_UNDEFINED_COMMAND,
	DST_BROKER_COMMAND,
	DST_REGISTER_COMMAND,
	DST_WITHDRAW_COMMAND
} DST_COMMAND;

DST_COMMAND dst_derive_command(const char *buf); /* cmd.c */

#endif /* __H_DST__ */
