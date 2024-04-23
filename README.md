# Zotero Auto-Tagger

Maintaining an organized and well-tagged Zotero library is crucial for efficient research and reference management. 

This Python script automates the process of tagging Zotero items, saving significant time and effort while ensuring consistent and accurate tagging across a collection.

## 🚀 Features
- **Keyword Tagging**: The script scans the title and abstract of each item in the collection and adds user predefined tags that match the keywords provided in the CSV file.
- **Tag Mapping**: If an item already has certain tags, the script can automatically add additional tags based on the tag mappings defined in the CSV file.
- **Phrase-to-Tag Mapping**: The script can assign tags to items based on specific phrases or words found in the title or abstract, as specified in the CSV file.
- **Initial Tags**: You can define a set of initial tags that will be added to every item in the collection.
- **Keep Existing Tags**: The script can either keep or remove the existing tags on the items before applying the new tags.

## 📋 Usage
- Install the required Python packages (pyzotero and tqdm) using pip.
- Replace the placeholders in the #User configurations section of the script with your API key, library ID, collection ID, and other settings.
- Create or modify the CSV file according to the specified format and field names.
- Run the script, and it will start processing the items in the specified collection, applying the tags based on the rules defined in the CSV file.

⚖️ Zotero-Auto-Tagger is licensed under CC BY 4.0
