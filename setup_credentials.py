#!/usr/bin/env python3
"""
Setup script to securely store Zotero credentials in macOS Keychain.
Run this once to store your API key and Library ID.
"""

import keyring
import getpass

SERVICE_NAME = "zotero-tag-automation"

print("=" * 60)
print("Zotero Credentials Setup")
print("=" * 60)
print()
print("This script will securely store your Zotero credentials")
print("in the macOS Keychain (encrypted, system-managed).")
print()

# Get Library ID
library_id = input("Enter your Zotero Library ID: ").strip()
if not library_id:
    print("Error: Library ID cannot be empty")
    exit(1)

# Get API Key (hidden input for extra security)
api_key = getpass.getpass("Enter your Zotero API Key: ").strip()
if not api_key:
    print("Error: API Key cannot be empty")
    exit(1)

# Store in Keychain
try:
    keyring.set_password(SERVICE_NAME, "library_id", library_id)
    keyring.set_password(SERVICE_NAME, "api_key", api_key)
    print()
    print("✓ Credentials successfully stored in macOS Keychain!")
    print()
    print(f"  Service: {SERVICE_NAME}")
    print(f"  Library ID: {library_id}")
    print(f"  API Key: {'*' * len(api_key)} (hidden)")
    print()
    print("You can now run the tagging script without entering credentials.")
    print("To view/manage these credentials, open:")
    print("  Keychain Access.app → Search for 'zotero-tag-automation'")
    print()
except Exception as e:
    print(f"✗ Error storing credentials: {e}")
    exit(1)
