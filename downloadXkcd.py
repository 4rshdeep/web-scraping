#! python3
import os, requests, bs4
url = "http://xkcd.com"
os.makedirs("xkcd", exist_ok=True)

# IITD proxy to use requests
# Require proxy at LAN, while there are no
# port restrictions on wifi though
proxies = {
    'http': 'http://proxy22.iitd.ac.in:3128',
    'https': 'http://proxy22.iitd.ac.in:3128',
    }


while not url.endswith('#'):
	# Download the page
	print('Downloading page %s....' % url)
	res = requests.get(url, proxies=proxies)
	res.raise_for_status()

	# Make a Soup
	soup = bs4.BeautifulSoup(res.text)
	
	# Find URL of the comic image
	comicElem = soup.select(' #comic img ')
	if comicElem == []:
		print('Could not find comic image')
	else:
		try:
			comicURL = 'https:' + comicElem[0].get('src')
			# Download Image
			print("Downloading image %s....." % comicURL)
			res = requests.get(comicURL, proxies=proxies)
			res.raise_for_status()
		except requests.exceptions.MissingSchema:
			#Skip the comic in case of exceptions
			prev = soup.select('a[rel="prev"]')[0]
			url = 'http://xkcd.com' + prev.get('href')
			continue
		# Save image to ./xkcd
	
		xkcdfile = open(os.path.join('xkcd', os.path.basename(comicURL)),'wb')
		for chunk in res.iter_content(10000):
			xkcdfile.write(chunk)

		xkcdfile.close()
	# Get the Prev button's url.
	prev = soup.select('a[rel="prev"]')[0]
	url = 'http://xkcd.com' + prev.get('href')
			
print('Done....')