from sqlalchemy import *
from sqlalchemy.sql import *


def get_bd(budget):
    bdgt = budget
    data= []
    engine = create_engine('sqlite:///base.sql', echo=True)
    connection = engine.connect()
    for row in connection.execute("select * from Offre where prix_offre <= " + bdgt) :
        data.append(row)

    connection.close()

    return data
