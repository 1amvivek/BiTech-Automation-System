import PyPDF2


def readPdf():
    import json
    pdfFileObj = open('uploads/keywords.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    skip = False
    dict = {}
    startingLine = ''
    isKeyword = True
    code = ''
    keywordUntil = 0

    for pageNum in range(pdfReader.numPages):
        elePos = 0
        currentPage = pdfReader.getPage(pageNum).extractText()
        content = currentPage.splitlines()
        facultyChoosingKeyword = 0
        for line in content:
            if line.find("choosing the keyword") != -1:  # content starts here
                skip = True
                continue

            if skip:
                if line == 'Page:':  # content ends here
                    break

                if line == ' ' or line == '':  # skip lines
                    continue

                if line[0] == ' ':
                    isKeyword = True
                    keywordUntil = 2  # keyword is in next two lines
                    facultyChoosingKeyword = line[1]
                    continue

                if isKeyword and keywordUntil > 0:
                    keywordUntil -= 1
                    elePos += 1
                    if elePos % 2 == 0:
                        if code.isdigit() and facultyChoosingKeyword != '0':  # condition to check whether they are proper keywords
                            dict[line.lower()] = code
                    else:
                        code = line

    json = json.dumps(dict)
    outputFile = open('uploads/keywords.json', 'w')
    print("Hello")
    outputFile.write(json)