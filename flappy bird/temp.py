class test():

    def __init__(self):
        self.x = 100

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x


t1 = test()
