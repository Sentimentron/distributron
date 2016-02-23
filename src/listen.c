#include <stdlib.h>
#include <assert.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>


#include "dst.h"

int dst_send_badcmd(int fd) {
	return send(fd, "ERR_BAD_CMD", 12, MSG_NOSIGNAL);
}

int dst_send_badpayload(int fd) {
	return send(fd, "ERR_BAD_PAYLOAD", 15, MSG_NOSIGNAL);
}

int dst_send_badpayloadread(int fd) {
	return send(fd, "ERR_BAD_PAYLOAD_READ", 20, MSG_NOSIGNAL);
}

int dst_send_badpayloadsize(int fd) {
	return send(fd, "ERR_BAD_PAYLOAD_SIZE", 20, MSG_NOSIGNAL);
}

int dst_send_badcmdread(int fd) {
	return send(fd, "ERR_BAD_CMD_READ", 16, MSG_NOSIGNAL);
}

int dst_send_ok(int fd) {
	return send(fd, "OK", 2, MSG_NOSIGNAL);
}

int dst_send_trylater(int fd) {
	return send(fd, "TRY_LATER", 9, MSG_NOSIGNAL);
}

int dst_exec_cmd(DST_COMMAND c, int session_fd) {
	char payload_size_buf[] = {0, 0, 0, 0, 0};
	char payload_buf[DST_PAYLOAD_MAX_LENGTH+1];
	DST_SERVICE service_buf[DST_MAX_SERVICE_SPECS];
	ssize_t r;
	int status;
	unsigned long sz;

	/* Initialise arguments */
	memset(service_buf, 0, DST_MAX_SERVICE_SPECS * sizeof(DST_SERVICE));
	memset(payload_buf, 0, DST_PAYLOAD_MAX_LENGTH + 1);

	/* Receive argument size */
	r = recv(session_fd, payload_size_buf, 4, 0);
	if (r == 4) {
		sz = strtoul(payload_size_buf, NULL, 10);
		if (sz > DST_PAYLOAD_MAX_LENGTH) {
			return dst_send_badpayloadsize(session_fd);
		}
		if (sz == 0) {
			return dst_send_badpayloadsize(session_fd);
		}
	} else {
		return dst_send_badpayloadsize(session_fd);
	}

	/* Receive argument payload */	
	r = recv(session_fd, payload_buf, sz, MSG_WAITALL);
	if (r == sz) {
		/* Successfully read */
	} else if (r == -1) {
		dst_send_badpayloadread(session_fd);
			perror("bad payload read");
		if (errno != EAGAIN && errno != EWOULDBLOCK) {
			perror("bad payload read");
		}
		return -1;
	} else {
		return dst_send_badpayload(session_fd);
	}
	
	switch(c) {
		case DST_REGISTER_COMMAND:
		case DST_WITHDRAW_COMMAND:
			status = dst_parse_payload_to_specs(
				payload_buf,
				service_buf,
				sz, 
				session_fd
			);
			break;
		default:
			status = 0;
	}

	if (status) {
		return status;
	}

	switch(c) {
		case DST_REGISTER_COMMAND:
			dst_update_services_table(service_buf);
			break;
		case DST_WITHDRAW_COMMAND:
			dst_trim_services_table(service_buf);
			break;
		case DST_BROKER_COMMAND:
			return dst_cmd_broker(payload_buf, session_fd);
		case DST_SEARCH_COMMAND:
			return dst_cmd_search(payload_buf, session_fd);
		default:
			break;
	}

	/* Dispatch the right cmd */
	assert(c != DST_UNDEFINED_COMMAND);

	return dst_send_ok(session_fd);
	
}

int dst_start_listening() {
	/* Starts listening on localhost:118118 */

	int err, server_fd;
	struct addrinfo hints, *res = NULL;
	const int reuse_opt = 1;
	struct timeval maxwait;
	memset(&hints, 0, sizeof(hints));

	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_protocol = 0;
	hints.ai_flags = AI_PASSIVE | AI_ADDRCONFIG;

	maxwait.tv_sec = 0;
	maxwait.tv_usec = 5000; /* 5 ms */
	
	err = getaddrinfo("127.0.0.1", "11818", &hints, &res);
	if (err) {
		DST_PERROR("failed to resolve local socket address: %s", gai_strerror(err));
		return err;
	}

	server_fd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
	if (server_fd == -1) {
		DST_PERROR("socket() failure");
		return errno;
	}

	/* Allows us to restart immediately */
	setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, 
 			(char *)&reuse_opt, sizeof(reuse_opt));

	if (bind(server_fd, res->ai_addr, res->ai_addrlen) == -1) {
		DST_PERROR("bind() failure");
		return errno;
	}

	freeaddrinfo(res);

	if (listen(server_fd, 2)) {
		DST_PERROR("listen() error");
		return errno;
	}

	while(1) {
		int session_fd; 
		char cmd_buf[DST_COMMAND_MAX_LENGTH];
		ssize_t r;
		/* Accept the connection */
		session_fd = accept(server_fd, NULL, NULL);
		if (session_fd == -1) {
			if (errno == EINTR) {
				/* Interrupted by system call */
				continue;
			}
			DST_PERROR("accept() error");
		}
		/* Times out if it takes more than 5ms to recv() */
		setsockopt(session_fd, SOL_SOCKET, SO_RCVTIMEO,
				(char *)&maxwait, sizeof(struct timeval));
		
		/* Read the command */
		r = recv(session_fd, cmd_buf, DST_COMMAND_MAX_LENGTH, 0);
		if (r == DST_COMMAND_MAX_LENGTH) {
			/* Determine which command this is */
			DST_COMMAND c = dst_derive_command(cmd_buf);
			if (c == DST_CLEAR_COMMAND) {	
				dst_cmd_clear();
				dst_send_ok(session_fd);
			} else if (c != DST_UNDEFINED_COMMAND) {
				dst_exec_cmd(c, session_fd);
			} else {
				dst_send_badcmd(session_fd);
			}
		} else if (r == -1) {
			dst_send_badcmdread(session_fd);
			if (errno != EAGAIN && errno != EWOULDBLOCK) {
				perror("bad read");
			}
		} else {
			dst_send_badcmd(session_fd);
		}
		close(session_fd);
	}
}

int main() {
	/* temporary method */
	dst_start_listening();
}
