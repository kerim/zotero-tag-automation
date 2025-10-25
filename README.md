# Zotero Tagging for Claude Code

Automatically tag Zotero items with timestamp tags after generating bibliographies. Designed for use with Claude Code and the Zotero MCP skill.

**Security:** All credentials stored securely in macOS Keychain (encrypted, no plain text).

## What This Does

After searching your Zotero library and generating bibliographies using the [Zotero MCP skill](https://github.com/kerim/zotero-mcp-skill), this tool:

1. **Extracts item keys** from bibliography markdown files
2. **Tags all items** with a timestamp tag (`Zotero-MCP-Results-YYYY-MM-DD-HHMM`)
3. **Enables easy retrieval** - search by tag in Zotero to find these exact items later

## Features

- ✓ **Secure credential storage** - macOS Keychain (encrypted, system-managed)
- ✓ **No plain text credentials** - API key never stored in files
- ✓ **Timestamp tags** - track which searches generated which bibliographies
- ✓ **Claude Code integration** - works seamlessly with Zotero MCP skill
- ✓ **Batch processing** - tag multiple items at once
- ✓ **Error handling** - reports success/failure for each item

## Setup (One-Time)

### 1. Get Zotero API Credentials

**Get your Library ID and API Key:**

1. Go to https://www.zotero.org/settings/keys/new
2. Create a new API key:
   - Name: "Zotero Tagging"
   - ✓ **Allow library access**
   - ✓ **Allow write access** (important!)
3. Copy the API key (shown only once)
4. Note your Library ID (shown on the same page)

### 2. Install Dependencies

```bash
cd /Users/niyaro/Documents/Code/zotero-tag-automation
python3 -m venv venv
source venv/bin/activate
pip install pyzotero keyring
```

### 3. Store Credentials in Keychain

```bash
python setup_credentials.py
```

Enter your:
- **Library ID** (e.g., 8168494)
- **API Key** (from step 1)

Credentials are encrypted and stored in macOS Keychain under service: `zotero-tag-automation`

## Usage

### In Claude Code

The skill is activated automatically when you:
- Generate a bibliography using the Zotero MCP skill
- Ask to tag items from a search

Claude will:
1. Extract item keys from the bibliography
2. Run the tagging script
3. Report success/failure

### Manual Usage

**Tag items from a bibliography file:**

```bash
cd /Users/niyaro/Documents/Code/zotero-tag-automation
source venv/bin/activate

# Extract keys and tag items
grep -o 'items/[A-Z0-9]*' bibliography.md | \
  sed 's/items\///' | \
  xargs python tag_items.py
```

**Tag specific items:**

```bash
source venv/bin/activate
python tag_items.py W44VF3CG M4G5W339 IQBVNCGF
```

**Tag from a list file:**

```bash
# Create file with one key per line
cat > keys.txt <<EOF
W44VF3CG
M4G5W339
IQBVNCGF
EOF

# Tag all
python tag_items.py $(cat keys.txt)
```

## Tag Format

Items are tagged with: `Zotero-MCP-Results-YYYY-MM-DD-HHMM`

**Example:** `Zotero-MCP-Results-2025-10-25-1417`

**Benefits:**
- Sortable by date/time
- Clearly indicates source (MCP search results)
- Unique per search session
- Easy to find in Zotero (search by tag)

## Integration with Zotero MCP Skill

This tool is designed to work with the [Zotero MCP skill](https://github.com/kerim/zotero-mcp-skill):

1. **Search** - Use Zotero MCP skill to find papers and generate bibliography
2. **Tag** - Use this tool to tag all items from that bibliography
3. **Retrieve** - Later, search Zotero by tag to find these exact items

**Example workflow:**
```
User: "Find papers on Indigenous language certification and create a bibliography"
  ↓
Zotero MCP Skill generates bibliography with 23 items
  ↓
Claude asks: "Would you like me to tag these 23 items for easy retrieval later?"
  ↓
Zotero Tagging extracts keys and tags all items
  ↓
User can now search Zotero for tag "Zotero-MCP-Results-2025-10-25-1417"
```

## Security

### Credential Storage

- **macOS Keychain** - System-encrypted, OS-managed
- **No plain text** - API key never stored in files or code
- **Service name** - `zotero-tag-automation`
- **Retrievable** - Can view in Keychain Access.app

### Managing Credentials

**View credentials:**
```bash
# Open Keychain Access app
open -a "Keychain Access"
# Search for: zotero-tag-automation
```

**Update credentials:**
```bash
python setup_credentials.py
```

**Delete credentials:**
```bash
security delete-generic-password -s "zotero-tag-automation" -a "api_key"
security delete-generic-password -s "zotero-tag-automation" -a "library_id"
```

## Files

```
zotero-tag-automation/
├── SKILL.md                  # Claude Code skill definition
├── README.md                 # This file
├── setup_credentials.py      # One-time setup script
├── tag_items.py              # Reusable tagging script
├── test_tag_one.py           # Test script (for development)
├── tag_bibliography_items.py # Batch tagging (example)
├── venv/                     # Python virtual environment
└── .gitignore                # Git ignore file
```

## Troubleshooting

### "Credentials not found in Keychain"

**Solution:** Run setup script
```bash
python setup_credentials.py
```

### "403 Forbidden" or write access error

**Problem:** API key lacks write permissions

**Solution:**
1. Create new API key at https://www.zotero.org/settings/keys/new
2. Enable both:
   - ✓ Allow library access
   - ✓ Allow write access
3. Re-run setup with new key

### "404 Not Found" for specific item

**Possible causes:**
- Item key is invalid
- Item was deleted from Zotero
- Wrong Library ID

**Solution:** Verify item exists in Zotero

### Version conflict error

**Problem:** Item was modified elsewhere during tagging

**Solution:** Script will skip and continue with remaining items

## Requirements

- **macOS** - Uses macOS Keychain
- **Python 3.7+** - For pyzotero and keyring
- **Zotero account** - With API key and write access
- **Claude Code** - For skill integration (optional)

## License

MIT License

## Related Projects

- [Zotero MCP Skill](https://github.com/kerim/zotero-mcp-skill) - Search and generate bibliographies
- [Zotero MCP Server](https://github.com/54yyyu/zotero-mcp) - MCP server for Zotero
- [pyzotero](https://github.com/urschrei/pyzotero) - Python client for Zotero API

## Acknowledgments

Inspired by [raphaelstevens/zotero-tag-automation](https://github.com/raphaelstevens/zotero-tag-automation) for demonstrating the web API approach. Our implementation uses a different design focused on macOS Keychain security and Claude Code integration.

## Support

For issues or questions:
- GitHub Issues: [Create an issue](../../issues)
- Zotero MCP Server: https://github.com/54yyyu/zotero-mcp/issues

---

**Made for researchers using Claude Code to search and organize their Zotero libraries.**
