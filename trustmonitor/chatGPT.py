import os
import json
import requests

api_key = 'your-api-key'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

url = 'https://api.openai.com/v1/chat/completions'


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
questions = [
    """Cuantas fuentes de informacion se mencionan el el articulo?. Responde solo el numero entero, por ejemplo '3'""",
    "cuales son las fuentes de informacion que se mencionan en el articulo, responde en forma de lista de phyton"]

def make_request(prompt):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0,
        "n": 1
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code == 200:
        generated_text = response_json['choices'][0]['message']['content']
        return generated_text
    else:
        print(f"Error: {response_json}")
        return None

def main():
    # Input text (e.g., a news article)

    for question in questions:
        prompt = f"Contexto: {context}\nPregunta: {question}\nRespuesta:"
        answer = make_request(prompt)
        #print(int(answer))
        print(f"Pregunta: {question}")
        print(f"Respuesta: {answer}")
        print("---------")

if __name__ == "__main__":
    main()
