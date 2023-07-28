from tlgCode import tlgCode
import cv2
# Exemplo de uso da classe
generator = tlgCode.TLGCode()
url = "https://web.telegram.org/k/#@HenriqueCaires"
generator.generate_qr_code(url)
qr_code_matrix = generator.get_qr_code_matrix()
print('a')
if qr_code_matrix is not None:
    print('b')
    qr_code_image = generator.generate_image()
    qr_code_image.save('qrcode.png')
    generator.generate_stl3('qrcode.stl')
