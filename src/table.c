#include "dst.h"

#include <stdlib.h>
#include <sys/socket.h>

static DST_SERVICE **table = NULL;
static int table_capacity  = 0;


static int dst_find_free_index() {
	/* scans through the table, looks for entries
	   marked inactive, returns the first available */
	int i;
	for (i = 0; i < table_capacity; i++) {
		DST_SERVICE *s = table[i];
		if (s == NULL) return i;
		if (!s->active) return i;
	}
	return table_capacity; /* indicates max size */
}

static void dst_realloc_services_table() {
	int desired_size = table_capacity * 2;
	if (desired_size == 0) {
		desired_size = DST_DEFAULT_TABLE_SIZE;
	}
	table = realloc(table, desired_size * sizeof(void *));
	memset(
		table + table_capacity,
		0, 
		(desired_size - table_capacity) * sizeof(void *)
	);
	table_capacity = desired_size;
	if (!table) {
		DST_PERROR("dst_realloc_services_table: failed");
		exit(1);
	}
}

static int dst_free_table_elem(int i) {
	if (table[i]->fqdn != NULL) free(table[i]->fqdn);
	if (table[i]->service != NULL) free(table[i]->service);
	table[i]->active = 0;
	return 0;
}

static int dst_inner_update_services_table(DST_SERVICE *buf, int start) {
	/* buf is allocated on the stack, we're transferring
	   it to the heap */
	int j;
	for(j = start; j < DST_MAX_SERVICE_SPECS; j++) {

		if (buf[j].port == 0) continue;

		int i = dst_find_free_index();
		if (i == table_capacity) {
			dst_realloc_services_table();
			return dst_inner_update_services_table(buf, 0);
		}

		if (table[i] != NULL) dst_free_table_elem(i);
		else {
			table[i] = malloc(sizeof(DST_SERVICE));
			if (table[i] == NULL) {
				DST_PERROR("bad alloc for service table element");
				exit(1);
			}
		}

		table[i]->fqdn = calloc(strlen(buf[j].fqdn)+1, 1);
		table[i]->service = calloc(strlen(buf[j].service)+1, 1);
		if (table[i]->fqdn == NULL || table[i]->service == NULL) {
			DST_PERROR("bad alloc for service structure");
			exit(1);
		}
		strcpy(table[i]->fqdn, buf[j].fqdn);
		strcpy(table[i]->service, buf[j].service);
		table[i]->active = 1;
		table[i]->port = buf[j].port;
	}
	return 0;
}

int dst_update_services_table(DST_SERVICE *buf) {
	return dst_inner_update_services_table(buf, 0);
}

static DST_SERVICE *dst_search_services_table(int *start, const char *name) {
	int i;
	for (i = *start; i < table_capacity; i++) {
		*start = i+1;
		DST_SERVICE *s = table[i];
		if (s == NULL) break;
		if (!s->active) continue;
		if (strcmp(s->service, name) == 0) return s;
	}
	return NULL;
}

static void dsendr(char *r, int fd) {
	send(fd, r, strlen(r), MSG_NOSIGNAL);
}

int dst_trim_services_table(const DST_SERVICE *service_buf) {
	int i, j;
	for (i = 0, j = 0; i < DST_MAX_SERVICE_SPECS; i++) {
		const DST_SERVICE *s = service_buf + i;
		DST_SERVICE *t;
		if (!s->port) break; /* reached the end of what's defined */
		while (j < table_capacity) {
			t = dst_search_services_table(&j, s->service);
			if (t == NULL) continue;
			if (t->port != s->port) /* same service, different port */
				continue;

			if (!t->active) continue; 

			if (strcmp(t->fqdn, s->fqdn) != 0) continue;

			t->active = 0; /* deactivate the service */
			break;
		}
	}
	return 0;
}

int dst_cmd_broker(const char *payload, int fd) {
	const DST_SERVICE *ret[16], *shuf[16]; /* can return up to 16 services at once */
	char buf[1024], tmp[1024]; /* used for response message */
	int i = 0, j = 0, c = 0;

	memset(shuf, 0, 16 * sizeof(DST_SERVICE*));
	memset(ret, 0, 16 * sizeof(DST_SERVICE*));
	memset(buf, 0, 1024);
	memset(tmp, 0, 1024);
	
	/* look for matching services */
	while (i < table_capacity && c < 16) {
		const DST_SERVICE *s = dst_search_services_table(&i, payload);
		if (s == NULL) {
			break; /* no more services */
		}
		if (!s->active) continue;	
		ret[c++] = s;
	}

	/* pseudo-randomly shuffle the response */
	for (i = 0; i < c; i++) {
		while(1) {
			int n = rand() % c;
			if (shuf[n]) continue;
			shuf[n] = ret[i];
			break;
		}
	}

	/* build the response message */
	i = 3; j = 0;
	strcpy(buf, "OK ");
	while (i < 1024 && j < c) {
		int s = snprintf(
				tmp, 
				1024, 
				"%s:%d:%s,", 
				shuf[j]->fqdn,
				shuf[j]->port,
				shuf[j]->service
			);
		j++;
		memcpy(buf + i, tmp, s);
		i += s;
	}

	/* send the response */
	if (j == 0) {
		dsendr("<null>", fd);
	} else {
		dsendr(buf, fd);
	}

	return 0;
}	

int dst_cmd_clear() {
	/* invalidate everything in the table */
	int i;
	for (i = 0; i < table_capacity; i++) {
		DST_SERVICE *s = table[i];
		if (s == NULL) break;
		s->active = 0;
	}
	return 0;
}

int dst_cmd_search(const char *str, int session_fd) {
	size_t plen = strlen(str); /* size of the payload */
	char buf[8]; /* max response length */
	char pad[1024];
	/* first four bytes of the response contain the 
	   number of matching services */
	int i, j;
	size_t sent = 0;

	int *matches;

	memset(buf, 0, 8);
	memset(pad, 0, 1024);

	/* allocate enough space to hold all possible matches */
	matches = calloc(table_capacity, sizeof(int));
	if (matches == NULL) {
		perror("dst_cmd_search: allocation failed! ");
		return -1;
	}

	/* match any number of services */
	for (i = 0, j = 0; i < table_capacity; i++) {
		DST_SERVICE *s = table[i];
		if (s == NULL) {
			break;	/* end of table */
		}
		if (!s->active) {
			continue; /* deleted */
		}
		if (strncmp(s->service, str, plen) == 0) { /* match */
			matches[j++] = i;
		}
	}
	
	/* Print "OK" to the response */
	sent += send(session_fd, "OK ", 3, MSG_NOSIGNAL | MSG_MORE);

	/* Print the number of matches to the response */
	sprintf(buf, "%04d ", j);
	sent += send(session_fd, buf, 5, MSG_NOSIGNAL | MSG_MORE);

	/* Print them */
	for (i = 0; i < j; i++) {
		DST_SERVICE *s = table[i];
		const char *r = s->service; 
	        size_t st = send(session_fd, r, strlen(r), MSG_NOSIGNAL | MSG_MORE);
		if (st == -1) {
			perror("dst_cmd_search: unable to send");
			return -1;
		}
		sent += send(session_fd, " ", 1, MSG_NOSIGNAL | MSG_MORE);
		sent += st;
	}

	send(session_fd, pad, sent % 1024, MSG_NOSIGNAL);
	
	free(matches);
	return 0;
}
