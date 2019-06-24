# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 22:11:52 2019

@author: gblanco
"""
import pandas as pd
import datos_rector
import json

import gc
gc.collect()

datos = datos_rector.datos2015Vuelta1
URLs = pd.read_csv('d:/Cursos/rector/URLs.csv',delimiter=";", encoding="ANSI")
URL = 'https://www.ucm.es/elecciones/rector-2015-vuelta1/mesas/?mid='

Rector2015V1 = datos_rector.elecciones_ucm(datos, URLs, URL)
Rector2015V1.scrap()

#Fallan dos centros or salgún motivo. Arreglo manual
Rector2015V1.datos[4]['centros'][29]['votos'] ,Rector2015V1.datos[4]['centros'][29]['recuento'] = Rector2015V1.parseo_a_json(str(361))
Rector2015V1.datos[4]['centros'][30]['votos'] ,Rector2015V1.datos[4]['centros'][30]['recuento'] = Rector2015V1.parseo_a_json(str(360))


URL = 'https://www.ucm.es/elecciones/rector-2015/mesas/?mid='
Rector2015V2 = datos_rector.elecciones_ucm(datos, URLs, URL)
Rector2015V2.scrap()


URL = 'https://www.ucm.es/elecciones/rector-2019/mesas/?mid='
Rector2019 = datos_rector.elecciones_ucm(datos, URLs, URL)
Rector2019.scrap()



with open('2015_vuelta1.json', 'w') as fp:
    json.dump(Rector2015V1.datos, fp, sort_keys=True, indent=4)
with open('2015_vuelta2.json', 'w') as fp:
    json.dump(Rector2015V2.datos, fp, sort_keys=True, indent=4)
with open('2019.json', 'w') as fp:
    json.dump(Rector2019.datos, fp, sort_keys=True, indent=4)



