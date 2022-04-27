<h1 align="center">Welcome to xbpp-img2array 👋</h1>
<p>
  <a href="https://github.com/LeFrenchPOC/xbpp-img2array/blob/main/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg" />
  </a>
</p>

> Python script to convert any type of image to C header array of bytes for EPaper display in multiple bit per pixel mode.

## What is it?
HD EPaper display with small microcontroller uses a lot of memory. Some displays can be used with less than 1 byte per pixel. In this case images cost less memory. This script converts any image to C header array of bytes for EPaper display in multiple bit per pixel mode (1, 2, 4 or 8 bits). It can be used with [IT8951 library](https://github.com/LeFrenchPOC/IT8951-32bit).

## Dependencies
- The `convert` command is not available on Windows. You have to install [ImageMagick](https://imagemagick.org/script/download.php)
- Any version of Python 3.x
- [Pillow](https://pillow.readthedocs.io/en/stable/)
```
pip install Pillow
```

## Usage
```
python img2array.py TYPE IMG_WIDTH IMG_HEIGHT IMG1_FILE_PATH IMG2_FILE_PATH ...
```
- `TYPE` can be `1bpp`, `2bpp`, `4bpp` or `8bpp`
- `IMG_WIDTH` and `IMG_HEIGHT` are the width and height of the image in pixels
- `IMGX_FILE_PATH` are the paths to the image files. Batch processing is supported.

## Author

👤 **Le French POC**

* Github: [@LeFrenchPOC](https://github.com/LeFrenchPOC)
* Website: [https://www.lefrenchpoc.fr/](https://www.lefrenchpoc.fr/)

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2021 [Le French POC](https://github.com/LeFrenchPOC).<br />
This project is [MIT](https://github.com/LeFrenchPOC/xbpp-img2array/blob/main/LICENSE) licensed.