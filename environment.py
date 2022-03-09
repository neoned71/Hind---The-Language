class Environment:
    def __init__(self,enclosing=None):
        self.values={}
        self.environment:Environment = enclosing


    def define(self,name:str,value:object)->None:
        # if (self.environment is not None):
        #     self.environment.define(name,value)
        #     return
        # print("Dictionary",self.values.keys())
        self.values[name] = value
        
    

    def assign(self,name:str,value:object)->None:
        # print("Dictionary",self.values.keys())
        if(name in self.values.keys()):
            
            self.values[name] = value
            return
        else:
            if (self.environment is not None):
                self.environment.assign(name,value)
                return

        raise Exception("Undefined variable: "+name)

    def get(self,name:str)->object:
        
        if(name in self.values.keys()):
            return self.values[name]
        else:
            if (self.environment is not None):
                return self.environment.get(name)

        raise Exception("Accessing undefined variable: "+name)

    def __str__(self) -> str:
        return "Keys:"+str(self.values.keys())+"\nValues:"+str(self.values.values())