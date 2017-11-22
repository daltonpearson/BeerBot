##############################
# Dalton Pearson - 19/9/2017 #
# BeerBot                    #
##############################

from lxml import html
import requests



comma = '\nINSERT INTO BEER (beerName, beerBrewery, beerCategory, beerAlc, beerPackage, beerUnits, beerUnitVol, beerPrice)\nVALUES\n'

def tofile():
	global comma
	with open('beer', 'a') as f:
		f.write(comma + '(\''  + name + '\', \'' + brewery + '\', \''  + category + '\', '  + percent + ', \'' + corb() + '\', '  + amount + ', ' + volume + ', ' + priceparse[1:] + ')')
#		f.write(name + ',' + brewery + ','  + category + ','  + percent + ',' + corb() + ','  + amount + ',' + volume + ',' + priceparse[1:] + ',' + str(apd) + '\n')
		f.close()
	comma = ',\n'
def firstList(lists):
	list = lists[0]
	return list
def corb():
	if parse[-8] == "n":
		return "C"
	elif parse[-8] == "e":
		return "B"
	elif parse[-9] == "e" and parse[-8] == " ":
		return "B"
	elif parse[-10] == "g":
		return "K"

def prog():
	bar = 20*beer/beers
	per = 100*beer/beers
	per = per
	vis = '['+"|"*bar + (20-bar) * " " + '] '
	print "\n"*10 + name + '\n' + enter + '\n' + str(beer) + ' of ' + str(beers) + ' Beers\n' + str(vis) +' ' + str(per) +'%'


page = requests.get('http://www.thebeerstore.ca/beers/search')
tree = html.fromstring(page.content)
beerlink = tree.xpath('//li/a/@href')

print "connected"
enter = " "
beers = 715 #len(beerlink)
beer = 0


for x in range(24, 738):#739

	search = "http://www.thebeerstore.ca" + beerlink[x]
	
	page = requests.get(search)
	tree = html.fromstring(page.content)
#	sale = tree.xpath('//strike/text()')
#	print sale
	
#	 or '//strike/text()'
	price = tree.xpath('//td[@class="price"]/text()')
	unit = tree.xpath('//td[@class="size"]/text()')
	
	name = firstList(tree.xpath('//title/text()'))
	percent = firstList(tree.xpath('//*[@id="block-system-main"]/div/div[1]/div/div/div/div[2]/dl/dd[3]/text()'))
	brewery = firstList(tree.xpath('//*[@id="block-system-main"]/div/div[1]/div/div/div/div[2]/dl/dd[2]/text()'))
	category = firstList(tree.xpath('//*[@id="block-system-main"]/div/div[1]/div/div/div/div[2]/dl/dd[1]/text()'))
#	price = price + sale
#	loc = 0
#	if len(unit) == (len(price)+1):
#		sale = sale[0]
#		sale = sale[1:]
#		sale = float(sale)
#		delta=0
#		print len(unit)-1
#		x=0
#		while x < len(unit)-1:
#			print 't'
#			low = price[x-1]
#			low = float(low[1:])
#			high = price[x]
#			high = float(high[1:])
#			print high-low
#			if (low<sale<high):
#				dif = high-low
#				if dif > delta:
#					loc = x
#			print loc
#			x += 1
#		sale = '$'+str(sale)
#		price.insert(loc, sale)
#	print price
	unit.reverse()
	price.reverse()

	if name[-18] == " ":
		name = name[0:-18]
	elif name[-18] != " ":
		name = name[0:-17]
	percent = percent[0:3]
	
	entered = 0
	beer += 1
	for x in range(0, len(unit)):
		parse = unit[x]
	
		
		if len(unit) == len(price):
			priceparse = price[x]
			amount = parse[0:2]
			volume = parse[-7:-3]
			volume = volume.lstrip()
			if parse[-7] == " ":
				if amount=="1 " and entered==0 and corb()=="B":
					amount = "1"
					tofile()
					enter = "Entered Bottle(1): " + name
					entered = 1
				elif amount=="1 " and entered==0 and corb()=="C":
					amount = "1"
					tofile()
					enter = "Entered Can(1): " + name
					entered = 1
				elif amount=="4 " and entered==0 and corb()=="B":
					amount = "4"
					tofile()
					enter = "Entered Bottle(4): " + name
					entered = 1
				elif amount=="4 " and entered==0 and corb()=="C":
					amount = "4"
					tofile()
					enter = "Entered Can(4): " + name
					entered = 1
				elif amount=="6 " and entered==0 and corb()=="B":
					amount = "6"
					tofile()
					enter = "Entered Bottle(6): " + name
					entered = 1
				elif amount=="6 " and entered==0 and corb()=="C":
					amount = "6"
					tofile()
					enter = "Entered Can(6): " + name
					entered = 1
				elif amount=="8 " and entered==0 and corb()=="B":
					amount = "8"
					tofile()
					enter = "Entered Bottle(8): " + name
					entered = 1
				elif amount=="8 " and entered==0 and corb()=="C":
					amount = "8"
					tofile()
					enter = "Entered Can(8): " + name
					entered = 1
				elif amount=="12" and entered==0 and corb()=="B":
					tofile()
					enter = "Entered Bottle(12): " + name
					entered = 1
				elif amount=="12" and entered==0 and corb()=="C":
					tofile()
					enter = "Entered Can(12): " + name
					entered = 1
				elif amount=="15" and entered==0 and corb()=="B":
					tofile()
					enter = "Entered Bottle(15): " + name
					entered = 1
				elif amount=="15" and entered==0 and corb()=="C":
					tofile()
					enter = "Entered Can(15): " + name
					entered = 1
				elif amount=="24" and entered==0 and corb()=="B":
					tofile()
					enter = "Entered Bottle(24): " + name
					entered = 1
				elif amount=="24" and entered==0 and corb()=="C":
					tofile()
					enter = "Entered Can(24): " + name
					entered = 1
			elif parse[-7] != " ":
				if amount=="1 " and entered==0 and corb()=="B":
					amount = "1"
					tofile()
					enter = "Entered Bottle(1): " + name
					entered = 1
				elif amount=="1 " and entered==0 and corb()=="C":
					amount = "1"
					tofile()
					enter = "Entered Can(1): " + name
					entered = 1
		


	if entered == 0:

		
		parse = unit[0]
		if corb()=="K":
			priceparse = price[0]
			amount = parse[0:1]
			volume = parse[-9:-3]
			volume = volume.lstrip()
			tofile()
			print "Entered Keg: " + name
		
		elif entered == 0:
			print "Not Entered: " + name
			with open('beerNR', 'a') as f:
				f.write(beerlink[x] + '\n')
				f.close()
	
	prog()

with open('beer', 'a') as f:
	f.write('\n;')
	f.close()

