# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 00:23:46 2019

@author: gblanco
"""
import pandas as pd
#import json #hay una función para guardar a JSON por si se tercia
import bs4
import re
from urllib.request import urlopen

class elecciones_ucm():
    def __init__(self, datos, URLs, URL):
        self.URL = URL
        self.datos = datos
        self.URLs = URLs
        self.puertas_cerradas=[]
        self.puertas_duplicadas=[]
        self.fallidos_1=[]
        self.fallidos_2=[]
        
    def conexion(self, puerta):
        print('conectando con la puerta...' + str(puerta))
        return bs4.BeautifulSoup(urlopen(self.URL + str(puerta)), 'html.parser')
    @staticmethod
    def comprobacion(soup, nombre):
        results = soup.find_all(string=re.compile('.*{0}.*'.format(nombre)), recursive=True)
        if len(results)>0:
            results = True
            print('hit ' + nombre)
        else:
            results = False
        return results
    
    def parseo_a_json(self, puerta):
        df = pd.read_html(self.URL + puerta, index_col=0)
        return df[0].to_json(), df[1].to_json()
    
    def scrap(self):
        for puerta in range(1000):
            soup = self.conexion(puerta)
            cuenta = 0
            for nombre in self.URLs.loc[:,'mesa_con_acento']:
                if self.comprobacion(soup, nombre):
                    cuenta += 1
                    for sector in range(1,6):
                        for centro in range(0,len(self.datos[sector]['centros'])):
                            nombre2 = str(self.URLs.loc[self.URLs.iloc[:,0]==self.datos[sector]['centros'][centro]['mesa'],'mesa_con_acento'].values[0])
                            if nombre2==nombre:
                                self.datos[sector]['centros'][centro]['votos'] ,self.datos[sector]['centros'][centro]['recuento'] = self.parseo_a_json(str(puerta))
            if cuenta==0:
                self.puertas_cerradas.append(puerta)
            elif cuenta>1:
                self.puertas_duplicadas.append(puerta)
                print(nombre)
            if puerta==999:
                for sector in range(1,6):
                    for centro in range(0,len(self.datos[sector]['centros'])):
                        try:
                            self.datos[sector]['centros'][centro]['recuento']
                        except:
                            self.fallidos_1.append([sector,centro])
                        try:
                            self.datos[sector]['centros'][centro]['votos']
                        except:
                            self.fallidos_2.append([sector,centro])                
        
        print('Resumen de ejecución:')
        if not self.fallidos_1==self.fallidos_2:
            print('Discrepancia, algun puerta no tenia dos tablas')
        else:
            for sector in range(1,6):
                for centro in range(0,len(self.datos[sector]['centros'])):
                    try:
                        self.datos[sector]['centros'][centro]['votos']
                    except:
                        print('No encontrado -> ' + self.datos[sector]['centros'][centro]['mesa'])
        


def extracc_brutos(datos):
    salida=[dict(datos[0])]
    for sector in range(1,6):
        centros = []
        for centro in range(0,len(datos[sector]['Mesas']),2):
            centros.append((dict({'centro':datos[sector]['Mesas'][centro+1],'mesa':datos[sector]['Mesas'][centro]})))
        salida.append(dict({"sector":datos[sector]['sector'],"centros":centros}))
    return(salida)

#prueba=json.dumps(salida)
    
    
    
# DATOS   

BRUTOdatos2015Vuelta1=[{"Elecciones a Rector 2015 - Primera vuelta":
"Resultados provisionales"},
{"sector":"Profesores Doctores de los cuerpos docentes universitarios",
"Mesas":
["Bellas Artes - PD",
"Bellas Artes",
"CC. Biologicas - PD",
"Ciencias Biologicas",
"CC. de la Documentacion - PD",
"Ciencias de la Documentacion",
"CC. de la Informacion - PD",
"Ciencias de la Informacion",
"CC. Economicas y Empresariales - PD",
"Ciencias Economicas y Empresariales",
"CC. Fisicas - PD",
"Ciencias Fisicas",
"CC. Geologicas - PD",
"Ciencias Geologicas",
"CC. Matematicas - PD",
"Ciencias Matematicas",
"CC. Politicas y Sociologia - PD",
"Ciencias Politicas y Sociologia",
"CC. Quimicas - PD",
"Ciencias Quimicas",
"Comercio y Turismo - PD",
"Comercio y Turismo",
"Derecho - PD",
"Derecho",
"Educacion - PD",
"Educacion – Centro de Formacion del Profesorado",
"Enfermeria, Fisioterapia y Podologia - PD",
"Enfermeria, Fisioterapia y Podologia",
"Estudios Estadisticos - PD",
"Estudios Estadisticos",
"Farmacia - PD",
"Farmacia",
"Filologia - PD",
"Filologia",
"Filosofia - PD",
"Filosofia",
"Geografia e Historia - PD",
"Geografia e Historia",
"Informatica - PD",
"Informatica",
"Medicina - PD",
"Medicina",
"Odontologia - PD",
"Odontologia",
"optica y Optometria - PD",
"optica y Optometria",
"Psicologia - PD",
"Psicologia",
"Trabajo Social - PD",
"Trabajo Social",
"Veterinaria - PD",
"Veterinaria"
]
},
{"sector":"Resto de Personal docente e investigador con dedicacion completa",
"Mesas":["CC. Quimicas - PDI-DC",
"Ciencias Quimicas",
"Filosofia - PDI-DC",
"Filosofia",
"Odontologia - PDI-DC",
"Odontologia",
"Psicologia - PDI-DC",
"Psicologia",
"Rectorado - PDI-DC",
"Rectorado"
]
},
{"sector":"Resto de Personal docente e investigador con dedicacion parcial",
"Mesas":["CC. Quimicas - PDI-DP",
"Ciencias Quimicas",
"Filosofia - PDI-DP",
"Filosofia",
"Odontologia - PDI-DP-1",
"Odontologia",
"Odontologia - PDI-DP-2",
"Odontologia",
"Psicologia - PDI-DP",
"Psicologia",
"Rectorado - PDI-DP",
"Rectorado"
]
},
{"sector":"Estudiantes",
"Mesas":["Bellas Artes - EST",
"Bellas Artes",
"CC. Biologicas - EST",
"Ciencias Biologicas",
"CC. de la Documentacion - EST",
"Ciencias de la Documentacion",
"CC. de la Informacion - EST-1",
"Ciencias de la Informacion",
"CC. de la Informacion - EST-2",
"Ciencias de la Informacion",
"CC. Economicas y Empresariales - EST",
"Ciencias Economicas y Empresariales",
"CC. Fisicas - EST",
"Ciencias Fisicas",
"CC. Geologicas - EST",
"Ciencias Geologicas",
"CC. Matematicas - EST",
"Ciencias Matematicas",
"CC. Politicas y Sociologia - EST",
"Ciencias Politicas y Sociologia",
"CC. Quimicas - EST",
"Ciencias Quimicas",
"Comercio y Turismo - EST",
"Comercio y Turismo",
"Derecho - EST-1",
"Derecho",
"Derecho - EST-2",
"Derecho",
"Educacion - EST-1",
"Educacion – Centro de Formacion del Profesorado",
"Educacion - EST-2",
"Educacion – Centro de Formacion del Profesorado",
"Enfermeria, Fisioterapia y Podologia - EST",
"Enfermeria, Fisioterapia y Podologia",
"Estudios Estadisticos - EST",
"Estudios Estadisticos",
"Farmacia - EST",
"Farmacia",
"Filologia - EST",
"Filologia",
"Filosofia - EST",
"Filosofia",
"Geografia e Historia - EST",
"Geografia e Historia",
"Informatica - EST",
"Informatica",
"Medicina - EST",
"Medicina",
"Odontologia - EST",
"Odontologia",
"optica y Optometria - EST",
"optica y Optometria",
"Psicologia - EST",
"Psicologia",
"Trabajo Social - EST",
"Trabajo Social",
"Veterinaria - EST",
"Veterinaria",
"Felipe II (Aranjuez) - EST",
"Centro Felipe II de Aranjuez",
"Maria Cristina (El Escorial) - EST",
"Centro Adscrito Maria Cristina de El Escorial",
"Rectorado - EST-1",
"Rectorado",
"Rectorado - EST-2",
"Rectorado"
]
},
{"sector":"Personal de Administracion y Servicios",
"Mesas":["CC. Quimicas - PAS-1",
"Ciencias Quimicas",
"CC. Quimicas - PAS-2",
"Ciencias Quimicas",
"Filosofia - PAS-1",
"Filosofia",
"Filosofia - PAS-2",
"Filosofia",
"Odontologia - PAS-1",
"Odontologia",
"Odontologia - PAS-2",
"Odontologia",
"Odontologia - PAS-3",
"Odontologia",
"Psicologia - PAS",
"Psicologia",
"Rectorado - PAS-1",
"Rectorado",
"Rectorado - PAS-2",
"Rectorado"
]
}
]


datos2015Vuelta1 = [{"Elecciones a Rector 2015 - Primera vuelta": "Resultados provisionales"}, {"sector": "Profesores Doctores de los cuerpos docentes universitarios", "centros": [{"centro": "Bellas Artes", "mesa": "Bellas Artes - PD"}, {"centro": "Ciencias Biologicas", "mesa": "CC. Biologicas - PD"}, {"centro": "Ciencias de la Documentacion", "mesa": "CC. de la Documentacion - PD"}, {"centro": "Ciencias de la Informacion", "mesa": "CC. de la Informacion - PD"}, {"centro": "Ciencias Economicas y Empresariales", "mesa": "CC. Economicas y Empresariales - PD"}, {"centro": "Ciencias Fisicas", "mesa": "CC. Fisicas - PD"}, {"centro": "Ciencias Geologicas", "mesa": "CC. Geologicas - PD"}, {"centro": "Ciencias Matematicas", "mesa": "CC. Matematicas - PD"}, {"centro": "Ciencias Politicas y Sociologia", "mesa": "CC. Politicas y Sociologia - PD"}, {"centro": "Ciencias Quimicas", "mesa": "CC. Quimicas - PD"}, {"centro": "Comercio y Turismo", "mesa": "Comercio y Turismo - PD"}, {"centro": "Derecho", "mesa": "Derecho - PD"}, {"centro": "Educacion \u2013 Centro de Formacion del Profesorado", "mesa": "Educacion - PD"}, {"centro": "Enfermeria, Fisioterapia y Podologia", "mesa": "Enfermeria, Fisioterapia y Podologia - PD"}, {"centro": "Estudios Estadisticos", "mesa": "Estudios Estadisticos - PD"}, {"centro": "Farmacia", "mesa": "Farmacia - PD"}, {"centro": "Filologia", "mesa": "Filologia - PD"}, {"centro": "Filosofia", "mesa": "Filosofia - PD"}, {"centro": "Geografia e Historia", "mesa": "Geografia e Historia - PD"}, {"centro": "Informatica", "mesa": "Informatica - PD"}, {"centro": "Medicina", "mesa": "Medicina - PD"}, {"centro": "Odontologia", "mesa": "Odontologia - PD"}, {"centro": "optica y Optometria", "mesa": "optica y Optometria - PD"}, {"centro": "Psicologia", "mesa": "Psicologia - PD"}, {"centro": "Trabajo Social", "mesa": "Trabajo Social - PD"}, {"centro": "Veterinaria", "mesa": "Veterinaria - PD"}]}, {"sector": "Resto de Personal docente e investigador con dedicacion completa", "centros": [{"centro": "Ciencias Quimicas", "mesa": "CC. Quimicas - PDI-DC"}, {"centro": "Filosofia", "mesa": "Filosofia - PDI-DC"}, {"centro": "Odontologia", "mesa": "Odontologia - PDI-DC"}, {"centro": "Psicologia", "mesa": "Psicologia - PDI-DC"}, {"centro": "Rectorado", "mesa": "Rectorado - PDI-DC"}]}, {"sector": "Resto de Personal docente e investigador con dedicacion parcial", "centros": [{"centro": "Ciencias Quimicas", "mesa": "CC. Quimicas - PDI-DP"}, {"centro": "Filosofia", "mesa": "Filosofia - PDI-DP"}, {"centro": "Odontologia", "mesa": "Odontologia - PDI-DP-1"}, {"centro": "Odontologia", "mesa": "Odontologia - PDI-DP-2"}, {"centro": "Psicologia", "mesa": "Psicologia - PDI-DP"}, {"centro": "Rectorado", "mesa": "Rectorado - PDI-DP"}]}, {"sector": "Estudiantes", "centros": [{"centro": "Bellas Artes", "mesa": "Bellas Artes - EST"}, {"centro": "Ciencias Biologicas", "mesa": "CC. Biologicas - EST"}, {"centro": "Ciencias de la Documentacion", "mesa": "CC. de la Documentacion - EST"}, {"centro": "Ciencias de la Informacion", "mesa": "CC. de la Informacion - EST-1"}, {"centro": "Ciencias de la Informacion", "mesa": "CC. de la Informacion - EST-2"}, {"centro": "Ciencias Economicas y Empresariales", "mesa": "CC. Economicas y Empresariales - EST"}, {"centro": "Ciencias Fisicas", "mesa": "CC. Fisicas - EST"}, {"centro": "Ciencias Geologicas", "mesa": "CC. Geologicas - EST"}, {"centro": "Ciencias Matematicas", "mesa": "CC. Matematicas - EST"}, {"centro": "Ciencias Politicas y Sociologia", "mesa": "CC. Politicas y Sociologia - EST"}, {"centro": "Ciencias Quimicas", "mesa": "CC. Quimicas - EST"}, {"centro": "Comercio y Turismo", "mesa": "Comercio y Turismo - EST"}, {"centro": "Derecho", "mesa": "Derecho - EST-1"}, {"centro": "Derecho", "mesa": "Derecho - EST-2"}, {"centro": "Educacion \u2013 Centro de Formacion del Profesorado", "mesa": "Educacion - EST-1"}, {"centro": "Educacion \u2013 Centro de Formacion del Profesorado", "mesa": "Educacion - EST-2"}, {"centro": "Enfermeria, Fisioterapia y Podologia", "mesa": "Enfermeria, Fisioterapia y Podologia - EST"}, {"centro": "Estudios Estadisticos", "mesa": "Estudios Estadisticos - EST"}, {"centro": "Farmacia", "mesa": "Farmacia - EST"}, {"centro": "Filologia", "mesa": "Filologia - EST"}, {"centro": "Filosofia", "mesa": "Filosofia - EST"}, {"centro": "Geografia e Historia", "mesa": "Geografia e Historia - EST"}, {"centro": "Informatica", "mesa": "Informatica - EST"}, {"centro": "Medicina", "mesa": "Medicina - EST"}, {"centro": "Odontologia", "mesa": "Odontologia - EST"}, {"centro": "optica y Optometria", "mesa": "optica y Optometria - EST"}, {"centro": "Psicologia", "mesa": "Psicologia - EST"}, {"centro": "Trabajo Social", "mesa": "Trabajo Social - EST"}, {"centro": "Veterinaria", "mesa": "Veterinaria - EST"}, {"centro": "Centro Felipe II de Aranjuez", "mesa": "Felipe II (Aranjuez) - EST"}, {"centro": "Centro Adscrito Maria Cristina de El Escorial", "mesa": "Maria Cristina (El Escorial) - EST"}, {"centro": "Rectorado", "mesa": "Rectorado - EST-1"}, {"centro": "Rectorado", "mesa": "Rectorado - EST-2"}]}, {"sector": "Personal de Administracion y Servicios", "centros": [{"centro": "Ciencias Quimicas", "mesa": "CC. Quimicas - PAS-1"}, {"centro": "Ciencias Quimicas", "mesa": "CC. Quimicas - PAS-2"}, {"centro": "Filosofia", "mesa": "Filosofia - PAS-1"}, {"centro": "Filosofia", "mesa": "Filosofia - PAS-2"}, {"centro": "Odontologia", "mesa": "Odontologia - PAS-1"}, {"centro": "Odontologia", "mesa": "Odontologia - PAS-2"}, {"centro": "Odontologia", "mesa": "Odontologia - PAS-3"}, {"centro": "Psicologia", "mesa": "Psicologia - PAS"}, {"centro": "Rectorado", "mesa": "Rectorado - PAS-1"}, {"centro": "Rectorado", "mesa": "Rectorado - PAS-2"}]}]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    