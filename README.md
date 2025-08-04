# urlPatternParser

A Python codebase for converting unformatted URL filtering rules (like those from EasyList) into Manifest V3 compatible declarativeNetRequest API rules.

## Overview

The `urlPatternParser` helps browser extension developers migrate from Manifest V2 to V3 by transforming traditional ad-blocking and content filtering rules into the new declarativeNetRequest format required by Chrome's Manifest V3.

## Features

- ✅ Parses EasyList and similar filter list formats
- ✅ Converts to Manifest V3 declarativeNetRequest rules
- ✅ Handles various rule types and patterns
- ✅ Validates generated rules

## Supported Rule Types
Your input should be a text file (.txt) containing rules, The parser supports various rule formats including:
- **Basic URL patterns**: `||example.com^`
- **Wildcard patterns**: `/ads/*`
- **Exception rules**: `@@||allowlist.com^`
- **Domain-specific rules**: `example.com##.ad-banner`
- **Resource type filters**: `||ads.com^$script,image`

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
   python run.py --inputPath "input.txt" --outputFolderPath "folder"
   ```

### Arguments

- `inputPath` - Path to your input text file (required)
- `outputFolderPath` - Path to the folder where manfest.json v3 rule will be stored


## Using as a Python Library

You can also import and use the parser directly in your Python code:

```python
from parser import Parser

# Convert
parser = Parser()
result = parser.convert("txt file location", "processed json folder location")
```

## Getting Help

```bash
python run.py --help
```

This will display all available options and usage information.


## Disclaimer

Invalid URL rules will be automatically dropped during parsing. This includes:

1. Rules with invalid URL filter i.e. empty filters and filters starting with "||*"
2. Rules that have invalid regex filters
3. Rules with duplicate initiator domain options (multiple "domain=" declarations)
4. Rules with duplicate domain type definitions (e.g., "third-party" defined twice with or without the "~")
5. Rules specified for content filtering

**Note**: This tool is designed to help with Manifest V3 migration. Always test your converted rules thoroughly in your extension environment.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.