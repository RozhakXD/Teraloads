#! /usr/bin/env python3
try:
    import requests, json, time, re, os, datetime, sys
    from rich.console import Console
    from rich import print
    from rich.panel import Panel
    from rich.progress import Progress
    from requests.exceptions import RequestException
except (Exception, KeyboardInterrupt) as e:
    exit(f"[Error] {str(e).capitalize()}!")

def Banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Panel("""[bold red]●[bold yellow] ●[bold green] ●[/]
[bold red].-----.                .-.                  .-.      
`-. .-'                : :                  : :      
  : : .--. .--.  .--.  : :   .--.  .--.   .-' : .--. 
[bold white]  : :' '_.': ..'' .; ; : :_ ' .; :' .; ; ' .; :`._-.'
  :_;`.__.':_;  `.__,_;`.__;`.__.'`.__,_;`.__.'`.__.'
       [italic blue]Terabox Downloader - Coded by Rozhak[/]""", width=57, style="bold bright_black"))
    return (0)

class Feature:

    def __init__(self):
        try:
            Banner()
            print(Panel(f"[italic white]Silahkan Masukan Link Terabox Pastikan Link Sudah Benar, Misalnya :[italic green] https://teraboxapp.com/s/?", width=57, style="bold bright_black", title=">>> Link Terabox <<<", subtitle="╭─────", subtitle_align="left"))
            your_links = Console().input("[bold bright_black]   ╰─> ")
            if '.com/s/' in your_links:
                self.link_kode = (your_links.split('.com/s/')[1])
            elif '?surl=' in your_links:
                self.split_link = ('1' + str(your_links.split('surl=')[1]))
                if '&' in str(self.split_link):
                    self.link_kode = self.split_link.split('&')[0]
                else:
                    self.link_kode = self.split_link
            else:
                print(Panel(f"[italic red]Anda Diwajibkan Memasukan Link Terabox Dengan Benar!", width=57, style="bold bright_black", title=">>> Link Tidak Benar <<<"))
                exit()
            print(Panel(f"[italic white]Silahkan Masukan Password Terabox Jika Tidak Ada Password Tekan Enter, Misalnya :[italic green] 123456", width=57, style="bold bright_black", title=">>> Password Terabox <<<", subtitle="╭─────", subtitle_align="left"))
            pwd = Console().input("[bold bright_black]   ╰─> ")
            print(Panel(f"[italic white]Sedang Mengunduh Seluruh File Pastikan Jaringan Kamu Bagus Agar Tidak Error Saat Mengunduh Files!", width=57, style="bold bright_black", title=">>> Catatan <<<"))
            self.Dapatkan_Files(self.link_kode, pwd)
        except (Exception) as e:
            print(Panel(f"[italic red]{str(e).title()}!", width=57, style="bold bright_black", title=">>> Error <<<"))
            exit()

    def Dapatkan_Files(self, shorturl, pwd):
        with requests.Session() as r:
            r.headers.update({
                'Host': 'terabox-dl.qtcloud.workers.dev',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'Accept': '*/*',
                'Referer': 'https://terabox-dl.qtcloud.workers.dev/',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Accept-Language': 'en-US,en;q=0.9',
                'Sec-Fetch-Dest': 'empty',
            })
            if len(pwd) == 0:
                self.password = ('')
            else:
                self.password = (pwd)
            params = {
                'shorturl': shorturl,
                'pwd': self.password,
            }
            response = r.get('https://terabox-dl.qtcloud.workers.dev/api/get-info', params = params)
            self.json_data = json.loads(response.text)
            if '\'ok\': True' in str(self.json_data):
                self.find_floders = re.findall('\'children\':', str(self.json_data))
                self.shareid, self.uk, self.sign, self.timestamp = self.json_data['shareid'], self.json_data['uk'], self.json_data['sign'], self.json_data['timestamp']
                if len(self.find_floders) == 2:
                    for z in self.json_data['list'][0]['children'][0]['children']:
                        self.create_time, self.fs_id, self.filename, self.size = z['create_time'], z['fs_id'], z['filename'], z['size']
                        self.mb_size = int(self.size) / (1024 * 1024)
                        self.create_string_time = datetime.datetime.fromtimestamp(int(self.create_time)).strftime('%d/%m/%Y %H:%M:%S')
                        print(Panel(f"""[bold white]Nama File :[bold green] {self.filename}
[bold white]Ukuran :[bold red] {self.mb_size:.2f} MB
[bold white]Upload Time :[bold green] {self.create_string_time}""", width=57, style="bold bright_black", title=">>> Sukses <<<"))
                        self.Downloads_File(self.shareid, self.uk, self.sign, self.timestamp, self.fs_id, self.filename.replace(' ', '_'))
                    Console().input("[bold white][[bold green]Selesai[bold white]]")
                    exit()
                else:
                    if '\'children\': []' in str(self.json_data):
                        for z in self.json_data['list']:
                            self.create_time, self.fs_id, self.filename, self.size = z['create_time'], z['fs_id'], z['filename'], z['size']
                            self.mb_size = int(self.size) / (1024 * 1024)
                            self.create_string_time = datetime.datetime.fromtimestamp(int(self.create_time)).strftime('%d/%m/%Y %H:%M:%S')
                            print(Panel(f"""[bold white]Nama File :[bold green] {self.filename}
[bold white]Ukuran :[bold red] {self.mb_size:.2f} MB
[bold white]Upload Time :[bold green] {self.create_string_time}""", width=57, style="bold bright_black", title=">>> Sukses <<<"))
                            self.Downloads_File(self.shareid, self.uk, self.sign, self.timestamp, self.fs_id, self.filename.replace(' ', '_'))
                        Console().input("[bold white][[bold green]Selesai[bold white]]")
                        exit()
                    else:
                        for z in self.json_data['list'][0]['children']:
                            self.create_time, self.fs_id, self.filename, self.size = z['create_time'], z['fs_id'], z['filename'], z['size']
                            self.mb_size = int(self.size) / (1024 * 1024)
                            self.create_string_time = datetime.datetime.fromtimestamp(int(self.create_time)).strftime('%d/%m/%Y %H:%M:%S')
                            print(Panel(f"""[bold white]Nama File :[bold green] {self.filename}
[bold white]Ukuran :[bold red] {self.mb_size:.2f} MB
[bold white]Upload Time :[bold green] {self.create_string_time}""", width=57, style="bold bright_black", title=">>> Sukses <<<"))
                            self.Downloads_File(self.shareid, self.uk, self.sign, self.timestamp, self.fs_id, self.filename.replace(' ', '_'))
                        Console().input("[bold white][[bold green]Selesai[bold white]]")
                        exit()
            else:
                print(Panel(f"[italic red]Tidak Bisa Mendapatkan Informasi Dari File Tersebut!", width=57, style="bold bright_black", title=">>> Gagal <<<"))
                exit()

    def Downloads_File(self, shareid, uk, sign, timestamp, fs_id, filename):
        with requests.Session() as r:
            try:
                r.headers.update({
                    'Accept-Encoding': 'gzip, deflate',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                    'Sec-Fetch-Dest': 'empty',
                    'Referer': 'https://terabox-dl.qtcloud.workers.dev/',
                    'Sec-Fetch-Mode': 'cors',
                    'Host': 'terabox-dl.qtcloud.workers.dev',
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Origin': 'https://terabox-dl.qtcloud.workers.dev',
                    'Sec-Fetch-Site': 'same-origin',
                    'Connection': 'keep-alive',
                })
                data = json.dumps({
                    'timestamp': timestamp,
                    'fs_id': fs_id,
                    'uk': uk,
                    'sign': sign,
                    'shareid': shareid,
                })
                response = r.post('https://terabox-dl.qtcloud.workers.dev/api/get-download', data = data)
                self.json_data = json.loads(response.text)
                if '\'ok\': True,' in str(self.json_data):
                    r.headers.pop('Content-Type')
                    r.headers.pop('Origin')
                    r.headers.update({
                        'Sec-Fetch-Mode': 'navigate',
                        'Referer': 'https://terabox-dl.qtcloud.workers.dev/',
                        'Upgrade-Insecure-Requests': '1',
                        'Sec-Fetch-Dest': 'document',
                        'Host': f'{re.search("https://(.*?)/", str(self.json_data["downloadLink"])).group(1)}',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Sec-Fetch-Site': 'cross-site',
                    })
                    response2 = r.get(self.json_data['downloadLink'], stream = True)
                    self.total_size = int(response2.headers.get('Content-Length', 0))
                    self.downloaded_size = 0
                    with Progress() as self.progress:
                        self.task = self.progress.add_task("[bold cyan]Unduhan...", total=self.total_size)
                        with open(f'/storage/emulated/0/Download/{filename}', 'wb') as w:
                            for data in response2.iter_content(chunk_size=1024):
                                w.write(data)
                                self.downloaded_size += len(data)
                                self.progress.update(self.task, completed=self.downloaded_size)
                            w.close()
                    sys.stdout.write("\033[F")
                    print(f"[bold bright_black]   ╰─>[bold green] Sukses Mengunduh {filename}...", end='\r')
                    time.sleep(2.5)
                    return (200)
                else:
                    print(f"[bold bright_black]   ╰─>[bold red] Tautan Unduhan Tidak Ditemukan...", end='\r')
                    time.sleep(3.5)
                    return (404)
            except (RequestException) as e:
                print(f"[bold bright_black]   ╰─>[bold red] Koneksi Anda Terputus Sedang Mengunduh Ulang...", end='\r')
                time.sleep(9.5)
                self.Downloads_File(shareid, uk, sign, timestamp, fs_id, filename)

if __name__=='__main__':
    try:
        if os.path.exists("Data/Subscribe.json") == False:
            youtube_url = json.loads(requests.get('https://raw.githubusercontent.com/RozhakXD/Teraloads/main/Data/Youtube.json').text)['Link']
            os.system(f'xdg-open {youtube_url}')
            with open('Data/Subscribe.json', 'w') as w:
                w.write(json.dumps({
                    "Status": True
                }))
            w.close()
            time.sleep(3.5)
        os.system('git pull')
        Feature()
    except (Exception) as e:
        print(Panel(f"[italic red]{str(e).title()}!", width=57, style="bold bright_black", title=">>> Error <<<"))
        exit()
    except (KeyboardInterrupt):
        exit()