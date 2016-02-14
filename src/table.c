#include "dst.h"

#include <stdlib.h>

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
			return dst_inner_update_services_table(buf, i);
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
