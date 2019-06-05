######################
##Author: {Stephan Gui}
##Version: {1.0.0}
##Maintainer: {Stephan Gui}
##Contact: {Stephan.gui4@gmail.com}
##Status: {Working}
######################

#Libs
import json
#Own sources
from Article_class import Article

def main():
    """
    The function of the main() is to call the other functions.
    There are no parameters and no returns.
    """
    article_list, disease_dictionary, compound_dictionary = article_maker()
    JSON_maker(article_list, disease_dictionary, compound_dictionary)

def article_maker():
    """
    The function of article_maker is to parse articles created with the text mining
    application into article objects. Simultaneously it creates two dictionaries
    containing the unique diseases and compounds.

    :return: The function returns a list of article objects,
             a dictionary containing all the unique diseases as keys and a number as value
             and a dictionary containing all unique compounds as keys and a number as value.
    """
    article_list = []
    unique_disease = []
    unique_compound = []
    disease_dictionary = {}
    compound_dictionary = {}
    PMID_set = set()
    with open("data/export ziektes en compounds") as disease_compound:
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
    with open("data/export ziektes en bitter gourd") as bittergourd_disease:
        counter = 0
        for line in bittergourd_disease:
            strippedline = line.rstrip("\n")
            splitline = strippedline.split(";")
            if splitline[0] not in PMID_set:
                search_query = splitline[3].split("AND")
                disease = search_query[0].strip(" ")
                disease = disease.strip('\"')
                article_list.append(Article(splitline[4], splitline[1], splitline[0], disease, "Na"))
                if disease not in unique_disease:
                    unique_disease.append(disease)
    for disease in unique_disease:
        disease_dictionary[disease] = counter
        counter+=1
    for compound in unique_compound:
        compound_dictionary[compound] = counter
        counter += 1
    return article_list, disease_dictionary, compound_dictionary

def JSON_maker(article_list, disease_dictionary, compound_dictionary):
    """
    The function of JSON_maker is to create a JSON file which can be visualised by the sunburst script.

    :param article_list: The article list contains a list of all the article objects.
    :param disease_dictionary: The disease_dictionary contains all the unique diseases as keys and a number as value.
    :param compound_dictionary: The compound_dictionary contains all unique compounds as keys and a number as value.
    :return: The function returns two JSON files.
             Bittergourd_disease_compound.json
                {"name": "Bittergourd", "children":[{"name": "disease","children"[{"name":"compound", "size": int}]}]}
             Bittergourd_compound_disease.json
                {"name": "Bittergourd", "children":[{"name": "compound","children"[{"name":"disease", "size": int}]}]}
    """
    Bittergourd_disease_compound_JSON = {"name":"Bitter Gourd", "children":[]}
    Bittergourd_compound_disease_JSON = {"name":"Bitter Gourd", "children":[]}
    article_disease_dictionary = {}
    article_compound_dictionary = {}
    counter = 0
    for disease in disease_dictionary:
        for article in article_list:
            if disease == article.get_ziekte():
                if disease in article_disease_dictionary:
                    article_disease_dictionary[disease].append(list(article.get_all_attributes()))
                else:
                    article_disease_dictionary[disease] = []
                    article_disease_dictionary[disease].append(list(article.get_all_attributes()))
        compound_count_dict = {}
        value = article_disease_dictionary[disease]
        for attributes in value:
            for compound in compound_dictionary:
                if compound in attributes:
                    if compound not in compound_count_dict:
                        compound_count_dict[compound] = 1
                    else:
                        compound_count_dict[compound] += 1
        Bittergourd_disease_compound_JSON["children"].append({"name": disease, "children":[]})
        for compound in compound_count_dict:
            Bittergourd_disease_compound_JSON["children"][counter]['children'].append({"name":compound,"size":compound_count_dict[compound]})
        counter += 1;
    with open("data/Bittergourd_disease_compound.json", "w") as outfile:
        json.dump(Bittergourd_disease_compound_JSON, outfile)
        outfile.close()
    counter = 0
    for compound in compound_dictionary:
        for article in article_list:
            if compound == article.get_compound():
                if compound in article_compound_dictionary:
                    article_compound_dictionary[compound].append(list(article.get_all_attributes()))
                else:
                    article_compound_dictionary[compound] = []
                    article_compound_dictionary[compound].append(list(article.get_all_attributes()))
        disease_count_dict = {}
        value = article_compound_dictionary[compound]
        for attributes in value:
            for disease in disease_dictionary:
                if disease in attributes:
                    if disease not in disease_count_dict:
                        disease_count_dict[disease] = 1
                    else:
                        disease_count_dict[disease] += 1
        Bittergourd_compound_disease_JSON["children"].append({"name": compound, "children":[]})
        for disease in disease_count_dict:
            Bittergourd_compound_disease_JSON["children"][counter]['children'].append({"name":disease,"size":disease_count_dict[disease]})
        counter+=1
    with open("data/Bittergourd_compound_disease.json", "w") as outfile2:
        json.dump(Bittergourd_compound_disease_JSON, outfile2)
        outfile.close()

main()