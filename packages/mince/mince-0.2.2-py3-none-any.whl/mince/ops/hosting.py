from __future__ import annotations


def find_available_port(
    min_port: int | str = 8052, *, n_attempts: int = 100
) -> int:
    import socket

    port = int(min_port)
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            port += 1
