# C Bindings (error codes)

<table>
<tr>
  <td>-1</td><td>Bad size</td>
  <td>Hostnames / service pairs may be too long.</td>
  <td>Reduce the size of hostname or service names</td>
</tr>
<tr><td>-2</td><td>Bad port number</td>
  <td>Ports must be less than 65536, 0 is reserved.</td>
  <td>Change port values to something inside that range </td></tr>
</table>
