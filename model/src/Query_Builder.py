database_tables= {
    "Vacansies" : {
        "ID" : "INTEGER PRIMARY KEY, " ,
        "name" : "VARCHAR(50) NOT NULL, ",
        "publishied_at" : "VARCHAR(50) NOT NULL, ",
        "schedule" : "VARCHAR(50) NOT NULL, ",
	    "prof_roles" : "VARCHAR(50) NOT NULL, ",
        "exp" : "VARCHAR(50) NOT NULL, ",
        "empoyment" : "VARCHAR(50) NOT NULL, ",
        "area_id" : "INTEGER NOT NULL, ",
        "employers_id" : "VARCHAR(50) NOT NULL,",
        "requirement" :  "VARCHAR(50) NOT NULL, ",
        "responsobility" : "VARCHAR(50) NOT NULL"
        },
    "Areas" : {
        "ID" : "INTEGER PRIMARY KEY, ",
        "name" : "VARCHAR(50) NOT NULL"
        },
    "Salary" : {
        "id_vacancy" : "INTEGER PRIMARY KEY, ",
	    "s_from" : "INTEGER, ",
	    "s_to" : "INTEGER, ",
        "currency" : "VARCHAR(50) NOT NULL, ",
	    "gross" : "BOOLEAN NOT NULL"
        },
    "Employer" : {
        "id_emp" : "INTEGER PRIMARY KEY, ",
        "name" : "VARCHAR(50) NOT NULL, ",
        "accredited_it_empoloyer" : "BOOLEAN NOT NULL, ",
        "trusted"  : "BOOLEAN NOT NULL"
        }
}



class Query_Builder:
    def __init__(self) -> None:
        self.query = {}
        
    def create(self):
        self.query.append("CREATE ")
        return self

    def table(self, *table_name):
        self.query.append(f"TABLE {', '.join(table_name)}")
        return self
    
    def select(self, *args):
        self.query.append(f"SELECT {', '.join(args)}")
        return self
    
    def _from(self):
        self.query.append(" FROM ")
        return self
    
    def drop(self,table_name):
        self.query.append(f"DROP ")
        return self

    def build(self):
        return ''.join(self.query)


a = Query_Builder()
for i in database_tables:
    for j in database_tables[i]:
        a.select(j)
    

