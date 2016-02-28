<table>
<tr><td><code>REGISTER</code></td><td>length</td><td>hostname:port:service</td></tr>
<tr><td colspan='3'><code>OK</code></td></tr>
</table>

The `REGISTER` command is a length-prefixed payload command. The payload consists of one or more tuples containing:
* The host that the service is running on.
* The port that the service is running on.
* The service name of that service.

These fields are joined together with the <code>:</code> character. Each entry must end with a `,` character.

Its response is <code>OK</code> if the registration succeeded.

The total size of the payload must be less than 1024 bytes.

Multiple registrations of services are permitted and will be stored as separate entities within Distributron. If your service doesn't support more than one requester accessing it concurrently on the same port, check whether any services are currently registered on that port with [`BROKER`](cmd-BROKER.md) before calling `REGISTER`.

## Example
In this scenario, there's one service (`testService1`) running on the `test-service.yourdomain.com` and it's listening on port 8888.

1. `test-service.yourdomain.com` sends `REGISTER45  test-service.yourdomain.com:8888:testService1` to Distributron.
1. Distributron responds with `OK`.

## Support status
<table>
<tr><td>Versions</td><td>0.1.0+</td></tr>
</table>
