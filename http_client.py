import sys
import socket


def resolve_host(host: str) -> str:
    """Resolves the host to an IPV4 address. If the host is already an IP
    address, it is returned as is.

    Parameters
    ----------
    host : str
        The host to resolve.

    Returns
    -------
    str
        The IP address of the host.
    """
    try:
        # Attempt to convert host to IP address if it's a domain name
        ip = socket.gethostbyname(host)
        return ip
    except socket.gaierror:
        print(f"Error: Unable to resolve host '{host}' to an IP address.")
        sys.exit(1)


def connect_to_server(host: str, port: int) -> socket.socket:
    """Connects to the server at `host` and `port` and returns the socket
    object.

    Parameters
    ----------
    host : str
        The host to connect to.
    port : int
        The port to connect to.

    Returns
    -------
    socket.socket
        The socket object representing the client.
    """
    try:
        # Creates and binds the client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        print(f"Connected to {host}:{port}")

        return client_socket

    except ConnectionError as e:
        print(f"Error: Unable to connect to {host}:{port}")
        sys.exit(1)


def send_and_receive_lines(socket: socket.socket) -> None:
    """Sends and receives lines of text to and from the server.

    Parameters
    ----------
    socket : socket.socket
        The socket object representing the client.
    """
    try:
        data = read_request()
        socket.sendall(data.encode())
        print(f"Received from server: {socket.recv(1024).decode()}")

    except Exception as e:
        print(f"Connection ran into unexpected error: {e}")
    finally:
        conn.close()
        print("\nClosing connection to server.")


def read_request() -> str:
    """Reads a multiple line request from the user and returns it.
    The request is terminated by a blank line.

    Returns
    -------
    str
        The input formatted according to HTTP request.
    """
    lines = []

    print("Enter request: ")
    while True:
        line = input()

        if line == "":
            lines.append("\r\n\r\n")
            break

        lines.append(line + "\r\n")

    return "".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python http_client.py <port> <webhost>")
        sys.exit(1)

    port, webhost = int(sys.argv[1]), sys.argv[2]

    ip = resolve_host(webhost)
    conn = connect_to_server(ip, port)
    send_and_receive_lines(conn)
