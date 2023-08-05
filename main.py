from tlgCode import tlgCode

# Exemplo de uso da classe
generator = tlgCode.TLGCode()
url = "https://www.instagram.com/sully.artt/"
generator.generate_qr_code(url)
qr_code_matrix = generator.get_qr_code_matrix()

if qr_code_matrix is not None:

    qr_code_image = generator.generate_image()
    qr_code_image.save('qrcode.png')
    generator.generate_stl()

