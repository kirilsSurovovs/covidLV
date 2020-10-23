import urllib.request as ur
import json
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10,5)

DOWNLOAD_RECENT = True
populDict = {
    # 'Vecpiebalgas novads': 3543,
    # 'Salaspils novads': 22659,
    # 'Krāslavas novads': 14155,
    # 'Dundagas novads': 3641,
    'Olaines novads': 19500,
    'Tukuma novads': 27850,
    'Jelgava': 55972,
    'Ogres novads': 33000,
    'Daugavpils': 110000
}
dayNumber = 30 # how many days to plot

if DOWNLOAD_RECENT:
    # var pieveinot rajonus ar garumzīmēm
    populDict['Rīga'] = 632600
    populDict['Kuldīgas novads'] = 22300

    urlSPKC = 'https://data.gov.lv/dati/lv/api/3/action/datastore_search?resource_id=492931dd-0012-46d7-b415-76fe0ec7c216&limit=50000'
    fileobj = ur.urlopen(url=urlSPKC)
    alldataNet = fileobj.read()

    fOut = open('covid-data-raw.json', mode='w')
    fOut.write(str(alldataNet))
    fOut.close()
else:
    fIn = open('covid-data-raw.json', mode='r')
    alldataNet = fIn.read()
    alldataNet = str(alldataNet)
    alldataNet = alldataNet.strip("b")
    alldataNet = alldataNet.strip("'")
    alldataNet = alldataNet.replace('\\','\\\\')
    fIn.close

pyData = json.loads(alldataNet)
pyData = pyData['result']
pyData = pyData['records']
# print(pyData[-1])

districtNumber = 120
recentCasesDict = dict(populDict)
recentCases100kDict = dict(populDict)
recentCases100kArray = {} # will contain 7-day infections per 100k
dateArray = {} #

for districtName in populDict.keys():
    casesBefore = '1'
    casesNow = '1'
    recentCases100kArray[districtName] = []
    dateArray[districtName] = []
    i = -1
    while i>-districtNumber*(dayNumber+7):
        entryDict = pyData[i]
        if districtName == entryDict['AdministrativiTeritorialasVienibasNosaukums']:
            # print(entryDict['Datums'], entryDict['AdministrativiTeritorialasVienibasNosaukums'], entryDict['ApstiprinataCOVID19infekcija'])
            dateArray[districtName].append(entryDict['Datums'])
            cases = entryDict['ApstiprinataCOVID19infekcija']
            if 'no 1' in cases:
                recentCases100kArray[districtName].append(1)
            else:
                recentCases100kArray[districtName].append(int(cases))
        i -= 1
    recentCases100kArray[districtName] = [x for _,x in sorted(zip(dateArray[districtName], recentCases100kArray[districtName]))]
    recentCases100kArray[districtName].reverse()
    cases14d = recentCases100kArray[districtName][0] - recentCases100kArray[districtName][13]
    recentCasesDict[districtName] = cases14d
    recentCases100kDict[districtName] = round(cases14d/populDict[districtName]*1e5)

    print(districtName, recentCases100kArray[districtName])
    n = len(recentCases100kArray[districtName])
    if n%2 == 1:
        del recentCases100kArray[districtName][-1]
        n -= 1
    for i in range(n-7):
        recentCases100kArray[districtName][i] = recentCases100kArray[districtName][i] - recentCases100kArray[districtName][i+7]
        recentCases100kArray[districtName][i] /= populDict[districtName]/1e5
        recentCases100kArray[districtName][i] = round(recentCases100kArray[districtName][i])
        print(districtName, recentCases100kArray[districtName][i])
    for i in range(7):
        del recentCases100kArray[districtName][-1]

print(recentCases100kArray)
dienas = []
for i in range(dayNumber+1):
    dienas.append(i-dayNumber)
for districtName in populDict.keys():
    dataList = list(recentCases100kArray[districtName])
    #     if len(recentCases100kArray[districtName]) > dayNumber:
    #         del recentCases100kArray[districtName][-1]
    #     elif len(recentCases100kArray[districtName]) < dayNumber:
    #         recentCases100kArray[districtName].append(recentCases100kArray[districtName][-1])
    while len(dienas) > len(dataList):
        dataList.append(dataList[-1])
    dataList.reverse()
    print(len(dienas), dienas)
    print(len(dataList), dataList)
    plt.plot(dienas, dataList, label=districtName)
plt.legend(populDict.keys(), loc='upper left')
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