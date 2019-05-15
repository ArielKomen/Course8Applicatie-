from Bio import Entrez

def main():
    d2_lijst = bestanden_inlezen()
    pubmed_zoeken(d2_lijst)

def bestanden_inlezen():
    #je wil het liefst drie lijsten met data terugkrijgen
    lijst_met_bestandspaden = ["/home/cole/Documents/course_8/afvinkopdrachten /afvinkopdracht 3/data/data fynotype ",
                               "/home/cole/Documents/course_8/afvinkopdrachten /afvinkopdracht 3/data/data moleculaire effecten",
                               "/home/cole/Documents/course_8/afvinkopdrachten /afvinkopdracht 3/data/pre-registration-process-export.csv"]
    d2_lijst = []

    for bestandspad in lijst_met_bestandspaden:
        lijst = generiek_bestand_inlezen(bestandspad)
        d2_lijst.append(lijst)
    #print(len(d2_lijst[0]))
    #print(len(d2_lijst[1]))
    #print(len(d2_lijst[2]))
    return d2_lijst
def generiek_bestand_inlezen(bestandspad):
    # in deze functie op een generieke manier een bestand inlezen
    # de bestanden zijn allemaal op enter gescheiden, dus dat maakt alles makkelijk
    lijst = []

    for regel in open(bestandspad):
        lijst.append(regel.strip())
    return lijst

def term_bepalen(d2_lijst, hoeveel_items_zoeken):
    lijst_met_zoektermen = []

    # In deze functie de combinaties bepalen.
    for eerste_item in d2_lijst[0][0:hoeveel_items_zoeken]:
        for tweede_item in d2_lijst[1][0:hoeveel_items_zoeken]:
            for derde_item in d2_lijst[2][0:hoeveel_items_zoeken]:
                zoekterm = eerste_item + "+AND+" + tweede_item + "+AND+" + derde_item
                lijst_met_zoektermen.append(zoekterm)
    return lijst_met_zoektermen

def pubmed_zoeken(d2_lijst):
    # alleen de eerste twee zoeken.
    hoeveel_items_zoeken = 2
    lijst_met_records = []
    opteller = 0


    lijst_met_zoektermen = term_bepalen(d2_lijst, hoeveel_items_zoeken)
    Entrez.email = "A.komen@student.han.nl"

    for zoekterm in lijst_met_zoektermen:
        handle = Entrez.esearch(db="pubmed", term=zoekterm)
        record = Entrez.read(handle)
        lijst_met_records.append(record)

    for record in lijst_met_records:
        print("van zoekterm "+lijst_met_zoektermen[opteller]+" zijn er zoveel hits gevonden: "+str(len(record["Count"])))
        opteller += 1


main()
