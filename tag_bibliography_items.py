#!/usr/bin/env python3
"""Add timestamp tag to all items from Indigenous Language bibliography"""

from pyzotero import zotero
from datetime import datetime

# Configuration
api_key = 'YT4k8qlHFee21xao3AnxCsSk'
library_id = '8168494'
library_type = 'user'

# Generate tag with current timestamp
timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
tag_to_add = f'Zotero-MCP-Results-{timestamp}'

# All 23 item keys from Indigenous Language Proficiency Certification bibliography
item_keys = [
    'W44VF3CG',  # 黃美金, 2003
    'W964C6CR',  # 李台元, 2002
    'IQBVNCGF',  # Chao, 2011
    'M4G5W339',  # 何光明, 2017
    'SYCKH89C',  # Council, 2014
    'C4HNHR3F',  # Wikipedia
    'BFSREY55',  # Palalavi
    'FZHSSZ3F',  # Collart, 2023
    'KJXA5IH6',  # Lin, 2017
    'PF8P5WA4',  # Preece, 2025
    'F6AT6DJL',  # Lin, 2025
    '7BYRFYFC',  # Sra, 2016
    'IMXQ2ZM3',  # Li, 2025
    '3TM254SW',  # Dupré, 2018
    'EWSH6ZA8',  # 湯愛玉, 2015
    'FT9D7IB5',  # Apay, 2015
    'AI563GSZ',  # Ting
    '7TPZZNUN',  # 黃美金, 2009
    'H9C56VJS',  # Development of Core Competencies
    'FI4D8N9U',  # Matiu & May, 2011
    'Y3KMLJUH',  # 原住民族語言研究發展中心
    'RK443D6Z',  # Huang et al
    'EZ8STB6A',  # Wu, 2011
]

# Connect to Zotero
zot = zotero.Zotero(library_id, library_type, api_key)

print(f"Adding tag '{tag_to_add}' to {len(item_keys)} items...")
print()

successful = 0
failed = 0
errors = []

for i, item_key in enumerate(item_keys, 1):
    try:
        # Get the item
        item = zot.item(item_key)

        # Get existing tags
        existing_tags = [tag['tag'] for tag in item['data'].get('tags', [])]

        # Add new tag if not already present
        if tag_to_add not in existing_tags:
            new_tags = existing_tags + [tag_to_add]
            item['data']['tags'] = [{'tag': tag} for tag in new_tags]

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
print(f"  Tag used: {tag_to_add}")

if errors:
    print("\nErrors:")
    for item_key, error in errors:
        print(f"  {item_key}: {error}")
