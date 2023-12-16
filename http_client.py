"""
A simple HTTP client that sends a request to a server and receives a response.
"""

import socket
import sys

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

    print(f"Connected to {address} at {port}.")

    return client_socket


def send_and_receive_lines(client_socket: socket.socket) -> None:
    """Sends and receives lines of text to and from the server.

    Parameters
    ----------
    socket : socket.socket
        The socket object representing the client.
    """
    try:
        data = read_request()
        client_socket.sendall(data.encode())

        received = b""
        while True:
            block = client_socket.recv(4096)
            received += block
            if len(block) < 4096:
                break

        print(f"Received {len(received)} bytes from server: {received.decode()}")

    except Exception as e:
        raise ConnectionError("Connection ran into unexpected error.") from e
    finally:
        print("\nClosing connection to server.")
        client_socket.close()


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

    arg_port, arg_address = int(sys.argv[1]), sys.argv[2]

    client = connect_to_server(arg_address, arg_port)
    send_and_receive_lines(client)
