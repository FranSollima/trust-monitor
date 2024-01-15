article = {'title' : """Afirman que subió la oferta de alquileres y que hubo bajas del 20% con la derogación de la ley""",
'body': """El presidente de la Cámara de Propietarios de la República Argentina aseguró que ahora hay '7.000 propiedades en oferta' mientras que hace semanas, con la vigencia de la cuestionada norma, 'no llegábamos a las 50, 60, viviendas'.
La derogación de la Ley de Alquileres a partir de la entrada en vigencia del Decreto 70/2023 generó un aumento en la oferta y 'bajas de un 20% promedio' en los precios en determinadas zonas de la Ciudad de Buenos Aires, afirmó este sábado el presidente de la Cámara de Propietarios de la República Argentina (Capra), Enrique Abatti.

'Hasta hace más o menos 20 días había oferta cero, no llegábamos a las 50, 60, viviendas; y al día de ayer (por el viernes) había más de 7.000 en oferta', subrayó Abatti en declaraciones a Radio Rivadavia.


Al respecto, consideró que 'esto beneficia fundamentalmente a los propietarios y a los inquilinos, así como a los corredores inmobiliarios'.

Asimismo, destacó que 'hoy el inquilino puede elegir y discutir el precio del alquiler', lo cual llevó a que 'en algunos barrios de Capital Federal han bajado 20% promedio el precio de los alquileres respecto de lo que pretendían los propietarios hace un mes atrás'.

Abatti recordó que 'el 1 de julio de 2020 comenzó la vigencia de una Ley de Alquileres que fue el origen de todas las penurias que pasaron no solamente los inquilinos, que no conseguían vivienda, sino también los propietarios, que tenían condiciones incumplibles por parte de los inquilinos, con contratos congelados por un año, con una inflación que supera el 160%'.

'Antes de la vigencia la Ley 27.551 no había grandes problemas entre inquilinos y propietarios: había una oferta permanente en Capital Federal de no menos de 20.000 viviendas', puntualizó.

No obstante, continuó, 'cuando comenzó la vigencia de esa ley fue bajando paulatinamente hasta llegar hace unos seis meses a 1.300 viviendas'.

'Luego se sancionó la segunda ley (Nº 27.737), con la que pretendían modificar los desastres que habían hecho con la 27.551, pero fue como echar más nafta al fuego porque a partir de ahí desapareció la oferta', señaló el presidente de Capra.


'Esto es extraordinario', enfatizó Abatti, quien consideró la entrada en vigor del Decreto 70/2023 como 'un cambio copernicano'.

Por su parte, Daniel Zampone, vicepresidente de la Cámara Inmobiliaria Argentina (CIA), manifestó también hoy que 'el mercado inmobiliario se está recuperando' luego de atravesar 'los peores cuatro años de lo que va del siglo del mercado'.

En diálogo con LN+, Zampone comentó que a partir de la derogación de la norma se están celebrando contratos 'como se hacía antes de 2020: cada dos años, en pesos y con actualizaciones cada tres meses por la inflación'.

En cuanto a la moneda acordada para el pago del alquiler, el vicepresidente de CIA dijo que 'puede pactarse con dólares, reales o pesos, la moneda que sea, siempre y cuando las partes estén de acuerdo'.


En este sentido, trajo a colación un reciente caso ocurrido en Rosario, Santa Fe, donde tanto propietario como inquilino acordaron que el pago se realice en bitcoins."""}

from NLP.nlp_base import NLP

nlp = NLP('es')
doc = nlp.analyze(article['body'])
entities = nlp.extract_entities_v2(doc)
#entity_classification = nlp.classify_entities(doc)
adjectives = nlp.extract_adjectives(doc)
adjective_count = nlp.count_adjectives(adjectives)
#entity_sentiments = nlp.extract_entity_sentiments(doc)
#place = nlp.extract_place(doc)
#date = nlp.extract_date(doc)
#sources = nlp.extract_sources(doc)
#links = nlp.extract_links(doc)

print(entities)
#print(entity_classification)
#print(adjectives)
print(adjective_count)
#print(entity_sentiments)
#print(doc.sentences[0].tokens[0])