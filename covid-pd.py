import urllib.request as ur
import json
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10,7)

DOWNLOAD_RECENT = True
dayNumber = 15 # how many days to plot
colorTreshold = 0 # only districts with higher incidence are colored
rateTreshold  = -1.00 # only districts with higher incidence growth during last week are colored
appearenceTreshold = 5 # only districts with higher incidence are plotted
plotLimit = 700
# populDict = {
#     'Rīga': 627487,
#     'Rēzekne': 27613,
#     'Olaines novads': 19500,
#     'Babītes novads': 11131,
#     'Tukuma novads': 27850,
#     'Jelgava': 55972,
#     'Ķekavas novads': 24306,
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
    urlSPKC = 'https://data.gov.lv/dati/lv/api/3/action/datastore_search?resource_id=492931dd-0012-46d7-b415-76fe0ec7c216&limit=100000'
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

df = pd.read_json(alldataNet)
df = pd.DataFrame( df["result"]["records"] )
df = df[["Datums", "14DienuKumulativaSaslimstiba", "AdministrativiTeritorialasVienibasNosaukums"]]
df = df[ df["14DienuKumulativaSaslimstiba"] != "no 1 līdz 5" ]
df = df[ df["14DienuKumulativaSaslimstiba"] != "..." ]
df["14DienuKumulativaSaslimstiba"] = pd.to_numeric(df["14DienuKumulativaSaslimstiba"], errors='coerce')
df.to_excel("covid.xlsx")
# df = df.groupby("Datums").sum()
# print(df)
# print(df.info())


for distr in populDict.keys():
    df2 = df[ df["AdministrativiTeritorialasVienibasNosaukums"] == distr ]
    plt.plot(df2["14DienuKumulativaSaslimstiba"]/populDict[distr]*1e5, label='', color='grey', alpha=0.2)
for distr in ['Rīga', 'Daugavpils', 'Jelgava', 'Tukuma novads', 'Olaines novads']:
    df2 = df[ df["AdministrativiTeritorialasVienibasNosaukums"] == distr ]
    plt.plot(df2["14DienuKumulativaSaslimstiba"]/populDict[distr]*1e5, label=distr)
plt.legend(loc='upper left')
plt.xlabel('Dienas')
plt.ylabel('Saslimušo skaits pēdējās 2 nedēļās, uz 100k iedzīvotāju')
axis = plt.gca()
axis.set_ylim(bottom=0)
# plt.yscale('log')
plt.savefig('covid.png')
plt.show()

