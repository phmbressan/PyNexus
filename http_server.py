import sys
import socket
import threading

from pathlib import Path

from common_conn import resolve_host_info


semaphore = threading.Semaphore(8)

def server_routine(socket: socket.socket) -> None:
    """Performs the server routine of accepting a connection, receiving data,
    and echoing it back to the client. Threading is used so that multiple
    clients are accepted.
    The socket is closed after the request is processed.
    """
    try:
        while True:
            connection, address = socket.accept()

            # Monitor thread number
            semaphore.acquire()

            thread = threading.Thread(
                target=handle_client_connection, args=(connection, address)
            )
            thread.start()

    except Exception as e:
        print(f"Server Error: {e}")
    finally:
        print("Closing server socket.")
        socket.close()

def handle_client_connection(connection: socket.socket, address: tuple) -> None:
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

        with connection:
            while True:
                data = connection.recv(1024)
                if not data:
                    break

                response = process_request(data.decode())

                connection.sendall(response.encode())

    except Exception as e:
        print(f"Server Error: {e}")
    finally:
        print("Closing server socket.")
        connection.close()
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
        print(f"Error: Unable to connect to {host}:{port} due to {e}")
        sys.exit(1)


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
        filepath = Path(request_words[1])
        return get_request(filepath)
    else:
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
    try:
        file_ext = filepath.suffix.lstrip(".")

        with open(filepath, "rb") as f:
            content = f.read()

        return f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: text/{file_ext}\r\n\r\n{str(content)}"
    except FileNotFoundError:
        return "HTTP/1.1 404 File Not Found\r\n\r\n"


if __name__ == "__main__":
    if len(sys.argv) > 3:
        print("Usage: python server.py <port> <ip>")
        sys.exit(1)

    port = int(sys.argv[1])
    ip = sys.argv[2]

    server_socket = start_server(ip, port)
    server_routine(server_socket)
