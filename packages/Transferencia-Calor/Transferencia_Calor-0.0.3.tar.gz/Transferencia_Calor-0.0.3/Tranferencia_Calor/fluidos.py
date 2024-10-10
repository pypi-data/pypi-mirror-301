import pandas as pd
from thermo.chemical import Chemical 

fluidos =['methane', 'ethane', 'propane', 'butane', 'isopentane', 
                 'hexane', 'heptane', 'octane', 'nonane', 'decane']

def  fluidos_db():
    print("Lista de fluidos de hidrocarburos disponible: \n")
    for i, fluido in enumerate (fluidos, 1):
        print(f"{i}.- {fluido}")
fluidos_db()


def propiedades_fluidos():
    prop_fluidos = []
    for prop in fluidos:
        chemical = Chemical(prop)
        prop_fluidos.append({
            "Fluido_Nombre": prop.title(),
            "Formula": chemical.formula,
            "Tc (K)": chemical.Tc,
            "Pc (Pa)": chemical.Pc,
            "PM (g/mol)":chemical.MW,
            "Vc ":chemical.Vc
        })
    df=pd.DataFrame(prop_fluidos)
    print("Las propiedades de los fludios son las siguientes: \n")
    print(df)
propiedades_fluidos()
    

 



