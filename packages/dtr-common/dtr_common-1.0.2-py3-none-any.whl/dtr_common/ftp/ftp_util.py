from __future__ import annotations

import ssl


def generate_tls_context(certpath: str, check_hostname: bool) -> ssl.SSLContext:
    ctx = ssl.SSLContext()
    ctx.options |= ssl.OP_NO_SSLv2
    ctx.options |= ssl.OP_NO_SSLv3
    ctx.check_hostname = check_hostname
    ctx.verify_mode = ssl.CERT_REQUIRED
    try:
      ctx.load_verify_locations(cafile=f"{certpath}/ca-bundle.crt")
    except FileNotFoundError:
       raise FileNotFoundError("FTPS certificate not found")
    return ctx
