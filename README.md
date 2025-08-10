# urlPatternParser

A Python codebase for converting unformatted URL filtering rules (like those from EasyList) into Manifest V3 compatible declarativeNetRequest API rules.

## Overview

The `urlPatternParser` helps browser extension developers migrate from Manifest V2 to V3 by transforming traditional ad-blocking into the new declarativeNetRequest format required by Chrome's Manifest V3.

## Features

- ✅ Parses EasyList and similar filter list formats
- ✅ Converts to Manifest V3 declarativeNetRequest rules
- ✅ Handles various rule types and patterns
- ✅ Ensures generated rules are compatible with Chrome's manifest v3 requirements

## Supported Rule Types
Your input should be a text file (.txt) containing rules, The parser supports various rule formats including:

### Basic URL Patterns
- **Basic URL patterns**: `||example.com^`
- **Wildcard patterns**: `/ads/*`
- **Exception rules**: `@@||allowlist.com^`
- **Path-based rules**: `example.com/ads/`

### Resource Type Modifiers
- **Script blocking**: `||ads.com^$script`
- **Image blocking**: `||banners.com^$image`
- **Stylesheet blocking**: `||styles.com^$stylesheet`
- **Multiple types**: `||ads.com^$script,image,stylesheet`
- **Type exceptions**: `||example.com^$~script`

### Domain-Specific Rules
- **Single domain**: `||ads.com^$domain=example.com`
- **Multiple domains**: `||ads.com^$domain=site1.com|site2.org`
- **Domain exceptions**: `||ads.com^$domain=~facebook.com|example.com`

### Combined Modifiers
- **Complex rules**: `||ads.com^$script,image,domain=example.com|test.org,third-party`
- **Mixed exceptions**: `||tracker.com^$~script,~image,domain=~facebook.com`

The parser only supports blocking and allowing rules.

## Output Format
The parser generates rules compatible with Chrome's declarativeNetRequest, the generated rule will be stored in the specified output folder in a JSON format:

```json
[
  {
    "id": 1,
    "priority": 1,
    "action": {
      "type": "block"
    },
    "condition": {
      "urlFilter": "||example.com^",
      "resourceTypes": ["main_frame", "sub_frame"]
    }
  }
]
```

# Usage

## Prerequisites
- Python 3.7 or higher
- No external dependencies required

## Quick Start

1. **Clone or download the repository**:
   ```bash
   git clone https://github.com/dev-emm4/urlPatternParser.git
   cd urlPatternParser/src
   ```

2. **Run the parser**:
   ```bash
   python run.py --inputPath "input.txt" --outputFolderPath "folder" --maxLength 30000
   ```

### Arguments

- `inputPath` - Path to your input text file (required, string)
- `outputFolderPath` - Path to the folder where manifest.json v3 rule will be stored (required, string)
- `maxLength` - Maximum number of rules to be generated (optional, integer)

## Using as a Python Library

You can also import and use the parser directly in your Python code:

```python
from parser import Parser

# Convert
parser = Parser()
result = parser.convert("txt file location", "processed json folder location", 30000)
```

## Getting Help

```bash
python run.py --help
```

This will display all available options and usage information.

## Disclaimer

Invalid URL rules will be automatically dropped during parsing. This includes:

1. **Invalid URL filters**: Empty filters and filters starting with "||*"
2. **Invalid regex filters**: Malformed regular expressions
3. **Duplicate domain options**: Multiple "domain=" declarations in the same rule
4. **Duplicate domain type definitions**: e.g., "third-party" defined twice with or without the "~"
5. **Content filtering rules**: Rules specified for cosmetic/content filtering
6. **Unsupported modifier options**: Any rule containing modifier options not defined in the [AdBlock Plus filter documentation](https://help.adblockplus.org/hc/en-us/articles/360062733293-How-to-write-filters)
7. **Specifically unsupported modifiers**: Rules containing `genericblock` or `popup` modifiers

**Note**: This tool is designed to help with Manifest V3 migration. Always test your converted rules thoroughly in your extension environment.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.