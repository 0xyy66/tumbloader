import requests as req
from bs4 import BeautifulSoup
from glob import glob
import os
import shutil
from colorama import Fore, init
from tqdm import tqdm

init(autoreset=True)
pwd = os.path.join(os.getcwd())
tmp_dir = os.path.join(pwd, 'tmp')

def check_tmp_dir():
	if not glob(tmp_dir):
		os.mkdir(tmp_dir)
		print(f'{tmp_dir} directory not found. Created.')
	
def get_photos_url(url):
	res = req.get(url)
	sauce = BeautifulSoup(res.text, features="html.parser")
	post_media_photo = sauce.find_all('img', {'class': 'post_media_photo image'})
	u_photo = sauce.find_all('img', {'class': 'u-photo'})
	photos = post_media_photo + u_photo
	return photos

def save_photo_locally(p):
	photo_url = str(p['src'])
	try:
		with open(os.path.join(tmp_dir, photo_url.split('/')[-1]), 'wb') as img:
			img_data = req.get(photo_url, stream = True)
			shutil.copyfileobj(img_data.raw, img)
	except:
		print(Fore.RED + 'Something went wrong.\n', photo_url + 'not downloaded')

if '__main__' == __name__:
	check_tmp_dir()
	url = str(input('insert tumblr profile url> '))
	if not url:
		# just a random profile i found cool
		url = 'https://wekartu.tumblr.com/'
	photos = get_photos_url(url)
	for p in photos:
		print(f"Downloading {str(p['src']).split('/')[-1]}")
		for i in tqdm(range(1)):
			save_photo_locally(p)
	print(f'Done! Your images have been saved in {tmp_dir}')