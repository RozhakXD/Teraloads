#! /usr/bin/env python3
import requests, os, time, json, re, datetime
from bs4 import BeautifulSoup
from rich import print
from rich.panel import Panel
from rich.console import Console

# Banner
banner = ("""[bold red]╦═╗┌─┐┬  ┬┌─┐┬─┐┌─┐┌─┐  ╦┌┬┐┌─┐┌─┐┌─┐
[bold red]╠╦╝├┤ └┐┌┘├┤ ├┬┘└─┐├┤   ║│││├─┤│ ┬├┤
[bold white]╩╚═└─┘ └┘ └─┘┴└─└─┘└─┘  ╩┴ ┴┴ ┴└─┘└─┘
[italic cyan]Coded by Rozhak""")

# Open
def Open(file):
    try:
        gambar = open(file, 'rb').read()
        return {
            "Gambar": gambar
        }
    except (IOError):
        Console(width=50).print(Panel("[italic red]Gambar Yang Tidak Diketahui!", title='😡', style='plum4'));exit()
# Main
def Main():
    os.system('clear')
    Console(width=50).print(Panel(banner, style='bold plum4'), justify='center')
    try:
        Console(width=50).print(Panel("[italic white]Silahkan Masukan File Gambar Pastikan Sudah Benar Dan File Berisi Gambar Bukan Yang Lain, Misalnya :[italic green] Data/Contoh.jpg", title='😎', style='bold plum4'))
        file = Console().input("[bold white][[bold green]?[bold white]][bold white] Files : ")
        img = Open(file)["Gambar"]
        Console(width=50).print(Panel("[italic white]Sedang Mencari Semua Gambar Yang Sama, Silahkan Untuk Menunggu Sebentar!", title='🙂', style='bold plum4'));time.sleep(2.5)
        Search(img, datetime.datetime.now())
    except Exception as e:
        Console(width=50).print(Panel(f"[italic red]{str(e).title()}", title='😡', style='plum4'));exit()
# Search
def Search(img, file):
    with requests.Session() as r:
        url = ('https://yandex.com/images-apphost/image-download') # Uploading images to yandex
        r.headers.update({
            'Host': 'yandex.com',
            'user-agent': 'Mozilla/5.0 (Linux; Android 9; RMX1941 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36',
            'content-type': 'image/jpeg',
            'accept': '*/*',
            'origin': 'https://yandex.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-dest': 'empty',
            'referer': 'https://yandex.com/',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
        })
        params = {
            'cbird': 111,
            'images_avatars_size': 'preview',
            'images_avatars_namespace': 'images-cbir'
        }
        response = r.post(url, params = params, data = img)
        x = json.loads(response.text)
        image_id = x["image_id"]
        url = x["url"]
        image_shard = x["image_shard"]
        url = ('https://yandex.com/images/touch/search') # Search using images
        r.headers.update({
            'Host': 'yandex.com',
            'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'user-agent': 'Mozilla/5.0 (Linux; Android 9; RMX1941 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': 'https://yandex.com/',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        })
        params = {
            'rpt': 'imageview',
            'url': url,
            'cbir_page': 'sites',
            'cbir_id': f'{image_shard}/{image_id}'
        }
        response7 = r.get(url, params = params)
        sp = BeautifulSoup(response7.text, 'html.parser')
        quote = re.findall("&quot;https://(.*?)&quot;", str(sp))
        looping = 0
        for x in quote:
            looping += 1
            Console().print(Panel(f"[bold white]{looping}.[bold green] https://{x}", title='✅', style='plum4'))
            open(f"Data/{file}", "a+").write(f"https://{x}\n")
        tampung = []
        for z in sp.find_all('a', href=True):
            if 'https://' in str(z):
                if len(z['href']) <= 201:
                    if z['href'] in tampung:
                        continue
                    else:
                        looping +=1
                        tampung.append(z['href'])
                        Console().print(Panel(f"[bold white]{looping}.[bold green] {z['href']}", title='✅', style='plum4'))
                        open(f"Data/{file}", "a+").write(f"{z['href']}\n")
                else:
                    continue
            else:
                continue
        Console().input("[bold white][[bold red]Kembali[bold white]]");time.sleep(2.5);Main()

if __name__=='__main__':
    os.system('git pull');Main()
