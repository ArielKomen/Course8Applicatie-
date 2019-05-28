class Option:
    #boolean = False

    def __init__(self, boolean):
        self.__boolean = boolean

    def set_boolean(self, boolean):
        self.__boolean = boolean

    def get_boolean(self):
        return self.__boolean
