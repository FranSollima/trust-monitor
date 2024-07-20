from transformers import pipeline

# Load the question-answering pipeline with a Spanish model
#qa_pipeline = pipeline("question-answering", model="mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es")

qa_pipeline = pipeline(
    'question-answering', 
    model='mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es'
)


# Example context (a news post in Spanish)
context = """ARTICULO:
La Voz es finalista en los Premios Digital Media Américas 2024 que organiza la Asociación Mundial 
de Editores de Noticias (WAN Ifra), en la categoría Mejor proyecto de suscripciones digitales/ Proyecto 
de reader revenue, con el proyecto Cursos exclusivos para suscriptores.Se trata de un lanzamiento que 
realizó La Voz en 2023 para diversificar la propuesta de valor para nuestra audiencia de suscriptores. 
Son webinarios dictados por reconocidos profesionales y se suman a los contenidos ya clásicos que ofrecemos 
como medio periodístico (informes, noticias, newsletters, videos) y los beneficios comerciales que ofrecemos 
(tarjeta de membresía Club La Voz para descuentos en comercios).En nuestro espacio online de cursos 
exclusivos, ofrecemos contenidos en video (con material didáctico escrito, en algunos casos) dictados por 
el chef Javier Rodríguez, creador de El Papagayo (entre los mejores 100 restaurantes de Latinoamérica 
según “Best Latam”); la bartender y capacitadora Pipi Yalour (autora del libro Manual de coctelería y 
creadora de la plataforma Chicas barra) y la psicopedagoga y especialista en educación Liliana González. 
Desarrollamos, además, una plantilla que permite acceder a un índice con 
los módulos de cada curso, para que sea amigable la navegación tanto en teléfonos celulares como en 
computadoras.En la misma categoría de los premios Digital Media Américas 2024, compiten los proyectos 
Rio Gastronomía y SP Gastronomía, de O Globo; UOL Prime, de UOL, y Valor PRO, de Valor Econômico, todos 
medios o grupos de medios de Brasil. Hubo más de 140 casos inscriptos. Roberto Perez, uno de los estudiantes
comentó: “Es el mejor medio de latinoamerica, por lejos”. La ceremonia de entrega será en 
la ciudad de Panamá, el 11 y 12 de abril.La Voz resultó ganadora de los premios en otras oportunidades: 
en 2022, obtuvo el primer premio como Mejor campaña patrocinada o de branded content, por la experiencia 
#MetelePata, de Voy de viaje. En 2019, ganó un premio por una serie llamada Cazatormentas. Y en 2016 obtuvo 
el galardón como Mejor sitio de noticias de Latinoamérica.
"""

# Define a list of questions to ask about the context
questions = [
    "¿Cuál es el tema principal del artículo?",
    "¿De quién trata el artículo?",
    "¿Cuándo ocurrieron los eventos en el artículo?",
    "¿Dónde ocurrieron los eventosen el artículo?",
    "¿Cuantos nombres propios se mencionan en este artículo?",
    "¿Quienes son los nombres propios que se mencionan en este artículo??",
    "Cuantas fuentes de informacion se mencionan el el articulo?. Dame solo el numero entero."

]

# Get answers to each question
for question in questions:
    result = qa_pipeline(question=question, context=context)
    print(f"Pregunta: {question}")
    print(f"Respuesta: {result['answer']}\n")