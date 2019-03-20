import json
import requests
from bs4 import BeautifulSoup



HOST = "http://www.matas.dk"

# -------- home page query ---------------

def get_product_page_url_list():
	url_list = []

	home_page = requests.get(HOST)
	soup = BeautifulSoup(home_page.content, 'html.parser')
	# print(soup.prettify())

	#for link in soup.find_all("a"):
	temp_url_list = []
	for link in soup.find_all("a", {"class": "nav__link"}):
		url = link.get('href')
		temp_url_list.append(url)


	for url in temp_url_list:
		if "http" not in url:
			if "maend/barbering" in url:
				url_list.append(url)
				print(url)


	return url_list

# -------- product page query ----------------

def get_product_list_from_page(url):
	# url = "https://www.matas.dk/makeup/ansigt/pudder"
	# url = "https://www.matas.dk/makeup/ansigt/foundation"
	product_page = requests.get(HOST + url)
	product_page_soup = BeautifulSoup(product_page.content, 'html.parser')
	product_tag_list = product_page_soup.find_all("div", class_="product-item")
	# print("len(product_tag_list): ", len(product_tag_list))


	products = []
	for product_tag in product_tag_list:
	# product_tag = product_item_list[0]
		title_row = product_tag.find_all("a")[1].span.find_all("span")
		brand = title_row[0].get_text().strip() if len(title_row) == 1 else ""
		name = title_row[1].get_text().strip() if len(title_row) == 2 else ""
		variant = title_row[2].get_text().strip() if len(title_row) == 3 else ""
		price = product_tag.find("div", class_="product-item__price-container").div.get_text().strip()

		product = {
			"brand": brand,
			"name": name,
			"variant": variant,
			"price": price
		}
		products.append(product)

	# print(products[0]['brand'])
	print("len(product_list_from_page): ", len(products))
	return products

def print_products(products):
	for product in products:
		print("name: ", product['name'], " price: ", product['price'])

if __name__ == '__main__':

	product_page_url_list = get_product_page_url_list()

	products = []
	for url in product_page_url_list:
		# print(len(get_product_list_from_page(url)))
		products.extend(get_product_list_from_page(url))

	print(len(products))
    # print_products(products)