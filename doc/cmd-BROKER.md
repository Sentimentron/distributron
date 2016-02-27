<table>
<tr><td><code>BROKER</code></td><td>length</td><td>service</td></tr>
<tr><td colspan='3'><code>result_count host:port ... | <null></code></td></tr>
</table>

The `BROKER` command is a length-prefixed payload command. Its response is a space-seperated list of zero or more `hostname:port` pairs. The payload is the full name of service you want to query.

## Example
In this scenario, there's one service (`testService1`) running on `host-b.yourdomain.com` on port 8888 which a requester running on `host-a.yourdomain.com` wants to discover. Here's how it happens:

1. The implementation for `testService1` calls [`REGISTER`](cmd-REGISTER.md) when it starts up.
1. `host-a.yourdomain.com` sends `BROKER  12  testService1` to Distributron.
1. Distributron responds with `    1 host-b.yourdomain.com:8888`.

## Support status
<table>
<tr><td>Versions</td><td>0.1.0+</td></tr>
</table>
