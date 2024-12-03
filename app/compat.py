"""Compatibility module for handling deprecated Werkzeug functions"""
import hmac

def safe_str_cmp(a, b):
    """
    Replacement for Werkzeug's removed safe_str_cmp function.
    This is a timing-attack safe comparison function.
    """
    return hmac.compare_digest(str(a).encode('utf-8'), str(b).encode('utf-8'))
