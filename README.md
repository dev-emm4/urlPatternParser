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

- **Basic URL patterns**: `||example.com^`
- **Wildcard patterns**: `/ads/*`
- **Exception rules**: `@@||allowlist.com^`
- **Domain-specific rules**: `example.com##.ad-banner`
- **Resource type filters**: `||ads.com^$script,image`

## Output Format

The parser generates rules compatible with Chrome's declarativeNetRequest API:

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

## Usage

First, clone the repository:

```bash
git clone https://github.com/dev-emm4/urlPatternParser.git
cd urlPatternParser
```

Add your unformatted rule file (txt format) to the `raRuleList` folder in the code directory.

Then run the parser to convert your filter lists:

```bash
python parser.parse(input_rules.txt, output_rules.json)
```

---

## Disclaimer

Invalid URL rules will be automatically dropped during parsing. This includes:

1. Rules that have a URL filter starting with "||*"
2. Rules that have invalid regex filters
3. Rules with duplicate initiator domain options (multiple "domain=" declarations)
4. Rules with duplicate domain type definitions (e.g., "third-party" defined twice with or without the "~")

**Note**: This tool is designed to help with Manifest V3 migration. Always test your converted rules thoroughly in your extension environment.