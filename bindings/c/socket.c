#include <assert.h>
#include <unistd.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>

/* Execute a transaction agaist a Distributron server */
int dst_trans_fixed_out(const char *in, char *out) {
  const int port = 11818;
  int sockfd, n, ret = -1;
  struct hostent *server;
  struct sockaddr_in serv_addr;

  /* Connect to the destination socket */
  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  server = gethostbyname("localhost");
  if (server == NULL) {
    perror("host resolution error");
    return -1;
  }

  memset(&serv_addr, 0, sizeof(serv_addr));
  serv_addr.sin_family = AF_INET;
  memcpy(server->h_addr, &(serv_addr.sin_addr.s_addr), server->h_length);
  serv_addr.sin_port = htons(11818);

  if (connect(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) {
    perror("ERROR connecting");
    return -1;
  }

  /* Send the message */
  n = write(sockfd, in, strlen(in)+1);
  if (n < 0) {
    perror("ERROR sending");
    goto close_skt;
  }


  /* Receive the message */
  n = read(sockfd, out, 1023);
  if (n < 0) {
    perror("read error");
    goto close_skt;
  }
  ret = 0;
close_skt:
  close(sockfd);
  return ret;
}


