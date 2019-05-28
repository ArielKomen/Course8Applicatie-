import mysql.connector
from Bio import Entrez
from Bio import Medline
from Article_class import Article
def main():
    article_list, disease_dictionary = article_maker()
    db_filler(article_list, disease_dictionary)
def article_maker():
    article_list = []
    unique_disease = []
    disease_dictionary = {}
    counter = 0
    with open("/home/stephan/PycharmProjects/Course8Applicatie-/data/export bitter gourd en ziektes") as bittergourd_disease:
        for line in bittergourd_disease:
            strippedline = line.rstrip("\n")
            splitline = strippedline.split(";")
            disease = splitline[3].split("AND")
            disease = disease[0].rstrip(" ")
            article_list.append(Article(splitline[4], splitline[1], splitline[0], disease, "Na"))
            if disease not in unique_disease:
                unique_disease.append(disease)
    for i in unique_disease:
        disease_dictionary[i] = counter
        counter+=1
    print(disease_dictionary)
    return article_list, disease_dictionary
def db_filler(article_list, disease_dictionary):

    cnx = mysql.connector.connect(host = "hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com", user = 'owe7_pg8@hannl-hlo-bioinformatica-mysqlsrv', password = 'blaat1234', database = 'owe7_pg8')
    cursor = cnx.cursor()
    for object in article_list:
        query_insert = "insert into owe7_pg8.article values(%s, %s, %s, %s, %s)"
        values = (int(object.get_pmid(object)), object.get_date(), object.get_title(), 255, disease_dictionary.get(object.get_ziekte(object)))
        print(values)
        #cursor.execute(query_insert, values)
main()