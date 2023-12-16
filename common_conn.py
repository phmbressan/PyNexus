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
    # Priorize IPv4
    for addr_type in (socket.AF_INET, socket.AF_INET6):
        try:
            return socket.getaddrinfo(host, port, addr_type, socket.SOCK_STREAM)[0]

        except Exception:
            pass

    raise AttributeError(f"Error: Unable to resolve host '{host}' to an IP address.")
