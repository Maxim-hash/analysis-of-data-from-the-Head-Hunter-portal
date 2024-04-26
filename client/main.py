from structural.client import App_Controller

class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age


if __name__ == "__main__":
    #obj = MyClass("John", 30)
    #obj2 = MyClass("Anna", 100)
    #temp = list(obj.__dict__.values())
    #print(':'.join(map(str, list(obj.__dict__.values())[1:])) + ":" +':'.join(map(str, obj2.__dict__.values())))
    app = App_Controller()
    app.run() 