import urllib.request as ur
import json
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10,7)

DOWNLOAD_RECENT = True
dayNumber = 30 # how many days to plot
colorTreshold = 130 # only districts with higher incidence are colored
rateTreshold  = -1.00 # only districts with higher incidence growth during last week are colored
appearenceTreshold = 5 # only districts with higher incidence are plotted
plotLimit = 700
# populDict = {
#     'Olaines novads': 19500,
#     'Tukuma novads': 27850,
#     'Jelgava': 55972,
#     'Ogres novads': 33000,
#     'Vecpiebalgas novads': 3555,
#     'Vecumnieku novads': 7665,
#     'Rojas novads': 33000,
#     'Daugavpils': 110000
# }
populDict = {
'Rīga': 627487,
'Daugavpils': 82046,
'Jelgava': 56062,
'Jēkabpils': 21928,
'Jūrmala': 49687,
'Liepāja': 68535,
'Rēzekne': 27613,
'Valmiera': 23050,
'Ventspils': 33906,
'Aglonas novads': 3099,
'Aizkraukles novads': 8024,
'Aizputes novads': 8057,
'Aknīstes novads': 2520,
'Alojas novads': 4492,
'Alsungas novads': 1268,
'Alūksnes novads': 13895,
'Amatas novads': 4979,
'Apes novads': 3220,
'Auces novads': 6009,
'Ādažu novads': 11625,
'Babītes novads': 11131,
'Baldones novads': 5387,
'Baltinavas novads': 947,
'Balvu novads': 11715,
'Bauskas novads': 22442,
'Beverīnas novads': 2927,
'Brocēnu novads': 5633,
'Burtnieku novads': 7369,
'Carnikavas novads': 8934,
'Cesvaines novads': 2266,
'Cēsu novads': 16291,
'Ciblas novads': 2355,
'Dagdas novads': 6549,
'Daugavpils novads': 19639,
'Dobeles novads': 19286,
'Dundagas novads': 3571,
'Durbes novads': 2601,
'Engures novads': 7124,
'Ērgļu novads': 2611,
'Garkalnes novads': 8923,
'Grobiņas novads': 8347,
'Gulbenes novads': 19771,
'Iecavas novads': 8353,
'Ikšķiles novads': 9888,
'Ilūkstes novads': 6412,
'Inčukalna novads': 7640,
'Jaunjelgavas novads': 5061,
'Jaunpiebalgas novads': 1982,
'Jaunpils novads': 2141,
'Jelgavas novads': 21738,
'Jēkabpils novads': 4156,
'Kandavas novads': 7559,
'Kārsavas novads': 5193,
'Kocēnu novads': 5783,
'Kokneses novads': 4922,
'Krāslavas novads': 13770,
'Krimuldas novads': 4807,
'Krustpils novads': 5453,
'Kuldīgas novads': 22028,
'Ķeguma novads': 5281,
'Ķekavas novads': 24306,
'Lielvārdes novads': 9597,
'Limbažu novads': 16507,
'Līgatnes novads': 3266,
'Līvānu novads': 10698,
'Lubānas novads': 2148,
'Ludzas novads': 11920,
'Madonas novads': 21879,
'Mazsalacas novads': 2880,
'Mālpils novads': 3331,
'Mārupes novads': 20753,
'Mērsraga novads': 1407,
'Naukšēnu novads': 1675,
'Neretas novads': 3284,
'Nīcas novads': 3100,
'Ogres novads': 32987,
'Olaines novads': 19667,
'Ozolnieku novads': 10019,
'Pārgaujas novads': 3576,
'Pāvilostas novads': 2524,
'Pļaviņu novads': 4808,
'Preiļu novads': 9054,
'Priekules novads': 4997,
'Priekuļu novads': 7556,
'Raunas novads': 3019,
'Rēzeknes novads': 24127,
'Riebiņu novads': 4513,
'Rojas novads': 3368,
'Ropažu novads': 6835,
'Rucavas novads': 1451,
'Rugāju novads': 2061,
'Rundāles novads': 3307,
'Rūjienas novads': 4824,
'Salacgrīvas novads': 7152,
'Salas novads': 3233,
'Salaspils novads': 22758,
'Saldus novads': 21587,
'Saulkrastu novads': 6735,
'Sējas novads': 2156,
'Siguldas novads': 17992,
'Skrīveru novads': 3337,
'Skrundas novads': 4543,
'Smiltenes novads': 11985,
'Stopiņu novads': 11458,
'Strenču novads': 2838,
'Talsu novads': 27425,
'Tērvetes novads': 3302,
'Tukuma novads': 27613,
'Vaiņodes novads': 2235,
'Valkas novads': 7603,
'Varakļānu novads': 2990,
'Vārkavas novads': 1793,
'Vecpiebalgas novads': 3555,
'Vecumnieku novads': 7665,
'Ventspils novads': 10824,
'Viesītes novads': 3500,
'Viļakas novads': 4472,
'Viļānu novads': 5417,
'Zilupes novads': 2575,
}

if DOWNLOAD_RECENT:
    # var pieveinot rajonus ar garumzīmēm
    # populDict['Rīga'] = 632600
    # populDict['Kuldīgas novads'] = 22300

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

    # print(districtName, recentCases100kArray[districtName])
    n = len(recentCases100kArray[districtName])
    if n%2 == 1:
        del recentCases100kArray[districtName][-1]
        n -= 1
    for i in range(n-7):
        recentCases100kArray[districtName][i] = recentCases100kArray[districtName][i] - recentCases100kArray[districtName][i+7]
        recentCases100kArray[districtName][i] /= populDict[districtName]/1e5
        recentCases100kArray[districtName][i] = round(recentCases100kArray[districtName][i])
        # print(districtName, recentCases100kArray[districtName][i])
    for i in range(7):
        del recentCases100kArray[districtName][-1]

# print(recentCases100kArray)
dienas = []
districtNumber = 0
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
    # print(len(dienas), dienas)
    # print(len(dataList), dataList)
    if districtName == 'Rīga':
        plt.plot(dienas, dataList, label=districtName, linewidth=3, color='black')
    elif (dataList[-1] > dataList[-7]*(1 + rateTreshold)) and (dataList[-1] > colorTreshold):
        if districtNumber<10:
            plt.plot(dienas, dataList, label=districtName)
        else:
            plt.plot(dienas, dataList, linestyle='dashed', label=districtName)
        districtNumber += 1
    elif dataList[-1] > appearenceTreshold:
        plt.plot(dienas, dataList, label='', color='grey', alpha=0.2)

plt.legend(loc='upper left')
plt.xlabel('Dienas (0 = šodien)')
plt.ylabel('Saslimušo skaits pēdējā nedēļā, uz 100k iedzīvotāju')
axis = plt.gca()
axis.set_ylim([0, plotLimit])
# plt.yscale('log')
plt.savefig('covid.png')
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