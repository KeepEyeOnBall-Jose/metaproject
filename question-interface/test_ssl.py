#!/usr/bin/env python3
"""
SSL Certificate Validation Script

This script validates that SSL certificates are properly configured
for HTTPS development.

Usage:
    python test_ssl.py
"""

import ssl
import os
import sys


def test_ssl_certificates():
    """Test SSL certificate configuration."""

    cert_file = "cert.pem"
    key_file = "key.pem"

    print("🔐 Testing SSL certificate configuration...")

    # Check if SSL files exist
    if not os.path.exists(cert_file):
        print(f"❌ Certificate file not found: {cert_file}")
        return False

    if not os.path.exists(key_file):
        print(f"❌ Key file not found: {key_file}")
        return False

    print("✅ SSL certificate files found")

    # Test SSL context creation
    try:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(cert_file, key_file)
        print("✅ SSL context created successfully")
        print("✅ Certificates are valid for HTTPS development")
        return True
    except ssl.SSLError as e:
        print(f"❌ SSL certificate error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error validating certificates: {e}")
        return False


if __name__ == "__main__":
    success = test_ssl_certificates()
    sys.exit(0 if success else 1)
