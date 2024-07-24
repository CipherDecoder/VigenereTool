import os
import ic
import processing
import freq_analysis as fa
from const import MAX_KEY_LEN, ALPHABET
def _encipher(plaintext, key):
    shifts = [ALPHABET.index(letter) for letter in key]
    blocks = processing.get_blocks(text=plaintext,size=len(key))
    cols = processing.get_columns(blocks)
    ciphered_blocks = processing.to_blocks([fa.shift_enc(col, shift) for col, shift in zip(cols, shifts)])
    ciphered = ''.join(ciphered_blocks)
    return ciphered

def _decipher(ciphertext, key):
    shifts = [ALPHABET.index(letter) for letter in key]
    blocks = processing.get_blocks(text=ciphertext,size=len(key))
    cols = processing.get_columns(blocks)
    deciphered_blocks = processing.to_blocks([fa.shift(col, shift) for col, shift in zip(cols, shifts)])
    deciphered = ''.join(deciphered_blocks)
    return deciphered

if __name__ == "__main__":
    text = input("Введи текст или путь к файлу с текстом: ")
    if os.path.exists(text):
        with open(text, "r") as file:
            text = file.read()
    text = processing.clear_text(text)
    print(text)
    inp = input("Введи ш для шифрования или р для расшифрования: ")
    if inp in "шШ" and inp != "":
        key = processing.clear_text(input("Введи ключ-слово: "))
        ciphered = _encipher(text, key)
        print("Шифротекст: " + ciphered)
        inp = input("Имя файла для сохранения: ")
        with open("encrypted/" + inp, "w") as file:
            file.write(ciphered)
    elif inp in "рР" and inp != "":
        inp = input("Введи к для расшифровки с ключём или ничего для вскрытия: ")
        if inp == "к":
            key = processing.clear_text(input("Введи ключ: ").upper())
        else:
            key_len = ic.find_key_length(ciphertext=text, max_key_len=MAX_KEY_LEN)
            key = fa.restore_key(text, key_len)
            print('Предполагаемая длина ключа: ' + str(key_len))
            print('Восстановленный ключ: ' + str(key))
            inp = input("Нужно подправить ключ? (y/N): ")
            if inp in "yY" and inp != "":
                key = processing.clear_text(input("Введи ключ: ").upper())
        deciphered = _decipher(text, key)
        print('Открытый текст: ' + str(deciphered))
        inp = input("Имя файла для сохранения: ")
        with open("decrypted/" + inp, "w") as file:
            file.write(deciphered)
