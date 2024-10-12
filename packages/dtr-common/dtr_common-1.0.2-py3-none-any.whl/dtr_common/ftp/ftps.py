import ssl
from ftplib import FTP, FTP_TLS
from socket import socket

"""
According to vsftpd documentation
the parameter require_ssl_reuse may break
many FTP client (and break ftplib)
The workaround is to use a subclass of FTP_TLS
"""


class MYFTPS(FTP_TLS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sock = None

    @property
    def sock(self):
        """Return the socket."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """When modifying the socket, ensure that it is ssl wrapped."""
        if value is not None and not isinstance(value, ssl.SSLSocket):
            value = self.context.wrap_socket(value)
        self._sock = value

    def ntransfercmd(self, cmd: str, rest: int | str | None = None) -> tuple[socket, int]:
        conn, size = FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:  # type: ignore[attr-defined]
            conn = self.context.wrap_socket(
                conn,
                server_hostname=self.host,
                session=self.sock.session,
            )
        return conn, size


def generate_tls_context(certpath: str, check_hostname: bool) -> ssl.SSLContext:
    ctx = ssl.SSLContext()
    ctx.options |= ssl.OP_NO_SSLv2
    ctx.options |= ssl.OP_NO_SSLv3
    ctx.check_hostname = check_hostname
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.load_verify_locations(cafile=f"{certpath}/ca-bundle.crt")
    return ctx


def connect_ftps(
    certpath: str, host: str, port: int, user: str, password: str, check_hostname: bool
) -> MYFTPS:
    ssl_ctx = generate_tls_context(certpath, check_hostname)
    ftps = MYFTPS(context=ssl_ctx)
    ftps.connect(host, port)
    ftps.login(user, password)
    ftps.prot_p()
    return ftps
