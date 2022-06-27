SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZqwertyuiopasdfghjklzxcvbnme'
MAX_KEY_SIZE = len(SYMBOLS)

def getMode():
    while True:
        print('Do you wish to encrypt or decrypt a message?')
        mode = input().lower()
        if mode in ['encrypt', 'e', 'decrypt', 'd']:
            return mode
        else:
            print('Enter either "encrypt"/"e" or "decrypt"/"d".')

def getMessage():
    print('Enter your message:')
    return input()

def getKey():
    key = 0
    while True:
        print(f'Enter the key number (1-{MAX_KEY_SIZE}):')
        key = int(input())
        if (key >= 1 and key <= MAX_KEY_SIZE):
            return key

def getTranslatedMessage(mode, message, key):
    if mode[0] == 'd':
        key = -key
    translated = ''

    for symbol in message:
        symbol_index = SYMBOLS.find(symbol)
        if symbol_index == -1:
            # Means symbol not found in SYMBOLS
            # Just add this symbol without any change
            translated += symbol
        else:
            # Encrypt or decypt:
            symbol_index += key

            if symbol_index >= len(SYMBOLS):
                symbol_index -= len(SYMBOLS)
            elif symbol_index < 0:
                symbol_index += len(SYMBOLS)

            translated += SYMBOLS[symbol_index]
    return translated

mode = getMode()
message = getMessage()
key = getKey()
print('Your translated text is:')
print(getTranslatedMessage(mode, message, key))