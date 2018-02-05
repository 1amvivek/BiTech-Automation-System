import json
from KeywordMatch import getKeywordsFromJSON


def readJSON(path):
    with open(path) as data_file:
        data = json.load(data_file)
        return data  # reading json data


def getRemainingKeywordPairs(keywordsResult):
    keywordsPdf = readJSON('uploads/keywords.json')
    for keywordresult in keywordsResult.values():
        if keywordresult in keywordsPdf.keys():
            keywordsPdf.pop(keywordresult)
    return keywordsPdf
