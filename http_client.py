import sys
import socket


def resolve_host_info(host: str, port: int) -> tuple:
    """Resolves the host and port to the appropriate connection info,
    prioritizing IPv6. Returns the connection info as a tuple to create
    a socket.

    Parameters
    ----------
    host : str
        The host to resolve.
    port : int
        The port to connect to.

    Returns
    -------
    tuple
        The connection info as a tuple with the following format:
        `(family, type, proto, canonname, sockaddr)`
    """
    # Priorize IPv6
    for addr_type in (socket.AF_INET6, socket.AF_INET):
        try:
            return socket.getaddrinfo(host, port, addr_type, socket.SOCK_STREAM)[0]

        except Exception:
            pass

    raise AttributeError(f"Error: Unable to resolve host '{host}' to an IP address.")


def connect_to_server(connection_info: tuple) -> socket.socket:
    """Receives the connection info and creates a socket to connect to the
    server. Returns the socket object representing the client.

    Parameters
    ----------
    connection_info : tuple
        The connection info as a tuple with the following format:
        `(family, type, proto, canonname, sockaddr)`

    Returns
    -------
    socket.socket
        The socket object representing the client.
    """
    try:
        family, socktype, proto, _, address = connection_info

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

    info = resolve_host_info(webhost, port)
    conn = connect_to_server(info)
    send_and_receive_lines(conn)
