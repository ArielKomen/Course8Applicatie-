# in deze methode wordt de class aricle gemaakt
class Article:
    def __init__(self, title, date, pmid, ziekte, compound):
        self.__title = title
        self.__date = date
        self.__pmid = pmid
        self.__ziekte = ziekte
        self.__compound = compound

    def set_title(self, title):
        self.__title = title
    def set_date(self, date):
        self.__date = date
    def set_pmid(self, pmid):
        self.__pmid = pmid
    def set_ziekte(self, ziekte):
        self.__ziekte = ziekte
    def set_compound(self, compound):
        self.__compound = compound

    def get_title(self):
        return self.__title
    def get_date(self):
        return self.__date
    def get_pmid(self):
        return self.__pmid
    def get_ziekte(self):
        return self.__ziekte
    def get_compound(self):
        return self.__compound
    def get_all_attributes(self):
        return self.__title, self.__date, self.__pmid, self.__ziekte, self.__compound
