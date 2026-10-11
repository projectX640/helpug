import base64
import hashlib
import hmac
import secrets
import time
from urllib.parse import quote


TOTP_PERIOD = 30
TOTP_DIGITS = 6


def generate_secret():
    return base64.b32encode(secrets.token_bytes(20)).decode().rstrip("=")


def _secret_bytes(secret):
    normalized = str(secret or "").replace(" ", "").upper()
    padding = "=" * (-len(normalized) % 8)
    return base64.b32decode(normalized + padding, casefold=True)


def totp_code(secret, counter):
    digest = hmac.new(
        _secret_bytes(secret),
        int(counter).to_bytes(8, "big"),
        hashlib.sha1,
    ).digest()
    offset = digest[-1] & 0x0F
    binary = int.from_bytes(digest[offset:offset + 4], "big") & 0x7FFFFFFF
    return f"{binary % (10 ** TOTP_DIGITS):0{TOTP_DIGITS}d}"


def verify_totp(secret, code, now=None, last_used_counter=None):
    normalized_code = str(code or "").replace(" ", "")
    if len(normalized_code) != TOTP_DIGITS or not normalized_code.isdigit():
        return None
    current_counter = int((time.time() if now is None else now) // TOTP_PERIOD)
    for counter in range(current_counter - 1, current_counter + 2):
        if last_used_counter is not None and counter <= last_used_counter:
            continue
        if hmac.compare_digest(totp_code(secret, counter), normalized_code):
            return counter
    return None


def otpauth_uri(secret, username, issuer="Rapid Response"):
    label = f"{issuer}:{username}"
    return (
        f"otpauth://totp/{quote(label)}?secret={quote(secret)}"
        f"&issuer={quote(issuer)}&algorithm=SHA1&digits={TOTP_DIGITS}&period={TOTP_PERIOD}"
    )
