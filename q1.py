# function to encrypt one character
def encrypt_char(char, shift1, shift2):
    # check if it's lowercase letter
    if char.islower():
        pos = ord(char) - ord('a')  # get position (0-25)

        if pos <= 12:  # a-m
            shift = shift1 * shift2  # multiply shifts
            new_pos = pos + shift
            new_pos = new_pos % 13   # keep it in first half
            return chr(new_pos + ord('a'))

        else:  # n-z
            shift = shift1 + shift2  # add shifts
            new_pos = pos - shift
            new_pos = 13 + ((new_pos - 13) % 13)  # keep in second half
            return chr(new_pos + ord('a'))

    # checking if it's uppercase
    elif char.isupper():
        pos = ord(char) - ord('A')

        if pos <= 12:  # A-M
            shift = shift1
            new_pos = pos - shift
            new_pos = new_pos % 13
            return chr(new_pos + ord('A'))

        else:  # N-Z
            shift = shift2 ** 2  # square of shift2
            new_pos = pos + shift
            new_pos = 13 + ((new_pos - 13) % 13)
            return chr(new_pos + ord('A'))

    else:
        # if not a letter, just return as it is
        return char


# function to decrypt one character (reverse of encrypt)
def decrypt_char(char, shift1, shift2):
    if char.islower():
        pos = ord(char) - ord('a')

        if pos <= 12:  # came from a-m
            shift = shift1 * shift2
            original = (pos - shift) % 13
            return chr(original + ord('a'))

        else:  # came from n-z
            shift = shift1 + shift2
            original = 13 + ((pos + shift - 13) % 13)
            return chr(original + ord('a'))

    elif char.isupper():
        pos = ord(char) - ord('A')

        if pos <= 12:  # came from A-M
            shift = shift1
            original = (pos + shift) % 13
            return chr(original + ord('A'))

        else:  # came from N-Z
            shift = shift2 ** 2
            original = 13 + ((pos - shift - 13) % 13)
            return chr(original + ord('A'))

    else:
        return char


# encrypt full file
def encrypt(shift1, shift2):
    with open('raw_text.txt', 'r') as f:
        text = f.read()  # read original text

    encrypted = ''

    # go through each character
    for char in text:
        encrypted += encrypt_char(char, shift1, shift2)

    # save encrypted text
    with open('encrypted_text.txt', 'w') as f:
        f.write(encrypted)

    print("Encryption done! Saved to encrypted_text.txt")


# decrypt full file
def decrypt(shift1, shift2):
    with open('encrypted_text.txt', 'r') as f:
        text = f.read()  # read encrypted text

    decrypted = ''

    # decrypt each character
    for char in text:
        decrypted += decrypt_char(char, shift1, shift2)

    # save decrypted text
    with open('decrypted_text.txt', 'w') as f:
        f.write(decrypted)

    print("Decryption done! Saved to decrypted_text.txt")


# check if decrypted text matches original
def verify():
    with open('raw_text.txt', 'r') as f:
        original = f.read()

    with open('decrypted_text.txt', 'r') as f:
        decrypted = f.read()

    # compare both files
    if original == decrypted:
        print("Verification SUCCESSFUL! Decryption matches the original.")
    else:
        print("Verification FAILED! Files do not match.")


# main part of the program
if __name__ == "__main__":
    # take input from user
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    # run all steps
    encrypt(shift1, shift2)
    decrypt(shift1, shift2)
    verify()