from flask import Flask, render_template, request
from Article_class import Article
app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    article_list = article_maker()  #maakt een lijst van article objecten
    table_input = getTextData(article_list)     #article_list is de lijst van article objecten die gevisualiseerd wordt, table_input zijn de gegevens die uit object articles worden gehaald
    return render_template('table_logic.html', input=table_input)

@app.route('/export', methods=['GET'])
def export():
    article_list = article_maker()  # maakt een lijst van article objecten
    table_input = getTextData(
        article_list)  # article_list is de lijst van article objecten die gevisualiseerd wordt, table_input zijn de gegevens die uit object articles worden gehaald

    if request.method == 'GET':
        #selection = request.args['Selected']
        selection = str(request.args.getlist('Selected'))
        print(selection)
        return render_template('table_logic.html', input=table_input)

def article_maker():
    article_list = []
    with open("/home/jungho/Documenten/BIN-2/Blok8/Course8Applicatie-/data/export bitter gourd en ziektes") as bittergourd_disease:
        for line in bittergourd_disease:
            strippedline = line.rstrip("\n")
            splitline = strippedline.split(";")
            disease = splitline[3].split("AND")
            disease = disease[0].rstrip(" ")
            article_list.append(Article(splitline[4], splitline[1], splitline[0], disease, "Na"))
    return article_list


def getTextData(article_list):
    data_list = []
    for i in article_list:
        data_sublist = []
        pmid = i.get_pmid(i)
        title = i.get_title()
        date = i.get_date()
        hyperlink = 'https://www.ncbi.nlm.nih.gov/pubmed/' + pmid
        data_sublist.append(title)
        data_sublist.append(date)
        data_sublist.append(hyperlink)
        data_list.append(data_sublist)
    #print(data_list)
    return data_list


if __name__ == '__main__':
    app.run()