import socket
import ipaddress
import re
import logging
from urllib.parse import urlparse, urlunparse

# Regex patterns to catch and mask sensitive variables (PII, tokens, authorization headers)
SENSITIVE_PATTERNS = [
    (re.compile(r'(authorization\s*:\s*bearer\s+)[a-zA-Z0-9_\-\.]+', re.IGNORECASE), r'\1[REDACTED]'),
    (re.compile(r'(api[_-]?key\s*[:=]\s*["\']?)[a-zA-Z0-9_\-\.]+(["\']?)', re.IGNORECASE), r'\1[REDACTED]\2'),
    (re.compile(r'("password"\s*:\s*")[^"]+(")', re.IGNORECASE), r'\1[REDACTED]\2'),
    (re.compile(r'("token"\s*:\s*")[^"]+(")', re.IGNORECASE), r'\1[REDACTED]\2'),
    (re.compile(r'(cookie\s*:\s*)[a-zA-Z0-9_\-\.=\s;]+', re.IGNORECASE), r'\1[REDACTED]'),
]

def mask_sensitive_data(message: str) -> str:
    """
    Mask authorization headers, passwords, cookies, and api keys with [REDACTED] in logs.
    """
    if not isinstance(message, str):
        return message
    for pattern, repl in SENSITIVE_PATTERNS:
        message = pattern.sub(repl, message)
    return message

class PIIMaskingFilter(logging.Filter):
    """
    Logging filter that intercepts log records and redacts sensitive PII or credentials before emission.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        if hasattr(record, "msg") and isinstance(record.msg, str):
            record.msg = mask_sensitive_data(record.msg)
        if hasattr(record, "args") and record.args:
            record.args = tuple(
                mask_sensitive_data(arg) if isinstance(arg, str) else arg
                for arg in record.args
            )
        return True

def sanitize_url(url: str) -> str:
    """
    Sanitize and clean user-provided URL string inputs to prevent schema manipulation.
    Strips fragments and restricts schemes strictly to http or https.
    """
    if not url:
        return ""
    
    url = url.strip()
    parsed = urlparse(url)
    
    scheme = parsed.scheme.lower() if parsed.scheme else "https"
    if scheme not in ("http", "https"):
        raise ValueError("Strict protocol restriction: only HTTP/HTTPS schemes are supported.")

    netloc = parsed.netloc.lower()
    if not netloc:
        raise ValueError("Invalid URL: netloc (domain) cannot be empty.")

    # Reconstruct url, removing anchors/fragments
    sanitized = urlunparse((
        scheme,
        netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        ""  # Force empty fragment/anchor
    ))
    return sanitized

def is_safe_url(url: str) -> bool:
    """
    Validate the URL scheme, resolve the hostname, and check if it points to a private/local IP
    to prevent Server-Side Request Forgery (SSRF).
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False

        hostname = parsed.hostname
        if not hostname:
            return False

        # Resolve hostname to all possible IP addresses
        addr_info = socket.getaddrinfo(hostname, None)
        for item in addr_info:
            ip_str = item[4][0]
            ip = ipaddress.ip_address(ip_str)

            # Reject private, loopback, link-local, multicast, or reserved addresses
            if (ip.is_private or 
                ip.is_loopback or 
                ip.is_link_local or 
                ip.is_multicast or 
                ip.is_reserved):
                return False

        return True
    except Exception:
        return False
