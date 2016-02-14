#include <string.h>

#include "dst.h"

DST_COMMAND dst_derive_command(const char *buf) {

	if (strncmp(buf, "BROKER  ", DST_COMMAND_MAX_LENGTH) == 0) 
		return DST_BROKER_COMMAND;
	if (strncmp(buf, "REGISTER", DST_COMMAND_MAX_LENGTH) == 0)
		return DST_REGISTER_COMMAND;
	if (strncmp(buf, "WITHDRAW", DST_COMMAND_MAX_LENGTH) == 0) 
		return DST_WITHDRAW_COMMAND;
	if (strncmp(buf, "CLEARALL", DST_COMMAND_MAX_LENGTH) == 0)
		return DST_CLEAR_COMMAND;
	return DST_UNDEFINED_COMMAND;

}
