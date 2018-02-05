import json
import re
from rake_nltk import Rake


def keywordMatch(title, description, backgroundInformation):
    print("Entering Keyword Match")
    keywordReport = {}
    keywordsPdf = getKeywordsFromJSON('uploads/keywords.json')
    keywordReport = titleMatch(title.lower(), keywordsPdf, keywordReport)
    keywordReport = descriptionMatch(description, keywordsPdf, keywordReport)
    if backgroundInformation != '':
        keywordReport = backgroundInformationMatch(backgroundInformation, keywordsPdf, keywordReport)
    keywordsHits = sorted(keywordReport, key=keywordReport.__getitem__) # Sorting keywords based on rank in asc order
    print("Exiting Keyword Match")
    topKeywordsHits = reversed(keywordsHits[-30:]) # getting the top 30 keywords
    return getKeywordswithId(topKeywordsHits)


def descriptionMatch(description, keywordsPdf, keywordReport):
    print("Entering Description Match")
    r = Rake()
    r.extract_keywords_from_text(description)
    keywords = list(set(r.get_ranked_phrases()))
    splitkeywords = []
    for word in keywords:
        word = word.strip()
        splitwords = re.split(',* |;* |:* |\.* |\s+ ', word)
        if len(splitwords) > 0:
            for splitword in splitwords:
                if (splitword is None or splitword.isdigit()) and splitword in splitkeywords:
                    splitkeywords.remove(splitword)
                    continue
                splitkeywords.append(splitword.lower())
    splitkeywords = list(set(splitkeywords))
    print("Exiting Description Match")
    return match(splitkeywords, keywordsPdf, keywordReport, 1.0)


def titleMatch(title, keywordsPdf, keywordReport):
    print("Entering Title Match")
    splitkeywords = list(set(re.split(',* |;* |:* |\.* |\s+ |( |) |{ |}', title.strip())))
    if len(splitkeywords) > 1:
        for splitword in splitkeywords:
            if (splitword is None or splitword.isdigit()) and splitword in splitkeywords:
                splitkeywords.remove(splitword)
                continue
    # print(match(splitkeywords, keywordsPdf, keywordReport, 2))
    print("Exiting Title Match")
    return match(splitkeywords, keywordsPdf, keywordReport, 2.0)


def backgroundInformationMatch(backgroundInformation, keywordsPdf, keywordReport):
    print("Entering BackgroundInformation Match")
    r = Rake()
    r.extract_keywords_from_text(backgroundInformation)
    keywords = list(set(r.get_ranked_phrases()))
    splitkeywords = []
    for word in keywords:
        word = word.strip()
        splitwords = re.split(',* |;* |:* |\.* |\s+ ', word)
        if len(splitwords) > 0:
            for splitword in splitwords:
                if (splitword is None or splitword.isdigit()) and splitword in splitkeywords:
                    splitkeywords.remove(splitword)
                    continue
                splitkeywords.append(splitword.lower())
    splitkeywords = list(set(splitkeywords))
    print("Exiting Background Match")
    return match(splitkeywords, keywordsPdf, keywordReport, 1.0)


def match(splitkeywords, keywordsPdf, keywordReport, rankStep):
    print("Entering Match Method")
    for wordForm in splitkeywords:
        for wordPdf in keywordsPdf:
            if wordForm == wordPdf:
                if wordPdf in keywordReport.keys():
                    keywordReport[wordPdf] = keywordReport[wordPdf] + (2.0 * rankStep)
                    continue
                else:
                    keywordReport[wordPdf] = rankStep
                    continue
            if wordPdf.find(wordForm) > -1:
                wordPositionRank = wordPositionRankStep(wordPdf, wordForm)
                if wordPdf in keywordReport.keys():
                    keywordReport[wordPdf] = keywordReport[wordPdf] + (wordPositionRank * rankStep)
                else:
                    keywordReport[wordPdf] = wordPositionRank * rankStep
    return keywordReport


def wordPositionRankStep(wordPdf, wordForm):
    wordPositionRank = 1
    if wordPdf.find(wordForm) != 0:
        splitwords = re.split(',* |\.* |\s+ ', wordPdf)
        for word in splitwords:
            if word.find(wordForm) == 0:
                wordPositionRank = 0.75
                break
            else:
                wordPositionRank = 0.5
    return wordPositionRank


def getKeywordswithId(keywords):
    keywordsWithId = {}
    with open('uploads/keywords.json') as data_file:
        data = json.load(data_file)
    for keyword in keywords:
        if keyword in data.keys():
            keywordsWithId[data[keyword]] = keyword
    return keywordsWithId


def getKeywordsFromJSON(path):
    with open(path) as data_file:
        data = json.load(data_file)
        return list(data.keys())  # Keywords from the pdf