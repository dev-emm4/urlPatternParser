# urlPatternParser

A Python library for converting unformatted URL filtering rules (like those from EasyList) into Manifest V3 compatible declarativeNetRequest API rules.

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

---

**Note**: This tool is designed to help with Manifest V3 migration. Always test your converted rules thoroughly in your extension environment.