# level: WARNING
# start_line: 22
# end_line: 22
# start_column: 8
# end_column: 23
import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print(f"Received from {self.client_address[0]}:")
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    # Create the server, binding to localhost on port 9999
    with socketserver.ThreadingTCPServer(
        ("0.0.0.0", 80),
        MyTCPHandler,
    ) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
