import qrcode

def generate_qrcode(url, token):
    file_path = '/media/qrcode/' + token + '.png'
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    image.save("."+ file_path)
    return file_path