<table>
<tr><td><code>SEARCH</code></td><td>length</td><td>prefix</td></tr>
<tr><td colspan='3'><code>result_count host:port ... | <null></code></td></tr>
</table>

The `SEARCH` command is a length-prefixed payload command. Its response is a space-separated list of zero or more service names which match the payload.

## Example
In this scenario, there are two services (`testService1` and `testService2`). A requester wants to know all of the `testService` services in the appliation.

1. The implementation for `testService1` and `testService2` call [`REGISTER`](cmd-REGISTER.md) when they start up.
1. `host-a.yourdomain.com` sends `SEARCH11  testService` to Distributron.
1. Distributron responds with `   2 testService1 testService2`.

## Support status
<table>
<tr><td>Versions</td><td>0.1.0+</td></tr>
</table>
