Distributron implements a small number of commands for service management. 
This page describes their format and links to more information about them.

## Request syntax
Each request consists of a command which is *right-padded to 8 characters*.

Some commands take a variable-length argument (called the payload). The payload length comes after the command and is *right-padded to 4 characters*. The payload then immediately follows. It is not necessary to null-terminate the payload. The total size of the command, its payload and the length of its payload must be less than 1024 bytes.

## List of valid commands
* [`BROKER`](cmd-BROKER.md) allows clients to lookup hostname/port number information about a service.
* [`CLEARALL`](cmd-CLEARALL.md) removes all information from the directory.
* [`PUCK`](cmd-PUCK.md) checks whether the registry is active.
* [`REGISTER`](cmd-REGISTER.md) allows services to register themselves.
* [`SEARCH`](cmd-SEARCH.md) allows services to find other possibly-matching services.
* [`WITHDRAW`](cmd-WITHDRAW.md) removes information from the directory.

## Support status
<table>
<tr><td>Versions</td><td>0.1.0+</td></tr>
</table>
