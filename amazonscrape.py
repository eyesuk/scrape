import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
import re

def amazonPrintComp(dataRef, search):
	"""
	Gets product and price from a product page on amazon as well as a list of products & prices from "Customers who purchased this item frequently bought"
	section. Appends lists products & prices to a .csv file.

	dataref is the unique product code to be plugged into the url
	search is the search term input by the user to get the product codes
	"""
	file = open('amz-'+search+'.csv', 'a')
	writer = csv.writer(file)

	url = "https://www.amazon.com/dp/"+dataRef

	headers = {'User-Agent': 'Mozilla/5.0'}
	print ("Processing: "+url)
	page = requests.get(url,headers=headers)
	bsobj = BeautifulSoup(page.content, "html.parser")

	myProduct = bsobj.find("span", id="productTitle")
	myProduct = myProduct.get_text().strip()
	# print(myShirt)
	# print(myShirt.get_text().strip())
	myPrice = bsobj.find("span", id="priceblock_ourprice")
	myPrice = myPrice.get_text()
	myPrice = float(myPrice[1:5])
	# print(myPrice)

	car = bsobj.find("div", class_="a-carousel-col a-carousel-center")
	# print(car)
	eachProduct = car.findAll("div", class_="sponsored-products-truncator-truncate sponsored-products-truncator-line-clamp-4")
	eachProduct = [p.get_text().strip() for p in eachProduct]
	# for i in eachProduct:
	# 	i = filter(lambda ch: ch not in ",", i)

	prices = bsobj.findAll("span", class_="p13n-sc-price")
	prices = [p.get_text().strip() for p in prices]
	prices = [float(p[1:5]) for p in prices]

	hrefs = bsobj.find_all('a', {"class":"a-link-normal"}, href=True)
	hrefs = [link['href'].strip() for link in hrefs] 

	eachProduct.append(myProduct)
	prices.append(myPrice)

<<<<<<< HEAD
	writer.writerow(hrefs)
=======
	writer.writerow(dataRef)
>>>>>>> b48595c77b6141d9cb52a8a14b5aa37c5632db61
	writer.writerow(eachProduct)
	writer.writerow(prices)

	file.close()

def main():

	headers = {'User-Agent': 'Mozilla/5.0'}

	#input
	search = input("What would you like to compare? ")
	url = "https://www.amazon.com/s/keywords="+search
	print ("Processing: "+url)
	page = requests.get(url,headers=headers)
	bsobj = BeautifulSoup(page.content, "html.parser")

	data = bsobj.find("div", {'id':'resultsCol'})
	newdata = data.findAll(attrs={"data-asin" : re.compile(r'B0')})
	
	listOfGoods = []
	for i in newdata:
		listOfGoods.append(i["data-asin"])

	for i in listOfGoods:
		try:
			amazonPrintComp(i, search)
		except AttributeError:
			pass
		else:
			pass

		sleep(3)
	print("Completed")

main()


	