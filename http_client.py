import sys
import socket

from common_conn import resolve_host_info


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
        family, socktype, proto, _, address = resolve_host_info(host, port)

        client_socket = socket.socket(family, socktype, proto)
        client_socket.connect(address)

    except Exception as e:
        raise ConnectionError(f"Error: Unable to connect to {address}") from e

    print(f"Connected to {address}")

    return client_socket


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

    conn = connect_to_server(webhost, port)
    send_and_receive_lines(conn)
