import socket

HOST = '127.0.0.1'  # Localhost (your computer)
PORT = 8080         # Port number (non-privileged, common for local dev)

def start_server():
    # Create a TCP socket using IPv4 and TCP (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to a specific address and port
        server_socket.bind((HOST, PORT))

        # Start listening for incoming connections; backlog of 5 means up to 5 can wait in queue
        server_socket.listen(5)
        print(f"Server is listening on http://{HOST}:{PORT}")

        while True:
            # Accept a new connection (blocking call until a client connects)
            client_conn, client_addr = server_socket.accept()

            # Automatically close connection when done using 'with'
            with client_conn:
                print(f"Connected by {client_addr}")

                # Receive up to 1024 bytes of data from the client
                # This is raw bytes from TCP stream
                raw_request = client_conn.recv(1024)
                # print(f"Raw request data: {raw_request}")


                print(f"Raw request data from {client_addr}")

                if not raw_request:
                    print("Empty request (browser pre-connect or closed early). Skipping.\n")
                    continue
                # 🧠 .decode('utf-8') converts bytes → human-readable string
                # HTTP is text-based (headers, methods, etc.)
                # If you skip decoding, you get raw bytes like b'GET / HTTP/1.1\r\n...'
                request = raw_request.decode('utf-8').strip()
                if not request:
                    print("No request received, skipping connection.")
                    continue

                print("--- HTTP Request Start ---")
                print(request)  # 🕵️ This shows the full HTTP request from the client
                print("--- HTTP Request End ---")

                # Parse request line (e.g., "GET / HTTP/1.1")
                request_line = request.splitlines()[0]
                method, path, version = request_line.split()

                # Basic routing: return different responses based on path
                if path == "/":
                    body = "<b>Hello, world!</b>"
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html\r\n"
                        f"Content-Length: {len(body)}\r\n"
                        "\r\n"
                        f"{body}"
                    )

                else:
                    # If path is unknown, return a 404 response
                    body = "404 Not Found"
                    response = (
                        "HTTP/1.1 404 Not Found\r\n"
                        "Content-Type: text/plain\r\n"
                        f"Content-Length: {len(body)}\r\n"
                        "\r\n"
                        f"{body}"
                    )

                # Send the HTTP response back to the client
                client_conn.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    start_server()
