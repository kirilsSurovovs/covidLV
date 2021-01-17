#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def read_series():
    return pd.Series()

def main():

    DF = pd.read_excel('vak.xlsx')
    # print(DF[ DF["Vakcinēto personu skaits"] < 2 ], '\n\n')
    # print(DF.info())
    # nodate = DF.drop(columns=["Vakcinācijas datums"])
    DF = DF.rename(
    columns={
        "Vakcinācijas iestādes nosaukums": "nos",
        "Vakcinēto personu skaits": "skaits",
        "Vakcinācijas iestādes kods": "kods",
        "Vakcinācijas datums": "dat"
    }
    )
    DF = DF.groupby("dat").sum()

    print(DF.head())
    plt.figure(figsize=(15, 8))
    plt.plot(DF["skaits"])
    # DF.plot.area(subplots=True)

    # rakus  = DF[ DF["Vakcinācijas iestādes kods"] == 10000234 ]
    # rakus2 = rakus[rakus["Indikācijas vakcinācijai"] == "Ārstniecības iestādes darbinieks;"]
    # rakus = rakus[ rakus["Indikācijas vakcinācijai"] != "Ārstniecības iestādes darbinieks;" ]
    # print(rakus.info())
    # print(rakus2.info())

    # day_place_vacNum = DF[["Vakcinācijas datums", "Vakcinācijas iestādes kods", "Vakcinēto personu skaits"]]
    # print(day_place_vacNum)

    # plt.plot(rakus["Vakcinācijas datums"], rakus["Vakcinēto personu skaits"])
    # plt.plot(rakus2["Vakcinācijas datums"], rakus2["Vakcinēto personu skaits"])
    
    ax = plt.gca()
    ax.grid()
    ax.set_ylim(bottom=0)
    ax.set_xlabel('Datums')
    ax.set_ylabel('Vakcinēto personu skaits')
    plt.tight_layout(pad=0.5)
    plt.savefig('vak.png')
    plt.show()

if __name__ == "__main__":
    main()
