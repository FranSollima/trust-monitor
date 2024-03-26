import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def getDataNoticia(link):
	soup = BeautifulSoup(requests.get(link).content, 'html.parser')
	data_noticia = {}
	data_noticia['link'] = link
	data_noticia['seccion'] = soup.find('div', {'class': 'story-section'}).text
	data_noticia['titulo'] = soup.find('header', {'class': 'story-title-restyling'}).text
	data_noticia['subtitulo'] = soup.find('h2', {'class': 'story-subtitle-restyling'}).text
	data_noticia['fecha_hora'] = soup.find('div', {'class': 'story-datetime-restyling'}).text
	data_noticia['autor'] = soup.find('div', {'class': 'story-author-restyling'}).text
	data_noticia['link_img'] = soup.find('div', {'class': 'story-promo'}).find('img')['src']
	data_noticia['caption_img'] = soup.find('div', {'class': 'story-promo'}).find('figcaption').text
	data_noticia['cuerpo'] = soup.find('div', {'class': 'story'}).find('section').text
	return data_noticia

links_noticias = set()
url_ultimas_noticias = 'https://www.lavoz.com.ar/lo-ultimo/'
for i in tqdm(range(1, 61)):
	soup = BeautifulSoup(requests.get(url_ultimas_noticias + str(i)).content, 'html.parser')
	for title in soup.find_all('h3', {'class': 'story-card-title'}):
		links_noticias.add('https://www.lavoz.com.ar'+title.find('a')['href'])
print('Links scrapeados: {}'.format(len(links_noticias)))

data_noticias = []
errores = []
for link in tqdm(links_noticias):
	if link in [noticia['link'] for noticia in data_noticias]:
		continue
	try:
		data_noticias.append(getDataNoticia(link))
	except:
		print('Error en:', link)
		errores.append(link)
		continue
print('Noticias scrapeadas: {}'.format(len(data_noticias)))
print('Errores: {}'.format(len(errores)))
for error in errores:
	print(error)

with open('data_noticias_lavoz.json', 'w') as f:
	json.dump(data_noticias, f, indent=4)
