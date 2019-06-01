class Option:
    #boolean = False

    def __init__(self, boolean, url_input, combination_name):
        self.__boolean = boolean
        self.__url_input = url_input
        self.__combination_name = combination_name

    def set_boolean(self, boolean):
        self.__boolean = boolean

    def get_boolean(self):
        return self.__boolean

    def set_data_url(self, url_input):
        self.__url_input = url_input

    def get_data_url(self):
        return self.__url_input

    def set_combination_name(self, combination_name):
        self.__combination_name = combination_name

    def get_combination_name(self):
        return self.__combination_name
