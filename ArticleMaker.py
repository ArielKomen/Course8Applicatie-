import mysql.connector
from Bio import Entrez
from Bio import Medline
import json
from Article_class import Article
def main():
    article_list, disease_dictionary, compound_dictionary = article_maker()
    JSON_maker(article_list, disease_dictionary, compound_dictionary)
    #db_filler(article_list, disease_dictionary)
def article_maker():
    article_list = []
    unique_disease = []
    unique_compound = []
    disease_dictionary = {}
    compound_dictionary = {}
    PMID_set = set()
    with open("/home/stephan/PycharmProjects/Course8Applicatie-/data/export ziektes en compounds") as disease_compound:
        counter = 0
        for line in disease_compound:
            strippedline = line.rstrip("\n")
            splitline = strippedline.split(";")
            search_query = splitline[3].split("AND")
            disease = search_query[0].strip(" ")
            disease = disease.strip('\"')
            compound = search_query[1].strip(" ")
            compound = compound.strip('\"')
            PMID_set.add(splitline[0])
            article_list.append(Article(splitline[4], splitline[1], splitline[0], disease, compound))
            if compound not in unique_compound:
                unique_compound.append(compound)
    for compound in unique_compound:
        compound_dictionary[compound] = counter
        counter += 1
    with open("/home/stephan/PycharmProjects/Course8Applicatie-/data/export bitter gourd en ziektes") as bittergourd_disease:
        counter = 0
        for line in bittergourd_disease:
            strippedline = line.rstrip("\n")
            splitline = strippedline.split(";")
            if splitline[0] not in PMID_set:
                disease = splitline[3].split("AND")
                disease = disease[0].strip(" ")
                disease = disease.strip('\"')
                article_list.append(Article(splitline[4], splitline[1], splitline[0], disease, "Na"))
                if disease not in unique_disease:
                    unique_disease.append(disease)
    for disease in unique_disease:
        disease_dictionary[disease] = counter
        counter+=1
    return article_list, disease_dictionary, compound_dictionary

def JSON_maker(article_list, disease_dictionary, compound_dictionary):
    JSON_dict = {"Name":"Bitter Gourd", "disease":[]}
    article_disease_compound_dictionary = {}
    article_disease_dictionary = {}
    counter = 0
    for key in disease_dictionary:
        for article in article_list:
            if key == article.get_ziekte() and article.get_compound() != "Na":
                if key in article_disease_dictionary:
                    article_disease_dictionary[key].append(list(article.get_all_attributes()))
                else:
                    article_disease_dictionary[key] = []
                    article_disease_dictionary[key].append(list(article.get_all_attributes()))

            elif key == article.get_ziekte():
                if key in article_disease_compound_dictionary:
                    article_disease_compound_dictionary[key].append(list(article.get_all_attributes()))
                else:
                    article_disease_compound_dictionary[key] = []
                    article_disease_compound_dictionary[key].append(list(article.get_all_attributes()))
        compound_count_dict = {}
        value = article_disease_dictionary[key]
        for attributes in value:
            for compound in compound_dictionary:
                if compound in attributes:
                    if compound not in compound_count_dict:
                        compound_count_dict[compound] = 1
                    else:
                        compound_count_dict[compound] += 1
        JSON_dict["disease"].append({"name": key, "compounds":[]})
        for compound in compound_count_dict:
            JSON_dict["disease"][counter]['compounds'].append({"name":compound,"value":compound_count_dict[compound]})
        counter += 1;
    with open("/home/stephan/PycharmProjects/Course8Applicatie-/data/data.json", "w") as outfile:
        json.dump(JSON_dict, outfile)
        outfile.close()


def db_filler(article_list, disease_dictionary):

    cnx = mysql.connector.connect(host = "hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com", user = 'owe7_pg8@hannl-hlo-bioinformatica-mysqlsrv', password = 'blaat1234', database = 'owe7_pg8')
    cursor = cnx.cursor()
    for object in article_list:
        query_insert = "insert into owe7_pg8.article values(%s, %s, %s, %s, %s)"
        values = (int(object.get_pmid(object)), object.get_date(), object.get_title(), 255, disease_dictionary.get(object.get_ziekte(object)))
        print(values)
        #cursor.execute(query_insert, values)
main()