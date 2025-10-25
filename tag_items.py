#!/usr/bin/env python3
"""
Reusable script to tag Zotero items with a timestamp tag.
Credentials are retrieved securely from macOS Keychain.

Usage:
    python tag_items.py ITEM_KEY1 ITEM_KEY2 ITEM_KEY3 ...

Example:
    python tag_items.py W44VF3CG M4G5W339 IQBVNCGF
"""

import sys
import keyring
from pyzotero import zotero
from datetime import datetime

SERVICE_NAME = "zotero-tag-automation"

def get_credentials():
    """Retrieve credentials from macOS Keychain"""
    library_id = keyring.get_password(SERVICE_NAME, "library_id")
    api_key = keyring.get_password(SERVICE_NAME, "api_key")

    if not library_id or not api_key:
        print("✗ Error: Credentials not found in Keychain")
        print()
        print("Please run setup_credentials.py first to store your credentials:")
        print("  python setup_credentials.py")
        print()
        sys.exit(1)

    return library_id, api_key

def tag_items(item_keys, tag=None):
    """Tag Zotero items with a timestamp tag"""

    # Get credentials from Keychain
    library_id, api_key = get_credentials()

    # Generate tag if not provided
    if tag is None:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        tag = f'Zotero-MCP-Results-{timestamp}'

    # Connect to Zotero
    zot = zotero.Zotero(library_id, 'user', api_key)

    print(f"Tagging {len(item_keys)} items with: {tag}")
    print()

    successful = 0
    failed = 0
    errors = []

    for i, item_key in enumerate(item_keys, 1):
        try:
            # Get the item
            item = zot.item(item_key)

            # Get existing tags
            existing_tags = [t['tag'] for t in item['data'].get('tags', [])]

            # Add new tag if not already present
            if tag not in existing_tags:
                new_tags = existing_tags + [tag]
                item['data']['tags'] = [{'tag': t} for t in new_tags]

                # Update the item
                zot.update_item(item)
                print(f"[{i}/{len(item_keys)}] ✓ {item_key}")
                successful += 1
            else:
                print(f"[{i}/{len(item_keys)}] ⊙ {item_key} (already tagged)")
                successful += 1

        except Exception as e:
            print(f"[{i}/{len(item_keys)}] ✗ {item_key}: {e}")
            errors.append((item_key, str(e)))
            failed += 1

    print()
    print(f"Summary:")
    print(f"  Successful: {successful}/{len(item_keys)}")
    print(f"  Failed: {failed}/{len(item_keys)}")
    print(f"  Tag: {tag}")

    if errors:
        print()
        print("Errors:")
        for item_key, error in errors:
            print(f"  {item_key}: {error}")
        return False

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tag_items.py ITEM_KEY1 ITEM_KEY2 ...")
        print()
        print("Example:")
        print("  python tag_items.py W44VF3CG M4G5W339 IQBVNCGF")
        print()
        print("Or provide item keys from a file:")
        print("  python tag_items.py $(cat item_keys.txt)")
        sys.exit(1)

    item_keys = sys.argv[1:]
    success = tag_items(item_keys)
    sys.exit(0 if success else 1)
