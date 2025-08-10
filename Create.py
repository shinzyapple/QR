import qrcode
import random
import string
import os

def generate_random_string(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

# 保存フォルダ名
folder_name = "qr_codes"

# フォルダがなければ作る
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

random_str = generate_random_string()

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(random_str)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

# フォルダの中にファイルを保存
filename = os.path.join(folder_name, f"{random_str}.png")
img.save(filename)

with open("registered_codes.txt", "a") as f:
    f.write(random_str + "\n")

print("QRコードを生成しました。")
