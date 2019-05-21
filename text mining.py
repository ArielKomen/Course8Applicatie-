from Bio import Entrez, Medline
import matplotlib.pyplot as plt
import numpy as np
import time

def main():
    d2_lijst = bestanden_inlezen()
    export_lijst = pubmed_zoeken(d2_lijst)
    schrijf_data_weg(export_lijst)
def bestanden_inlezen():
    """
    ziektes zijn lijst[0]
    compounds zijn lijst[1]
    bitter gourd is lijst[2]
    """
    d2_lijst = []
    lijst_met_bestandspaden = ["/home/cole/Documents/course_8/weektaken/textmining applicatie/data/ziekte lijst",
                               "/home/cole/Documents/course_8/weektaken/textmining applicatie/data/compound lijst",
                               "/home/cole/Documents/course_8/weektaken/textmining applicatie/data/bitter gourd lijst"]

    for bestandspad in lijst_met_bestandspaden:
        lijst = generiek_bestand_inlezen(bestandspad)
        d2_lijst.append(lijst)
    return d2_lijst

def generiek_bestand_inlezen(bestandspad):
    # in deze functie op een generieke manier een bestand inlezen
    # de bestanden zijn allemaal op enter gescheiden, dus dat maakt alles makkelijk
    lijst = []

    for regel in open(bestandspad):
        if regel != "":
            lijst.append(regel.strip())
    return lijst


def pubmed_zoeken(d2_lijst):
    lijst_met_records = []
    opteller = 0
    sleep_time = 0
    
    lijst_met_getallen = []
    tweede_lijst_met_getallen = []
    

    #je wilt een lijst hebben met bitter gourd en ziektes, ziektes met compounds. Dus die moet je eerst maken.
    lijst_met_bitter_gourd_ziektes = make_bitter_gourd_disease_list(d2_lijst)
    lijst_met_ziektes_compounds = make_disease_compounds_list(d2_lijst)

    Entrez.email = "A.komen@student.han.nl"

    for zoekterm in lijst_met_bitter_gourd_ziektes[0:]:
        count = get_count(zoekterm)
        time.sleep(sleep_time)
        
        lijst_met_getallen.append(float(count))
        tweede_lijst_met_getallen.append(opteller)
        opteller += 1
    
        if int(count) > 0:
            lijst_met_records = get_artikelen(zoekterm, count, lijst_met_records)
            time.sleep(sleep_time)
            print("zoveel hits: "+str(count)+" en bij deze term: "+ zoekterm)
        else:
            print("deze zoekterm heeft geen hits: "+zoekterm)
    
    #print("zoveel hits in totaal hebben meer dan 10000 artikelen: "+str(opteller))
    #visualiseer_aantal_artikelen(lijst_met_getallen, tweede_lijst_met_getallen)

    # maak de export lijst.
    export_lijst = make_export_lijst(lijst_met_records, lijst_met_bitter_gourd_ziektes)

    return export_lijst
    


def visualiseer_aantal_artikelen(lijst_met_getallen, tweede_lijst_met_getallen):
    lijst = []
    
    lijst = sorted(lijst_met_getallen)
    
    if len(lijst) == len(tweede_lijst_met_getallen):
        plt.scatter(tweede_lijst_met_getallen,lijst)

        plt.yticks(np.arange(min(lijst), max(lijst)+1, 1000.0))

        plt.yticks(np.arange(min(lijst), max(lijst)+1, 100.0))
        plt.xlabel("verschillende termen")
        plt.ylabel("hoeveelheid gevonden artikelen")
        plt.title("hoeveelheid artikelen met termen")
        plt.show()
    else:
        print("de lengte is toch niet gelijk op een of andere manier")
    
    
def get_count(zoekterm):
    handle = Entrez.esearch(db="pubmed", term=zoekterm)
    record = Entrez.read(handle)
    count = record['Count']
    return count

def get_artikelen(zoekterm, count, lijst_met_records):
    handle_item = Entrez.esearch(db="pubmed", term=zoekterm, retmax=count)
    record_item = Entrez.read(handle_item)
    lijst_met_records.append(record_item)
    return lijst_met_records


def make_disease_compounds_list(d2_lijst):
    lijst_met_ziektes_compounds = []

    # Eerst de ziektes, dat is lijst[0]
    for eerste_item in d2_lijst[0][0:]:
        if eerste_item != "":
        # Dan de compounds, dat is lijst[1]
            for tweede_item in d2_lijst[1][0:]:
                if tweede_item != "":
                    zoekterm = eerste_item + " AND " + tweede_item
                    lijst_met_ziektes_compounds.append(zoekterm)
    return lijst_met_ziektes_compounds

def make_bitter_gourd_disease_list(d2_lijst):
    lijst_met_bitter_gourd_ziektes = []

    # Eerst de ziektes, dat is lijst[2]
    for eerste_item in d2_lijst[0][0:]:
        if eerste_item != "":
        # Dan de bitter gourd, dat is lijst[1]
        #for tweede_item in d2_lijst[2][0]:
            zoekterm = eerste_item + " AND " + d2_lijst[2][1]
            lijst_met_bitter_gourd_ziektes.append(zoekterm)
    return lijst_met_bitter_gourd_ziektes

def make_export_lijst(lijst_met_records, lijst_met_ziektes_compounds):
    export_lijst = []
    opteller = 0
    # in deze forloop de data in een bestandje zetten zodat je het later weer kan gebruiken ergens anders voor.
    for record in lijst_met_records:
        export_lijst = get_info(record["IdList"], export_lijst, lijst_met_ziektes_compounds[opteller])
        #print(lijst_met_bitter_gourd_ziektes[opteller])
        opteller +=1

    return export_lijst

def get_info(idlist, export_lijst, bitter_gourd_ziekte):
    # in deze functie per id alles in een lijst zetten.
    lijst = []
    item_handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline", retmode="text")
    records = Medline.parse(item_handle)
    try:
        for item in records:        
            # item[PMID] de pubmed identifier
            # item[TI] de record title, dus hoe het heet
            # item["DP"] de datum dat het is uitgekomen
            lijst.append(item["PMID"])
            lijst.append(item["DP"])
            lijst.append("na")
            lijst.append(bitter_gourd_ziekte)
            lijst.append(item["TI"])
            export_lijst.append(lijst)
            lijst = []
                
        return export_lijst
    except:
        print("er is een error opgetreden bij: "+item["PMID"])
        lijst.append("error occured;na;na;na;na")
        export_lijst.append(lijst)
        return export_lijst

def schrijf_data_weg(export_lijst):
    # in deze methode de data wegschrijven naar een tekstbestandje
    bestand = open("/home/cole/Documents/course_8/weektaken/textmining applicatie/data/export bitter gourd en ziektes", "a")

    for lijst in export_lijst:
        regel = lijst[0]+";"+lijst[1]+";"+lijst[2]+";"+lijst[3]+";"+lijst[4]+"\n"
        bestand.write(regel)

    bestand.close()
main()










