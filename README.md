# Yi camera firmware downloader

Supports Yi 4K, Yi 4K+, Yi Lite

### arguments:

#### positional arguments:
*  camera      Camera Serial Number

#### optional arguments:
*  -h, --help  show this help message and exit
*  -a          List previous firmwares
*  -n N        Custom filename
*  -c          Removes download confirmation


* Download latest Yi Lite firmware: python yi-fw-dl.py J11V21C 
* Choose which firmware to download: python yi-fw-dl.py J11V21C -a
* Download latest firmware as firmware.bin: python yi-fw-dl.py J11V21C -n firmware.bin
    

