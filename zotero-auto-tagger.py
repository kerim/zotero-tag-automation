import csv
from pyzotero import zotero, zotero_errors
from tqdm import tqdm
import time
import os

# User configurations
api_key = 'YOUR_API_KEY'  # Replace with your Zotero API key, which can be obtained from https://www.zotero.org/settings/keys.
library_id = 'YOUR_LIBRARY_ID'  # Replace with your Zotero library ID, which can be obtained from https://www.zotero.org/settings/keys/new.
library_type = 'user'  # Replace with 'group' if the library type is a group library, otherwise leave it as 'user'.
collection_id = 'YOUR_COLLECTION_ID'  # Replace with the ID of the collection you want to process. You can find the collection ID using the Zutilo plugin for Zotero.
csv_file_name = 'zotero-database-mappings.csv'  # Replace with the name of your CSV file containing tag mappings
csv_delimiter = ';'  # Replace with the delimiter character used in your CSV file
csv_fieldnames = ['type', 'value', 'mapped_tag1', 'mapped_tag2', 'mapped_tag3']  # Field names used in the CSV file
error_log_file_name = 'error_log.txt'  # Replace with the desired name for the error log file
initial_tags = ['INITIAL_TAG']  # Replace with your desired initial 'tag1', 'tag2' (or leave it as an empty list [])
keep_existing_tags = True  # Set to True if you want to keep existing tags, False to remove them

# Connect to your Zotero library
zot = zotero.Zotero(library_id, library_type, api_key)

# Load keywords, tag mappings, and phrase-to-tag mappings from CSV file
keywords = []
tag_mappings = {}
phrase_to_tags_mapping = {}

with open(csv_file_name, 'r') as csv_file:
    reader = csv.DictReader(csv_file, delimiter=csv_delimiter, fieldnames=csv_fieldnames)
    for row in reader:
        mapping_type = row['type']
        value = row['value']
        mapped_tags = []
        for column, tag in row.items():
            if column.startswith('mapped_tag') and tag and tag != value:
                mapped_tags.append(tag)

        if mapping_type == 'keyword':
            keywords.append(value)
        elif mapping_type == 'tag_mapping':
            tag_mappings[value] = mapped_tags
        elif mapping_type == 'phrase_to_tag':
            phrase_to_tags_mapping[value] = mapped_tags

# Get items from the specified collection
collection_items = zot.everything(zot.collection_items(collection_id))
total_items = len(collection_items)

# Initialize the progress bar
progress_bar = tqdm(total=total_items, unit='item', ascii=False, colour='green', leave=True, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} | eta {remaining} | {rate_fmt}', ncols=80)

# Flag to track if any errors occurred
errors_occurred = False

# List to store error messages
error_messages = []

# Start time for elapsed time calculation
start_time = time.time()

# Iterate through the collection items
for i, item in enumerate(collection_items, start=1):
    # Check metadata against keywords
    metadata = ' '.join([item['data'].get('title', ''), item['data'].get('abstractNote', '')])
    new_tags = initial_tags.copy()  # Initialize with the user-provided initial tags

    # Add existing tags if keep_existing_tags is True
    if keep_existing_tags:
        existing_tags = [tag['tag'] for tag in item['data'].get('tags', [])]
        new_tags.extend(existing_tags)

    # Add matching keywords as tags
    for keyword in keywords:
        if keyword.lower() in metadata.lower():
            new_tags.append(keyword)

    # Add additional tags based on tag mappings
    for tag in set(new_tags):
        additional_tags = tag_mappings.get(tag, [])
        new_tags.extend(additional_tags)

    # Assign tags based on phrases
    for phrase, mapped_tags in phrase_to_tags_mapping.items():
        if phrase.lower() in metadata.lower():
            new_tags.extend(mapped_tags)

    # Update tags for the item
    try:
        item = zot.item(item['key'])  # Get the latest version of the item
        item['data']['tags'] = [{'tag': tag} for tag in set(new_tags)]
        zot.update_item(item)
    except zotero_errors.PreConditionFailed:
        error_message = f"Version conflict for item {item['key']}, skipping..."
        error_messages.append(error_message)
        progress_bar.write(error_message)
        errors_occurred = True
        continue

    # Update the progress bar
    progress_bar.update(1)

# Close the progress bar
progress_bar.close()

# Calculate elapsed time
elapsed_time = time.time() - start_time

# Create a log file if any errors occurred
if errors_occurred:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(script_dir, error_log_file_name)
    with open(log_file_path, 'w') as log_file:
        log_file.write("Task completed with the following errors:\n\n")
        for error_message in error_messages:
            log_file.write(error_message + '\n')
    print(f"Task completed with some errors in {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}.")
    print(f"Error logs have been written to '{log_file_path}'.")
else:
    elapsed_seconds = int(elapsed_time)
    hours, remainder = divmod(elapsed_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Task completed successfully in {hours} hour(s), {minutes} minute(s), {seconds} seconds.")
    print("Congrats! Your meticulous tagging has laid the groundwork to craft masterpieces!")