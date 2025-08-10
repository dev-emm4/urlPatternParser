import json
import re
from pathlib import Path
from typing import List, Dict, Any

from error import FilePathError
from mv3Rule.mv3Rule import Mv3Rule


class FileHandler:
    def __init__(self):
        self._validOptionPattern = re.compile(
            r'^(?:script|image|stylesheet|object|xmlhttprequest|subdocument|ping|websocket|document|~script|~image'
            r'|~stylesheet|~object|~xmlhttprequest|~subdocument|~ping|~websocket|~document|~other|font|media|other'
            r'|domain=~?[a-zA-Z0-9.-]+\.[a-zA-Z0-9]{1,}(?:\|~?[a-zA-Z0-9.-]+\.[a-zA-Z0-9]{1,})*)(?:,'
            r'(?:script|image|stylesheet|object|xmlhttprequest|subdocument|ping|websocket|document|~script|~image'
            r'|~stylesheet|~object|~xmlhttprequest|~subdocument|~ping|~websocket|~document|~other|font|media|other'
            r'|domain=~?[a-zA-Z0-9.-]+\.[a-zA-Z0-9]{1,}(?:\|~?[a-zA-Z0-9.-]+\.[a-zA-Z0-9]{1,})*))*$'
        )
        self._cosmeticFilterPattern = r'#[@$?]?#'

    def readUnformattedRuleFrom(self, aInputFilePath: str) -> List[str]:
        stringList: List[str]
        safeInputFilePath: Path = self._covertToSafePath(aInputFilePath)

        self._validateFile(safeInputFilePath, ['.txt'])

        with open(safeInputFilePath, 'r', encoding='utf-8') as file:
            stringList: List[str] = file.read().splitlines()

        unformattedRules: List[str] = self._extractUnformattedFilteringRulesFrom(stringList)
        return unformattedRules

    def _extractUnformattedFilteringRulesFrom(self, aStringList: List[str]) -> List[str]:
        unformattedRules: List[str] = []
        for string in aStringList:
            stringWithoutSpace: str = self._removeSpacesFromString(string)
            if self._isStringAValidNetworkFilteringRule(stringWithoutSpace):
                unformattedRules.append(stringWithoutSpace)

        return unformattedRules

    def _removeSpacesFromString(self, aString: str) -> str:
        return re.sub(r'\s+', '', aString)

    def _isStringAValidNetworkFilteringRule(self, aString: str) -> bool:
        if aString == "":
            return False
        elif aString.startswith('!'):
            return False
        elif re.search(self._cosmeticFilterPattern, aString):
            return False
        elif '$' in aString:
            options: str = self._extractOptionsFrom(aString)
            return self._isOptionFormatValid(options)
        else:
            return True

    def _extractOptionsFrom(self, aString: str) -> str:
        options: str = aString.split('$', 1)[1]

        return options

    def _isOptionFormatValid(self, aOption: str) -> bool:
        if re.match(self._validOptionPattern, aOption):
            return True
        return False

    def writeMv3RuleJsonToOutputFile(self, aOutputFilePath: str, aMv3RuleList: List[Mv3Rule]):
        dictMv3Rule: List[Dict[str, Any]] = self._transformToDict(aMv3RuleList)
        safeOutputFilePath: Path = self._covertToSafePath(aOutputFilePath)

        with open(safeOutputFilePath, 'w', encoding='utf-8') as file:
            json.dump(dictMv3Rule, file, indent=2, ensure_ascii=False)

    def _transformToDict(self, aMv3RuleList: List[Mv3Rule]) -> List[Dict[str, Any]]:
        dictMv3RuleList: List[Dict[str, Any]] = []

        for mv3Rule in aMv3RuleList:
            dictMv3Rule: dict[str: Any] = mv3Rule.to_dict()
            dictMv3RuleList.append(dictMv3Rule)

        return dictMv3RuleList

    def generateOutPutFilePath(self, aOutPutFolderPath: str, aInputFilePath: str) -> str:
        safeInputFilePath: Path = self._covertToSafePath(aInputFilePath)
        safeOutputFilePath: Path = self._covertToSafePath(aOutPutFolderPath)

        self._validateOutputFolder(safeOutputFilePath)

        fileName: str = self._generateOutputFilename(safeInputFilePath)
        fullOutputFilePath: Path = safeOutputFilePath / fileName

        return str(fullOutputFilePath)

    def _covertToSafePath(self, aUserPathString) -> Path:
        path = Path(aUserPathString)
        path = path.expanduser()
        path = path.resolve()
        return path

    def _validateOutputFolder(self, aOutputFolderPath: Path):
        if not aOutputFolderPath.exists():
            aOutputFolderPath.mkdir(parents=True, exist_ok=True)
        if not aOutputFolderPath.is_dir():
            raise FilePathError(f'folder does not exist: {aOutputFolderPath}')

    def _generateOutputFilename(self, aInputFilePath: Path) -> str:
        stem: str = aInputFilePath.stem
        outputFilename: str = f"{stem}{'_processed'}{'.json'}"
        return outputFilename

    def _validateFile(self, aFilePath: Path, aExtension: List[str]):
        if not aFilePath.exists():
            raise FilePathError(f'file path does not exist: {aFilePath}')
        if not aFilePath.is_file():
            raise FilePathError(f'file does not exists: {aFilePath}')
        if not aFilePath.suffix.lower() in aExtension:
            raise FilePathError('invalid extension')
