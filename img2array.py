import os.path
import platform
import subprocess
import sys

from PIL import Image

dirname = os.getcwd()

table_path = os.path.join(dirname, 'tmp', 'table.gif')
px_width = 0
px_height = 0

system = platform.system()
cmd = ''
if system == 'Windows':
    cmd = 'magick.exe'
elif system == 'Linux':
    cmd = 'convert'
elif system == 'Darwin':
    cmd = 'convert'


def create_color_table():
    directory = os.path.join(dirname, 'tmp')
    if not os.path.exists(directory):
        os.makedirs(directory)
    subprocess.call([cmd, '-size', '1x16', 'gradient:gray100-gray0', table_path])


def get_image_height(image_path):
    im = Image.open(image_path)
    _, heigth = im.size
    return heigth


def scale_and_convert_image(image_path, type):
    converted_image_path_raw = os.path.splitext(image_path)[0]
    converted_image_path = os.path.join(dirname, 'tmp', 'current.gif')

    print("resizing, converting color ...")
    target_size = str(px_width) + 'x' + str(px_height)
    subprocess.call([cmd, image_path,
                     # '-rotate', '-90',
                     '-resize', target_size + '^',
                     '-gravity', 'center',
                     '-extent', target_size,
                     '-quantize', 'gray',
                     # '-brightness-contrast', '0x00',
                     '-dither', 'Floyd-Steinberg',  # see 'convert -list' for other options
                     '-remap', table_path,
                     # '-contrast-stretch', '20%', # macht die 16 colors kaputt
                     converted_image_path])
    print("converting to raw image ...")
    make_raw(converted_image_path, converted_image_path_raw, type)


def make_raw(image_path, destination_path, type):
    f = open(destination_path + '.h', 'wb')
    f.write(b'#ifndef __' + destination_path.upper().encode() + b'_H__\n')
    f.write(b'#define __' + destination_path.upper().encode() + b'_H__\n')

    f.write(b'#define ' + destination_path.upper().encode() + b'_WIDTH ' + str(px_width).encode() + b'\n')
    f.write(b'#define ' + destination_path.upper().encode() + b'_HEIGHT ' + str(px_height).encode() + b'\n')

    f.write(b'const uint8_t ' + destination_path.encode() + b'_data_' + type.encode() + b'[] = {\n')

    if type == "8bpp":
        write_8bpp(image_path, f)
    elif type == "4bpp":
        write_4bpp(image_path, f)
    elif type == "2bpp":
        write_2bpp(image_path, f)
    elif type == "1bpp":
        write_1bpp(image_path, f)

    f.seek(-1, os.SEEK_END)
    f.truncate()
    f.write(b'};\n')
    f.write(b'#endif\n')
    f.close()


def write_8bpp(image_path, header):
    im = Image.open(image_path)
    width, height = im.size
    start_height = 0
    if height > px_height:
        start_height = (height - px_height) // 2
        height = start_height + px_height

    px = im.load()
    num = 0
    for y in range(start_height, height):
        for x in range(0, width):
            val = px[x, y] * 17
            header.write(str(hex(val)).encode())
            header.write(b',')
            num += 1

    print("wrote " + str(num) + " bytes to file header")


def write_4bpp(image_path, header):
    im = Image.open(image_path)
    width, height = im.size
    start_height = 0
    if height > px_height:
        start_height = (height - px_height) // 2
        height = start_height + px_height

    px = im.load()
    val = 0
    i = 0
    num = 0
    for y in range(start_height, height):
        for x in range(0, width):
            i = not i
            if i:
                val = px[x, y]
            else:
                val += px[x, y] << 4
                header.write(str(hex(val)).encode())
                header.write(b',')
                num += 1

    print("wrote " + str(num) + " bytes to file header")


def write_2bpp(image_path, header):
    im = Image.open(image_path)
    width, height = im.size
    start_height = 0
    if height > px_height:
        start_height = (height - px_height) // 2
        height = start_height + px_height

    px = im.load()
    val = 0
    i = 0
    num = 0
    for y in range(start_height, height):
        for x in range(0, width):
            if i == 0:
                val = 0 if px[x, y] < 0xF else 3
                i += 2
            elif i == 6:
                val += 0 << i if px[x, y] < 0xF else 3 << i
                header.write(str(hex(val)).encode())
                header.write(b',')
                num += 1
                i = 0
            else:
                val += 0 << i if px[x, y] < 0xF else 3 << i
                i += 2
    print("wrote " + str(num) + " bytes to file header")


def write_1bpp(image_path, header):
    im = Image.open(image_path)
    width, height = im.size
    start_height = 0
    if height > px_height:
        start_height = (height - px_height) // 2
        height = start_height + px_height

    px = im.load()
    val = 0
    i = 0
    num = 0
    for y in range(start_height, height):
        for x in range(0, width):
            if i == 0:
                val = 0 if px[x, y] < 0x7 else 1
                i += 1
            elif i == 7:
                val += 0 << i if px[x, y] < 0x7 else 1 << i
                header.write(str(hex(val)).encode())
                header.write(b',')
                num += 1
                i = 0
            else:
                val += 0 << i if px[x, y] < 0x7 else 1 << i
                i += 1
    print("wrote " + str(num) + " bytes to file header")


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print(f'Usage: {sys.argv[0]} [type] [width] [height] [images]')
        exit(-1)

    type = sys.argv[1]
    if type != '1bpp' and type != '2bpp' and type != '4bpp' and type != '8bpp':
        print(f'Type must be 1bpp, 2bpp, 4bpp or 8bpp')
        exit(-1)

    px_width = int(sys.argv[2])
    px_height = int(sys.argv[3])

    create_color_table()
    for image_path in sys.argv[4:]:
        scale_and_convert_image(image_path, type)
