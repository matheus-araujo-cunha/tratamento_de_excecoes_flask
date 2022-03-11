from os import getenv
import ujson as json
from app.services import create_user_id
from app.services import validate_fields

class User:
    DATABASE_FILEPATH = getenv("DATABASE_FILEPATH")

    def __init__(self,name:str,email:str) -> None:
        fields = validate_fields(name,email) 
        self.name = fields["name"]
        self.email = fields["email"]
        self.id = create_user_id()
    
    @classmethod
    def read_database(cls):
        try:
            with open(cls.DATABASE_FILEPATH,"r") as database_reader:
                data = json.load(database_reader)
                return data
        except (FileNotFoundError,ValueError):
            return cls.create_database()   

    @classmethod
    def create_database(cls):
        with open(cls.DATABASE_FILEPATH,"w") as database_writer:   
            json.dump([],database_writer,indent=2)
            return []    


    def add_to_database(self,data):
        database = self.read_database()
        with open(self.DATABASE_FILEPATH,"w") as database_writer:
            database.append(data)
            json.dump(database,database_writer,indent=2)
        return data            