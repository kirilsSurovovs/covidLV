import urllib.request as ur
import json
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10,5)

# urlSPKC = 'https://data.gov.lv/dati/lv/api/3/action/datastore_search?resource_id=492931dd-0012-46d7-b415-76fe0ec7c216&limit=50000'
# fileobj = ur.urlopen(url=urlSPKC)
# alldataNet = fileobj.read()
#
# ## fOut = open('covid-data-raw.json', mode='w')
# ## fOut.write(str(alldataNet))
# ## fOut.close()

fIn = open('covid-data-raw.json', mode='r')
alldataNet = fIn.read()
alldataNet = str(alldataNet)
alldataNet = alldataNet.strip("b")
alldataNet = alldataNet.strip("'")
fIn.close

pyData = json.loads(alldataNet)
pyData = pyData['result']
pyData = pyData['records']
# print(pyData[-1])

populDict = {
    'Olaines novads': 19500,
    'R\\xc4\\xabga': 632600,
    'Kuld\\xc4\\xabgas novads': 22300,
    'Tukuma novads': 27850,
    'Daugavpils': 110000
}
districtNumber = 120
recentCasesDict = dict(populDict)
recentCases100kDict = dict(populDict)
recentCases100kArray = {} # will contain 7-day infections per 100k

for districtName in populDict.keys():
    casesBefore = '1'
    casesNow = '1'
    recentCases100kArray[districtName] = []
    i = -1
    while i>-districtNumber*16:
        # print(pyData[i]['Datums'], pyData[i]['AdministrativiTeritorialasVienibasNosaukums'])
        entryDict = pyData[i]
        if districtName == entryDict['AdministrativiTeritorialasVienibasNosaukums']:
            cases = entryDict['ApstiprinataCOVID19infekcija']
            if 'no 1' in cases:
                recentCases100kArray[districtName].append(1)
            else:
                recentCases100kArray[districtName].append(int(cases))
            if i>-districtNumber:
                casesNow = entryDict['ApstiprinataCOVID19infekcija']
                # print(districtName, i, entryDict['Datums'], entryDict['ApstiprinataCOVID19infekcija'])
            elif i>-districtNumber*15.5 and i<-districtNumber*14.5:
                casesBefore = entryDict['ApstiprinataCOVID19infekcija']
                if 'no 1' in casesBefore:
                    casesBefore = 1
                # print(districtName, i, entryDict['Datums'], entryDict['ApstiprinataCOVID19infekcija'])
                # break
        i -= 1
    n = len(recentCases100kArray[districtName])
    print(n)
    for i in range(n//2):
    #     # print(recentCases100kArray[districtName][i])
        recentCases100kArray[districtName][i] = recentCases100kArray[districtName][i] - recentCases100kArray[districtName][n//2 + i]
        recentCases100kArray[districtName][i] /= populDict[districtName]/1e5
        recentCases100kArray[districtName][i] = round(recentCases100kArray[districtName][i])
    for i in range(n//2):
        del recentCases100kArray[districtName][-1]
    cases14d = int(casesNow) - int(casesBefore) if int(casesNow)>int(casesBefore) else 0
    recentCasesDict[districtName] = cases14d
    recentCases100kDict[districtName] = round(cases14d/populDict[districtName]*1e5)

print(recentCases100kArray)
dienas = []
for i in range(8):
    dienas.append(i-7)
for districtName in populDict.keys():
    if len(recentCases100kArray[districtName]) > 8.5:
        del recentCases100kArray[districtName][-1]
    elif len(recentCases100kArray[districtName]) < 7.5:
        recentCases100kArray[districtName].append(recentCases100kArray[districtName][-1])
    dataList = list(recentCases100kArray[districtName])
    dataList.reverse()
    plt.plot(dienas, dataList, label=districtName)
plt.legend(populDict.keys(), loc='upper center')
plt.xlabel('Dienas (0 = šodien)')
plt.ylabel('Saslimušo skaits pēdējā nedēļā, uz 100k iedzīvotāju')
plt.show()


date = pyData[-1]['Datums']
date = date.split('T')[0]
print(f'Date: {date}\n')
print('District          cases in 14 d    per 100k')
for districtName in populDict.keys():
    dNmod = districtName
    while len(dNmod)<len('Vecpiebalgas novads'):
        dNmod += ' '
    print(dNmod, '\t', f'{recentCasesDict[districtName]:6}', '\t', f'{recentCases100kDict[districtName]:6}')

input('Print any key')