from flask import Flask, render_template, request, jsonify
from option import Option
from Article_class import Article
#globaal een object aanmaken om de optie van de gebruiker te onthouden van de
optie = Option(True, "https://gist.githubusercontent.com/ArielKomen/99076738a5a169cfeab5f9d2f27c0a13/raw/07d3cc77be38647c0048e1ef9c2ab695e7fc5c16/data_bittergourd_compound_disease.json", "")
#optie = option.set_boolean(False)

"""
code voor bittergourd_disease_compound
https://gist.githubusercontent.com/ArielKomen/c35cdb735fa770542cd6494c2fdc179e/raw/89135f903086768c9f2e3e0bfb7ec23f28af55ab/data_bittergourd_disease_compound.json

code voor bittergourd_compound_disease
https://gist.githubusercontent.com/ArielKomen/99076738a5a169cfeab5f9d2f27c0a13/raw/07d3cc77be38647c0048e1ef9c2ab695e7fc5c16/data_bittergourd_compound_disease.json

"""

app = Flask(__name__)

@app.route('/webpage.html', methods=['GET'])
def webpage_html():
    article_list = article_maker()
    # maakt een lijst van article objecten
    table_input = getTextData(article_list)

    combinatie_lijst = maak_combinatie_lijst(optie)
    html_lijst = zooi(combinatie_lijst)
    return render_template('webpage.html', input=html_lijst, input_b=table_input, data_url=optie.get_data_url())


@app.route('/Help.html',methods=['GET'])
def help_html():
    return render_template('Help.html')


@app.route('/Disclaimer.html',methods=['GET'])
def disc_html():
    return render_template('Disclaimer.html')


@app.route('/About.html',methods=['GET'])
def about_html():
    return render_template('About.html')



@app.route('/output', methods = ['POST','GET'])
def output():
    if request.method == 'GET':
        combination_name = request.args['combination_name']
        combination_value = request.args['combination_value']
        #print(combination_name, combination_value)
        optie.set_combination_name(combination_name)

        article_list = article_maker()
        # maakt een lijst van article objecten
        table_input = getTextData(article_list)

        combinatie_lijst = maak_combinatie_lijst(optie)
        html_lijst = zooi(combinatie_lijst)
        return render_template('webpage.html', input=html_lijst, input_b=table_input, data_url=optie.get_data_url())

@app.route('/export', methods=['GET'])
def export():
    if request.method == 'GET':

        combinatie_lijst = maak_combinatie_lijst(optie)
        html_lijst = zooi(combinatie_lijst)

        article_list = article_maker()
        # maakt een lijst van article objecten
        table_input = getTextData(article_list)
        # article_list is de lijst van article objecten die gevisualiseerd wordt,
        # table_input zijn de gegevens die uit object articles worden gehaald
        selection = str(request.args.getlist('Selected'))
        print(selection)
        return render_template('webpage.html', input=html_lijst, input_b=table_input, data_url=optie.get_data_url())


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':

        #een lijst van compounds is true
        #een lijst van diseases is false
        user_answer = request.form['options']
        if user_answer == "Compound":
            optie.set_boolean(True)
            optie.set_data_url("https://gist.githubusercontent.com/ArielKomen/99076738a5a169cfeab5f9d2f27c0a13/raw/07d3cc77be38647c0048e1ef9c2ab695e7fc5c16/data_bittergourd_compound_disease.json")
        else:
            optie.set_boolean(False)
            optie.set_data_url("https://gist.githubusercontent.com/ArielKomen/c35cdb735fa770542cd6494c2fdc179e/raw/89135f903086768c9f2e3e0bfb7ec23f28af55ab/data_bittergourd_disease_compound.json")
        #print(user_answer)
        print(optie.get_boolean())
        article_list = article_maker()
        # maakt een lijst van article objecten
        table_input = getTextData(article_list)

        combinatie_lijst = maak_combinatie_lijst(optie)
        html_lijst = zooi(combinatie_lijst)
        return render_template('webpage.html', input=html_lijst, input_b=table_input, data_url=optie.get_data_url())
    if request.method == 'GET':
        article_list = article_maker()
        # maakt een lijst van article objecten
        table_input = getTextData(article_list)

        combinatie_lijst = maak_combinatie_lijst(optie)
        html_lijst = zooi(combinatie_lijst)
        return render_template('webpage.html', input=html_lijst, input_b=table_input, data_url=optie.get_data_url())

def maak_combinatie_lijst(optie):
    compound_data = "data/compound lijst"
    ziekte_data = "data/ziekte lijst"


    if optie.get_boolean() == False:
        combinatie_lijst = make_compound_ziekte_combinatie_lijst(compound_data, ziekte_data)
    else:
        combinatie_lijst = make_ziekte_compound_combinatie_lijst(compound_data, ziekte_data)

    return combinatie_lijst

