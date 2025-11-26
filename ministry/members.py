class Member:
    def __init__(self,name,id,birth,father,mother,nat,image,role,level,isleader):
        self.name=name
        self.id=id
        self.birth=birth
        self.father=father
        self.mother=mother
        self.nat=nat
        self.image=image
        self.role=role
        self.level=level
        self.isleader=isleader


    def __str__(self):
        return f"name:  {self.name }  , id: { self.id } , role: {  self.role}, isleader:  {self.isleader  }"    

        
