import sys
import socket

from pathlib import Path


def server_routine(socket: socket.socket) -> None:
    """Performs the server routine of accepting a connection, receiving data,
    and echoing it back to the client. The socket is closed after the data is
    sent.
    """
    try:
        connection, address = socket.accept()

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
        socket.close()


def start_server(host: str = "", port: int = 9_001, n_listen: int = 5) -> socket.socket:
    """Starts a server listening on `host` and `port` and return the socket
    object.

    Parameters
    ----------
    host : str
        The host to listen on.
    port : int
        The port to listen on.

    Returns
    -------
    socket.socket
        The socket object representing the server.
    """
    try:
        # Creates and binds the server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))

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
