<table>
<tr><td><code>WITHDRAW</code></td><td>length</td><td>hostname:port:service</td></tr>
<tr><td colspan='3'><code>OK</code></td></tr>
</table>

The `WITHDRAW` command is a length-prefixed payload command. The payload consists of:
* The host that the service is running on.
* The port that the service is running on.
* The service name of that service.

It's effect is to remove the service identified by the payload so it no longer appears in [`BROKER`](BROKER).

## Example
In this scenario, there's one service (`testService1`) running on `test-service.yourdomain.com` on port 8888 which is now terminating. Here's how it signals to Distributron that it's no longer available:

1. The implementation for `testService1` calls [`REGISTER`](REGISTER) when it starts up.
1. `host-a.yourdomain.com` sends `WITHDRAW45  test-service.yourdomain.com:8888:testService1` to Distributron.
1. Distributron responds with `OK`.

It's also possible for other services to call `WITHDRAW` on a service that's not responding to their requests.

## Support status
<table>
<tr><td>Versions</td><td>0.1.0+</td></tr>
</table>
