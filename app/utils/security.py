import hmac

def safe_str_cmp(a, b):
    """
    Constant-time string comparison for strings. Use this function to compare
    strings in cryptographic contexts.
    """
    if not isinstance(a, bytes):
        a = a.encode('utf-8')
    if not isinstance(b, bytes):
        b = b.encode('utf-8')
    return hmac.compare_digest(a, b)
