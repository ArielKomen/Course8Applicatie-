from Bio import Entrez
from Bio import Medline
import matplotlib.pyplot as plt
import numpy as np

def main():
    jaren_dict = {}
    zoekterm_dict = {}
    jaren_dict = data_opzoeken(jaren_dict, zoekterm_dict)
    grafiek_maken(jaren_dict)


def data_opzoeken(jaren_dict, zoekterm_dict):
    zoekterm_dict, zoekterm = zoek_woord_op(zoekterm_dict)
    jaren_dict = get_jarenlijst(zoekterm_dict, zoekterm, jaren_dict)
    vraag_om_nog_meer_input(jaren_dict, zoekterm, zoekterm_dict)
    return jaren_dict


def vraag_om_nog_meer_input(jaren_dict, zoekterm, zoekterm_dict):
    print("wil je nog meer zoekwoorden opgeven?")
    vraag = input("klik op: y voor nog meer input: ")
    if vraag == "y":
        data_opzoeken(jaren_dict, zoekterm_dict)
    else:
        grafiek_maken(jaren_dict)
    return jaren_dict, zoekterm


def zoek_woord_op(zoekterm_dict):
    Entrez.email = "ariel.komen@filternet.nl"  # Always tell NCBI who you are
    zoekterm = input("geef een zoekwoord op: ")
    handle = Entrez.esearch(db="pubmed", term=zoekterm, retmax=300)
    record = Entrez.read(handle)
    print(len(record["IdList"]))
    zoekterm_dict[zoekterm] = record
    return zoekterm_dict, zoekterm


def get_jarenlijst(zoekterm_dict, zoekterm, jaren_dict):
    # nu nog de datums achterhalen
    jaren_lijst = []
    idlist = zoekterm_dict.get(zoekterm)["IdList"]

    item_handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline", retmode="text")
    records = Medline.parse(item_handle)
    for item in records:
        # print(item["DP"][0:4])
        jaren_lijst.append(item["DP"][0:4])

    jaren_dict[zoekterm] = jaren_dict_maken(jaren_lijst)


    return jaren_dict


def jaren_dict_maken(jaren_lijst):
    jaren_per_zoekterm_dict = {}

    for jaar in jaren_lijst:
        if jaar not in jaren_per_zoekterm_dict:
            jaren_per_zoekterm_dict[jaar] = 0
        else:
            jaren_per_zoekterm_dict[jaar] += 1
    return(jaren_per_zoekterm_dict)





def grafiek_maken(jaren_dict):
    opteller = 0
    width = 0.35
    N = 0
    lengte = 0
    grootste_zoekwoord = ""
    for item in jaren_dict.items():
        if len(item[1]) > N:
            N = len(item[1])
            grootste_zoekwoord = item[0]

    ind = np.arange(N)
    kleuren = ["red", "turquoise", "green", "yellow", "orange"]
    jaren_dict = x_waarde_even_lang_maken(jaren_dict)

    for zoekwoord in jaren_dict.keys():
        lengte = opteller * width
        plt.bar(ind + lengte, sorted(jaren_dict.get(zoekwoord).values()), width=width,color=kleuren[opteller], label = zoekwoord)
        #plt.bar(sorted(jaren_dict.get(zoekwoord).keys()),sorted(jaren_dict.get(zoekwoord).values()), color = kleuren[opteller])
        opteller += 1

    plt.title("hoeveel artikelen er per jaar zijn")
    plt.xlabel("de hoeveelheid artikelen")
    plt.ylabel("het jaartal")
    plt.xticks(ind + width / 2, tuple(sorted(jaren_dict.get(grootste_zoekwoord).keys())))
    plt.legend(loc='best')
    plt.show()

def x_waarde_even_lang_maken(jaren_dict):
    #eerst alle jaartallen achterhalen en in een lijst zetten.
    lijst_met_jaartallen = []
    for dict in jaren_dict.values():
        for item in dict.keys():
            if item not in lijst_met_jaartallen:
                lijst_met_jaartallen.append(item)

    #dan ervoor zorgen dat de dicts beide evenvol worden gemaakt.
    for dict in jaren_dict.values():
        for jaar in lijst_met_jaartallen:
            if jaar not in dict.keys():
                dict[jaar] = 0



    return jaren_dict






main()


