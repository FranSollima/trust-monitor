import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tqdm import tqdm

def open_chrome(headless=True):
	options = webdriver.ChromeOptions()
	if headless:
		options.add_argument('headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('--disable-gpu')
	options.add_argument('--disable-extensions')
	options.add_argument('log-level=2')
	return webdriver.Chrome(options=options)

def get_data_noticia(link):
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
	data_noticia['cuerpo'] = ''
	cuerpo = soup.find('div', {'class': 'story'}).find('section')
	for elemento in cuerpo.find_all():
		if elemento.name in ('p', 'span', 'h2', 'h1', 'h5'):
			data_noticia['cuerpo'] += elemento.text + '\n'
		elif elemento.name in (
			'ul', 'li', 'ol', 'b', 'i', 'h3', 'h4', 'blockquote', 'br',
			'a', 'div', 'script', 'article', 'g', 'path', 'u', 'section',
			'figure', 'img', 'genoa-player', 'vf-conversation-starter',
			'figcaption', 'svg', 'iframe', 'figure', 'button'
		):
			pass
		else:
			print(link)
			print(elemento.name)
			print(elemento.text)
	return data_noticia

def get_links_noticias():
	links_noticias = set()
	url_ultimas_noticias = 'https://www.lavoz.com.ar/lo-ultimo/'
	for i in tqdm(range(1, 61)):
		print(url_ultimas_noticias + str(i))
		with open_chrome() as driver:
			driver.get(url_ultimas_noticias + str(i))
			main = driver.find_element(By.CSS_SELECTOR, 'section.main-content')
			while not main.find_elements(By.CSS_SELECTOR, 'a.story-card-entire-link'):
				pass
			links_noticias_pagina = driver.execute_script("""
				const links = Array.from(document.querySelectorAll('a.story-card-entire-link'));
				const links_noticias = links.map(link => link.href);
				return links_noticias;
			""")
			driver.quit()
		links_noticias_pagina = set(links_noticias_pagina)
		links_noticias.update(links_noticias_pagina)
		return links_noticias

def get_links_noticias_from_txt(txt_file):
	links_noticias = set()
	with open(txt_file) as f:
		for line in f:
			links_noticias.add(line.strip())
	return links_noticias

# links_noticias = get_links_noticias()
links_noticias = get_links_noticias_from_txt('links_noticias.txt')
print('Links scrapeados: {}'.format(len(links_noticias)))

data_noticias = []
errores = []
for link in tqdm(links_noticias):
	if link in [noticia['link'] for noticia in data_noticias]:
		continue
	try:
		data_noticias.append(get_data_noticia(link))
	except:
		print('Error en:', link)
		errores.append(link)
		continue
print('Noticias scrapeadas: {}'.format(len(data_noticias)))
print('Errores: {}'.format(len(errores)))
for error in errores:
	print(error)

with open('data_noticias.json', 'w') as f:
	json.dump(data_noticias, f, indent=4)
