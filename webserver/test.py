from tlgCode import tlgCode
import time

# Exemplo de uso da classe
generator = tlgCode.TLGCode()
url = "https://www.guergolet.art.br/?referer=qr"
generator.generate_qr_code(url)
qr_code_matrix = generator.get_qr_code_matrix()

start_time = time.time()
if qr_code_matrix is not None:

    qr_code_image = generator.generate_image()
    qr_code_image.save('qrcode.png')
    generator.generate_stl('qrcode.stl')

end_time = time.time()

time_difference = end_time - start_time

print(f"A chamada do método levou {time_difference} segundos.")
