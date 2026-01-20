#!/usr/bin/env python3
"""Test tagging one Zotero item via web API"""

from pyzotero import zotero

# Configuration
api_key = 'YT4k8qlHFee21xao3AnxCsSk'
library_id = '8168494'
library_type = 'user'
tag_to_add = 'Zotero-MCP-Results-2025-10-25-1350'

# Test with one item
test_item_key = 'W44VF3CG'

# Connect to Zotero
zot = zotero.Zotero(library_id, library_type, api_key)

print(f"Testing tag addition on item {test_item_key}...")

# Get the item
item = zot.item(test_item_key)

# Show current tags
current_tags = [tag['tag'] for tag in item['data'].get('tags', [])]
print(f"Current tags: {current_tags}")

# Add the new tag (keeping existing tags)
new_tags = current_tags + [tag_to_add]
item['data']['tags'] = [{'tag': tag} for tag in new_tags]

# Update the item
try:
    zot.update_item(item)
    print(f"✓ Successfully added tag '{tag_to_add}' to item {test_item_key}")

    # Verify
    updated_item = zot.item(test_item_key)
    updated_tags = [tag['tag'] for tag in updated_item['data'].get('tags', [])]
    print(f"Updated tags: {updated_tags}")

except Exception as e:
    print(f"✗ Error updating item: {e}")
