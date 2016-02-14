#include <errno.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>


#include "dst.h"

int dst_send_badcmd(int fd) {
	return send(fd, "ERR_BAD_CMD", 12, MSG_NOSIGNAL);
}

int dst_send_trylater(int fd) {
	return send(fd, "TRY_LATER", 9, MSG_NOSIGNAL);
}

int dst_start_listening() {
	/* Starts listening on localhost:118118 */

	int err, server_fd;
	struct addrinfo hints, *res = NULL;
	memset(&hints, 0, sizeof(hints));

	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_protocol = 0;
	hints.ai_flags = AI_PASSIVE | AI_ADDRCONFIG;
	
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
		
		/* Read the command */
		r = recv(session_fd, cmd_buf, DST_COMMAND_MAX_LENGTH, MSG_DONTWAIT);
		if (r == DST_COMMAND_MAX_LENGTH) {
			/* Determine which command this is */
			DST_COMMAND c = dst_derive_command(cmd_buf);
			switch(c) {
				default:
					dst_send_badcmd(session_fd);
			}
		} else if (r == -1) {
			if (errno == EAGAIN || errno == EWOULDBLOCK) {
				dst_send_badcmd(session_fd);
			} else {
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
