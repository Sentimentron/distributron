#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>

#include "dst.h"

int dst_parse_service(char *payload, ssize_t *cur, ssize_t payload_sz, DST_SERVICE *s) {
	char *sfqdn, *sport, *sservice;
	int port;
	/* Extract the FQDN field */
	sfqdn = payload;
	while (payload[*cur] != ':' && *cur < payload_sz) {
		(*cur)++;
	}
	payload[*cur] = '\0';
	(*cur)++;
	/* Extract the port string */
	sport = payload + *cur;
	while (payload[*cur] != ':' && *cur < payload_sz) {
		(*cur)++;
	}
	payload[*cur] = '\0';
	/* Finally extract the service */
	sservice = payload + *cur;
	while(payload[*cur] != ',' && *cur < payload_sz) {
		(*cur)++;
	}
	if (payload[*cur] != ',') {
		return -1; /* Bad deliminator */
	}
	payload[*cur] = '\0';

	/* Convert the port into a integer */
	port = strtoul(sport, NULL, 10);
	if (port > 65535 || port <= 0) {
		return -2; /* Bad port */
	}

	/* Check the lengths of the other two strings */
	if (strlen(sfqdn) <= 4) {
		return -3; /* Bad FQDN format */
	}
	if (strlen(sservice) <= 1) {
		return -4; /* Bad service format */
	}

	s->fqdn = sfqdn;
	s->service = sservice;
	s->port = port;
	return 0;
}

static void send_error(int session_fd, const char *str) {
	send(session_fd, str, strlen(str), MSG_NOSIGNAL);
}

int dst_parse_payload_to_specs(
        char *payload_buf, 
        DST_SERVICE *service_buf, 
        ssize_t payload_sz,
        int fd
) {
	ssize_t cur = 0;
	int status, i;
	for (i = 0; i < DST_MAX_SERVICE_SPECS; i++) {
		status = dst_parse_service(payload_buf, &cur, payload_sz, service_buf + i);
		switch(status) {
			case -1: send_error(fd, "ERR_BAD_DELIM"); break;
			case -2: send_error(fd, "ERR_BAD_PORT"); break;
			case -3: send_error(fd, "ERR_BAD_HOST"); break;
			case -4: send_error(fd, "ERR_BAD_SRV"); break;
		}
		if (status) {
			return status;
		}	
	}
	return 0;
}