def make_compound_ziekte_combinatie_lijst(compound_data, ziekte_data):
    # in deze functie er voor zorgen dat er een combinatielijst gemaakt wordt tussen ziekte en compound
    combinatie_lijst = []
    combinatie_dict = {}
    ziekte_lijst = make_ziekte_lijst(ziekte_data)
    compound_lijst = make_compound_lijst(compound_data)

    for ziekte in ziekte_lijst[0:]:
        combinatie_dict[ziekte] = compound_lijst[0:]
        combinatie_lijst.append(combinatie_dict)
        combinatie_dict = {}

    return combinatie_lijst

def make_ziekte_compound_combinatie_lijst(compound_data, ziekte_data):
    # in deze functie er voor zorgen dat er een combinatielijst gemaakt wordt tussen compound en ziekte
    combinatie_lijst = []
    combinatie_dict = {}
    ziekte_lijst = make_ziekte_lijst(ziekte_data)
    compound_lijst = make_compound_lijst(compound_data)
    for compound in compound_lijst[0:]:
        combinatie_dict[compound] = ziekte_lijst[0:]
        combinatie_lijst.append(combinatie_dict)
        combinatie_dict = {}

    return combinatie_lijst

def make_ziekte_lijst(ziekte_data):
    ziekte_lijst = []
    for regel in open(ziekte_data):
        regel = regel.strip()
        if regel != "":
            ziekte_lijst.append(regel)

    return ziekte_lijst

def make_compound_lijst(compound_data):
    compound_lijst = []
    for regel in open(compound_data):
        regel = regel.strip()
        if regel != "":
            compound_lijst.append(regel)

    return compound_lijst

def zooi(combinatie_lijst):
    html_lijst = []
    opteller = 0
    speciale_opteller = 0

    # html_lijst.append('<ul>')
    html_lijst.append('<div class="btn-group-vertical">')
    for item in combinatie_lijst:

        html_lijst.append('<button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#Flask_applicatie_'+str(opteller)+ '" aria-expanded="false" aria-controls="Flask_applicatie">' + list(item.items())[0][0] + "</button>")
        html_lijst.append('<div class ="collapse" id="Flask_applicatie_'+str(opteller)+'">')

        html_lijst.append('<div class="card card-body">')
        html_lijst.append('<div class="btn-group-vertical">')
        for lijst in item.values():
            for woord in lijst:
                #<form action="/input_a" method="POST">
                #html_lijst.append('<input type="submit" name="output" value="output_'+str(speciale_opteller)+'" >')
                #html_lijst.append('<input type="button" name="ouput_'+str(speciale_opteller)+'" >')
                html_lijst.append('<form action="/output" method="GET">')
                #html_lijst.append('<input type="text" name="'+list(item.items())[0][0]+'_'+woord+' value='+str(speciale_opteller)+'">')
                html_lijst.append('<div class="hidden">')
                aapje = list(item.items())[0][0]+'_'+woord
                html_lijst.append('<input type="text" name="combination_name" value="' + aapje + '">')
                nootje = str(speciale_opteller)
                html_lijst.append('<input type="text" name="combination_value" value="' + nootje + '">')
                html_lijst.append('</div>')
                html_lijst.append('<button type="submit" class="btn btn-secondary" value="'+list(item.items())[0][0]+'_'+woord+'">'+woord+'</button>')
                html_lijst.append('</form>')
                #html_lijst.append(woord)
                #html_lijst.append('</li>')
                speciale_opteller += 1
        speciale_opteller = 0
        html_lijst.append('</div>')
        html_lijst.append('</div>')
        html_lijst.append('</div>')
        opteller += 1
    html_lijst.append('</div>')
    #for item in html_lijst:
        #print(item)
    return html_lijst

def article_maker():
    article_list = []
    if optie.get_combination_name() == "":
        with open("/home/cole/Documents/course_8/weektaken/flask_applicatie/data/export bitter gourd en ziektes") as bittergourd_disease:
            for line in bittergourd_disease:
                #ervoor zorgen dat de ziekte en andere dingen worden opgeslagen in de article class.
                splitline = line.rstrip("\n").split(";")
                disease = splitline[3].replace("\"", "").split("AND")
                disease = disease[0][:-1] + "_" + disease[1][1:]
                lijst = disease.split("_")

                article_list.append(Article(splitline[4], splitline[1], splitline[0], lijst[0], lijst[1]))
    else:
        print(optie.get_combination_name())
        with open("/home/cole/Documents/course_8/weektaken/textmining applicatie/data/export ziektes en compounds") as bittergourd_disease:
            for line in bittergourd_disease:
                splitline = line.rstrip("\n").split(";")
                disease = splitline[3].replace("\"", "").split("AND")
                # een lijst van compounds is true
                # een lijst van diseases is false
                # ik wil eerst een ziekte, en dan een compound
                if optie.get_boolean() == False:
                    disease = disease[0][:-1] + "_" + disease[1][1:]
                else:
                    disease = disease[1][1:] + "_" + disease[0][:-1]
                #alles dat de goede naam heeft zetten in de article lijst om  te laten zien.


                #lijst[1] zijn de compounds en lijst[0] de ziektes
                if disease == optie.get_combination_name():
                    lijst = disease.split("_")
                    article_list.append(Article(splitline[4], splitline[1], splitline[0], lijst[0], lijst[1]))

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
