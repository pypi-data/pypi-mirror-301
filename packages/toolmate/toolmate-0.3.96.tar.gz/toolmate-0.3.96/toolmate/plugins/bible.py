"""
CUV Bible
Reference: https://bible.fhl.net/json
cuv = requests.get("https://bible.fhl.net/json/qb.php?gb=0&chap=3&sec=6&chineses=出")
cuv.text.encode().decode('unicode_escape')

NET Bible
Reference: https://labs.bible.org/
https://labs.bible.org/api/?passage=John+3:16-17;%20Deut%206:4
"""

from toolmate import config, print1
from toolmate.bible.bible_verse_parser import BibleVerseParser

def extract_bible_references(function_args):
    content = config.currentMessages[-1]["content"]
    config.toolTextOutput = BibleVerseParser(False).extractAllReferencesReadable(content)
    if config.toolTextOutput:
        print2("```references")
        print1(config.toolTextOutput)
        print2("```")
    return ""

functionSignature = {
    "examples": [
        "Extract Bible references",
    ],
    "name": "extract_bible_references",
    "description": "Extract Bible references from a block of text",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}

config.addFunctionCall(signature=functionSignature, method=extract_bible_references)
config.inputSuggestions.append("Extract Bible references: ")
