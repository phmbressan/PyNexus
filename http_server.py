"""
A simple HTTP server that accepts GET requests and returns the local file 
requested.
"""

import socket
import sys
import threading
from pathlib import Path

from common_conn import resolve_host_info

semaphore = threading.Semaphore(8)


def server_routine(server_socket: socket.socket) -> None:
    """Performs the server routine of accepting a connection, receiving data,
    and echoing it back to the client. Threading is used so that multiple
    clients are accepted.
    The socket is closed after the request is processed.
    """
    try:
        while True:
            connection, address = server_socket.accept()

            # Monitor thread number
            with semaphore:
                thread = threading.Thread(
                    target=handle_client_connection, args=(connection, address)
                )
                thread.start()

    except Exception as e:
        raise ConnectionError(f"Server Error: {e}") from e
    finally:
        print(f"Closing server socket at {server_socket}.")
        server_socket.close()


def handle_client_connection(server_socket: socket.socket, address: tuple) -> None:
    """Handles a client connection.

    Parameters
    ----------
    connection : socket.socket
        The client connection.
    address : tuple
        The client address.
    """
    try:
        print(f"Connected to {address[0]}:{address[1]}")

        with server_socket:
            while True:
                data = server_socket.recv(4096)
                if not data:
                    break

                response = process_request(data.decode())

                server_socket.sendall(response.encode())

    except Exception as e:
        raise ConnectionError(f"Server Error: {e}") from e
    finally:
        print(f"Closing server socket at {address[0]}:{address[1]}.")
        server_socket.close()
        semaphore.release()


def start_server(host: str = "", port: int = 9_001, n_listen: int = 5) -> socket.socket:
    """Starts a server listening on `host` and `port` and return the socket
    object.

    Parameters
    ----------
    host : str
        The host to listen on.
    port : int
        The port to listen on.
    n_listen : int
        The number of connections to listen for.

    Returns
    -------
    socket.socket
        The socket object representing the server.
    """
    try:
        # Creates and binds the server socket
        family, socktype, proto, _, address = resolve_host_info(host, port)

        server_socket = socket.socket(family, socktype, proto)
        server_socket.bind(address)

        # Listen for incoming connections
        server_socket.listen(n_listen)

        print(f"Listening on port: {port}")

        return server_socket
    except Exception as e:
        raise ConnectionError(f"Error: Unable to connect to {host}:{port}.") from e


def process_request(request: str) -> str:
    """Processes the request and returns the response.

    Parameters
    ----------
    request : str
        The request string.

    Returns
    -------
    response: str
        The response string.
    """
    request_words = request.split()

    if request_words[0] == "GET":
        filepath = Path("./" + request_words[1].strip("./"))
        return get_request(filepath)

    raise NotImplementedError


def get_request(filepath: Path) -> str:
    """Processes a GET request for a file and returns the response.

    Parameters
    ----------
    filepath : Path
        The path to the file.

    Returns
    -------
    response: str
        The response string.
    """
    response_template = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Length: {content_length}\r\n"
        "Content-Type: text/{file_ext}\r\n\r\n{content}"
    )

    try:
        file_ext = filepath.suffix.lstrip(".")

        with open(filepath, "rb") as f:
            content = f.read()
        return response_template.format(
            content_length=len(content), file_ext=file_ext, content=content.decode()
        )
    except FileNotFoundError:
        return "HTTP/1.1 404 File Not Found\r\n\r\n"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python server.py <port> <address>")
        sys.exit(1)

    arg_port, arg_address = int(sys.argv[1]), sys.argv[2]

    server = start_server(arg_address, arg_port)
    server_routine(server)
