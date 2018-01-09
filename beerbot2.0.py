##############################
# Dalton Pearson - 19/9/2017 #
# BeerBot                    #
##############################

from lxml import html
import requests
import unicodedata
import pyodbc
import time
#sql connection and empty table
con_string = (
    r"Driver={ODBC Driver 13 for SQL Server};"
    r"Server=DALTON-PC\SQLEXPRESS;"
    r"Database=PROG1735;"
    r"Trusted_Connection=yes;"
    )
cnxn = pyodbc.connect(con_string)
cursor=cnxn.cursor()

cnxn.commit()


def tofile(beerID, name, percent, pack, quantity, volume, price, priceos, isOnSale):
	values = '('  + str(beerID) + ', \'' + name + '\', ' + percent + ', ' + quantity + ', \''  + pack + '\', ' + volume + ', ' + price +', '+ priceos + ', ' + str(isOnSale) + ')'
	with open('beer', 'a') as f:
		f.write(values + ',' + '\n')
		f.close()
	
	#SQL SERVER insertion
	insert = 'INSERT INTO PRODUCTS (beerID, prodName, prodAlc, prodQuantity, prodPackage, prodVol, prodPrice, prodSalePrice, prodIsOnSale) VALUES '
	cursor.execute(insert+values)
	cnxn.commit()

def firstList(lists):
	list = lists[0]
	return list


def prog(beer, beers, name):
	bar = 20*beer/beers
	vis = '['+"|"*bar + (20-bar) * " " + ']'
	print "\n"*10 + name + '\n' + str(beer) + ' of ' + str(beers) + ' Beers\n' + str(vis)

def normQuantity(string):
	#done
	if string[1] == " ":
		return string[0]
	elif string[1] != " ":
		return string[0:2]

def normPack(string):
	#done
	if string[6] == "C" or string[7] == "C":
		return "Can"
	elif string[6] == "B" or string[7] == "B":
		return "Bottle"
	elif string[6] == "K" or string[7] == "K":
		return "Keg"
	elif string[6] == "A" or string[7] == "A":
		return "Aluminum Bottle"
		
def normVolume(string):
	#done
	string = string.strip(' ml')
	x=1
	while x < len(string):
		if string[-x-1] == " ":
			return string[-x:]
		x=x+1

def normPrice(list):
	#done
	for x in range(len(list)):		
		price = list[x]
		list[x] = price[1:]						
	return list

def salePrice(listos, listns):
	#done
	for x in range(len(listos)):
		if listos[x] == listns[x]:
			listos[x] = "null"
		elif listos[x] != listns[x]:
			sale = listos[x]
			listos[x] = sale[9:]
	return listos

def normalize(list):
	#done
	escapes = ''.join([chr(char) for char in range(1, 32)])
	for x in range(0, len(list)):		
		list[x] = unicodedata.normalize("NFKD", list[x])
	return list

def isOnSale(listos,listns):
	#done
	if listos == 'null':
		return 0
	elif listos != 'null':
		return 1

def beers(beerlink):
	#done
	#determine total number of beers in the beerlink list
	beers = 0
	for x in range(24, len(beerlink)):
		if beerlink[x] == "https://www.facebook.com/TheBeerStoreON/?utm_source=website&utm_medium=footer":
			break
		beers = beers + 1
	return beers

def run():
	#get all distinct beers from beer store search page
	cursor.execute("DELETE FROM PRODUCTS")
	page = requests.get('http://www.thebeerstore.ca/beers/search')
	tree = html.fromstring(page.content)
	beerlink = tree.xpath('//li/a/@href')

	print "connected"

	beer = 0
	beerID = 0
	totalBeers = beers(beerlink)

	#get all entries in each individual beer page
	for x in range(24, len(beerlink)):#24
		
		#error handling to end loop before non-beer link is entered
		if beerlink[x] == "https://www.facebook.com/TheBeerStoreON/?utm_source=website&utm_medium=footer":
			break
		search = "http://www.thebeerstore.ca" + beerlink[x]
		#get page and then individual beer links
		try:
			page = requests.get(search)
		except:
			run()
			break
		
		tree = html.fromstring(page.content)
		#get prices excludingcluding sale prices
		pricens = normPrice(tree.xpath('//td[@class="price"]/text()|//td[@class="price"]/strike/text()'))
		#get prices including sale prices
		priceos = salePrice(normPrice(tree.xpath('//span[@class="sale-price"]/text()|//td[@class="price"]/text()')), pricens)
		#get size string
		size = normalize(tree.xpath('//td[@class="size"]/text()'))
		#get name from title tag and format
		name = (firstList(tree.xpath('//title/text()'))[:-17]).strip()
		
		#get percent and error handling for alcohol percentage of non-alcoholic beers	
		try:
			percent = firstList(tree.xpath('//*[@id="block-system-main"]/div/div[1]/div/div/div/div[2]/dl/dd[3]/text()'))[:-1]
		except:
			percent = "0.0"
		#get brewery and category text
		#currently not used
		#brewery = firstList(tree.xpath('//*[@id="block-system-main"]/div/div[1]/div/div/div/div[2]/dl/dd[2]/text()'))
		#category = firstList(tree.xpath('//*[@id="block-system-main"]/div/div[1]/div/div/div/div[2]/dl/dd[1]/text()'))
		
		#call functions and write to file/ insert into sql database
		for x in range(0,len(size)):
			tofile(beerID, name, percent, normPack(size[x]), normQuantity(size[x]), normVolume(size[x]), pricens[x], priceos[x], isOnSale(priceos[x], pricens[x]))
		
		#iterate beerID and call progress function
		beerID = beerID + 1
		prog(beerID, totalBeers, name)
runs = 0
while 0<1:
	#Simple loop to make the script update the database once per hour
	run()
	runs=runs+1
	print ("Runs: "+str(runs))
	time.sleep(3600)
print "Error too many searches"