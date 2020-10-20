import urllib.request as ur
import json

urlSPKC = 'https://data.gov.lv/dati/lv/api/3/action/datastore_search?resource_id=492931dd-0012-46d7-b415-76fe0ec7c216&limit=50000'
fileobj = ur.urlopen(url=urlSPKC)
alldataNet = fileobj.read()

fOut = open('covid-data-raw.json', mode='w')
fOut.write(str(alldataNet))
fOut.close()

# fIn = open('covid-data-raw.json', mode='r')
# alldataNet = fIn.read()
# fIn.close

pyData = json.loads(alldataNet)
pyData = pyData['result']
pyData = pyData['records']
# print(pyData[-1])

populDict = {
    'Olaine': 19500,
    'Rīga': 632600,
    'Kuldīga': 22300,
    'Tukuma novads': 27850,
    'Vecpiebalga': 3543
}
districtNumber = 120
recentCasesDict = dict(populDict)
recentCases100kDict = dict(populDict)

for districtName in populDict.keys():
    casesBefore = '1'
    casesNow = '1'
    i = -1
    while i>-districtNumber*16:
        # print(pyData[i]['Datums'], pyData[i]['AdministrativiTeritorialasVienibasNosaukums'])
        entryDict = pyData[i]
        if districtName in entryDict['AdministrativiTeritorialasVienibasNosaukums']:
            if i>-districtNumber:
                casesNow = entryDict['ApstiprinataCOVID19infekcija']
                # print(districtName, i, entryDict['Datums'], entryDict['ApstiprinataCOVID19infekcija'])
            elif i>-districtNumber*15.5 and i<-districtNumber*14.5:
                casesBefore = entryDict['ApstiprinataCOVID19infekcija']
                if 'no 1' in casesBefore:
                    casesBefore = 1
                # print(districtName, i, entryDict['Datums'], entryDict['ApstiprinataCOVID19infekcija'])
                break
        i -= 1
    cases14d = int(casesNow) - int(casesBefore) if int(casesNow)>int(casesBefore) else 0
    recentCasesDict[districtName] = cases14d
    recentCases100kDict[districtName] = round(cases14d/populDict[districtName]*1e5)

date = pyData[-1]['Datums']
date = date.split('T')[0]
print(f'Date: {date}\n')
print('District      \tcases\tfor 100k')
for districtName in populDict.keys():
    dNmod = districtName
    while len(dNmod)<len('Vecpiebalga'):
        dNmod += ' '
    print(dNmod, '\t', f'{recentCasesDict[districtName]:4}', '\t', f'{recentCases100kDict[districtName]:4}')

input('Print any key')