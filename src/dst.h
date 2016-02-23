#ifndef __H_DST__
#define __H_DST__

#include <stdio.h>
#include <string.h>
#include <sys/types.h>

#define DST_LOG(args, ...) fprintf(stderr, "dst: " args "\n", __VA_ARGS__);
#define DST_PERROR(args, ...) do { \
		fprintf(stderr, "dst: " args "\n", ##__VA_ARGS__); \
		perror("dst: error was"); \
	} while(0)

/* The max/required length for commands */
#define DST_COMMAND_MAX_LENGTH 8
/* The biggest payload we can offer (excluding size, always 4 bytes) */
#define DST_PAYLOAD_MAX_LENGTH 1024
/* The maximum number of FQDN:port:service things we can 
 * put inside a payload */
#define DST_MAX_SERVICE_SPECS 16
/* The maximum number of services we can store
   before reallocating */
#define DST_DEFAULT_TABLE_SIZE 32

typedef enum {
	DST_UNDEFINED_COMMAND,
	DST_BROKER_COMMAND,
	DST_REGISTER_COMMAND,
	DST_WITHDRAW_COMMAND,
	DST_CLEAR_COMMAND,
	DST_SEARCH_COMMAND,
	DST_PUCK_COMMAND, /* heartbeat */
} DST_COMMAND;

typedef struct {
	char *fqdn;
	char *service;
	int port;
	int active;
} DST_SERVICE;

DST_COMMAND dst_derive_command(const char *buf); /* cmd.c */
int dst_parse_payload_to_specs(			 /* parse.c */
	char *payload_buf, 
	DST_SERVICE *service_buf, 
	ssize_t payload_sz,
	int session_fd
);
int dst_update_services_table(DST_SERVICE *service_buf); /* table.c */
int dst_trim_services_table(const DST_SERVICE *service_buf);
int dst_cmd_broker(const char *payload, int session_fd);
int dst_cmd_search(const char *payload, int session_fd);
int dst_cmd_clear(void);

#endif /* __H_DST__ */
