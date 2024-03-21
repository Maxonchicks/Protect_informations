import os
import sys

DEGREE = 2
START_BYTE = 54
SIZE_ONE_BIT = 8


def start():
    while True:
        choice = int(input("Введите номер: 1 - кодирование, 2 - декодирование, 3 - выход\n"))

        if choice == 1:
            encode()
        elif choice == 2:
            decode()
        elif choice == 3:
            break
        else:
            print("Введена неккоректный номер!")


def encode():
    text_len = os.stat('text.txt').st_size
    img_len = os.stat('start1.bmp').st_size

    if text_len >= img_len * DEGREE / SIZE_ONE_BIT - START_BYTE:
        print("Слишком длинный текст!")
        return

    text = open('text.txt', 'r')
    start_bmp = open('start1.bmp', 'rb')
    encode_bmp = open('encode.bmp', 'wb')

    header_bytes = start_bmp.read(START_BYTE)
    encode_bmp.write(header_bytes)

    text_mask, img_mask = create_masks()

    while True:
        symbol = text.read(1)
        if not symbol:
            break
        symbol = ord(symbol)

        for _ in range(0, SIZE_ONE_BIT, DEGREE):
            img_byte = int.from_bytes(start_bmp.read(1), sys.byteorder) & img_mask
            bits = symbol & text_mask
            bits >>= (SIZE_ONE_BIT - DEGREE)
            img_byte |= bits
            encode_bmp.write(img_byte.to_bytes(1, sys.byteorder))

            symbol <<= DEGREE

    encode_bmp.write(start_bmp.read())

    text.close()
    start_bmp.close()
    encode_bmp.close()


def decode():
    to_read = int(input("Введите сколько символов прочитать: "))
    img_len = os.stat('encoded_5.bmp').st_size

    if to_read >= img_len * DEGREE / SIZE_ONE_BIT - START_BYTE:
        print("Слишком длинный текст!")
        return

    text = open('decoded.txt', 'w', encoding='utf-8')
    encoded_bmp = open('encoded_5.bmp', 'rb')

    encoded_bmp.seek(START_BYTE)
    text_mask, img_mask = create_masks()
    img_mask = ~img_mask

    read = 0
    while read < to_read:
        symbol = 0

        for _ in range(0, SIZE_ONE_BIT, DEGREE):
            img_byte = int.from_bytes(encoded_bmp.read(1), sys.byteorder) & img_mask

            symbol <<= DEGREE
            symbol |= img_byte

        read += 1
        text.write(chr(symbol))

    text.close()
    encoded_bmp.close()


def create_masks():
    text_mask = 0b11111111
    img_mask = 0b11111111

    text_mask <<= (SIZE_ONE_BIT - DEGREE)
    text_mask %= 256
    img_mask >>= DEGREE
    img_mask <<= DEGREE

    return text_mask, img_mask

start()
