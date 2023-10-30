class Demo():

    def __init__(self, string):
        self.string = string

    def __sub__(self, other):
        return self.string + " " + other
    
    def __repr__(self):
        return 'Object: %s'%(self.string)
    
if __name__ == "__main__":
    string = Demo("Hello")
    print(string)
    print(string - "World!!")