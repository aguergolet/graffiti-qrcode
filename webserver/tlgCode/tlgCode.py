import qrcode
from PIL import Image, ImageDraw
import math
import subprocess
import uuid
import os

class TLGCode:
    def __init__(self):
        self.qr_code = None

    def generate_qr_code(self, url):
        # Gera o QR Code com a URL fornecida
        self.qr_code = qrcode.QRCode(version=2, box_size=10, border=4)
        self.qr_code.add_data(url)
        self.qr_code.make(fit=True)

    def get_qr_code_matrix(self):
        # Retorna a matriz do QR Code (áreas pretas e brancas) como uma lista de listas
        if self.qr_code is None:
            return None            


        return self.qr_code.get_matrix()

    def display_qr_code(self):
        # Exibe o QR Code
        if self.qr_code is not None:
            qr_code_image = self.qr_code.make_image(fill_color="black", back_color="white")
            qr_code_image.show()

    
    def generate_image(self):
        qr_code_matrix = self.get_qr_code_matrix()

        size = len(qr_code_matrix)
        pixel_size = int(1200 / size)
        image = Image.new("RGB", (1200, 1200), color=(255, 255, 255))

        identification_areas = self.get_identification_areas(len(qr_code_matrix))

        for i in range(size):
            for j in range(size):
                factor = 0
                is_white = not qr_code_matrix[i][j]
                if is_white :
                    color = (255, 255, 255)
                else:
                    color = (0,0,0)
                factor = 2
                for area in identification_areas:
                    x1, y1, x2, y2, color_debug = [i for i in area]
                    if i >= x1 and i <= x2 and j >= y1 and j <= y2:
                        factor = 0

                x = j * (pixel_size)
                y = i * (pixel_size)
                image.paste(color , (x+factor, y+factor, x + pixel_size - factor, y + pixel_size - factor))

        draw = ImageDraw.Draw(image)
        
        line_width=3
        for area in identification_areas:
            x1, y1, x2, y2, color_debug = [i * pixel_size for i in area]
            color_debug = int(color_debug/pixel_size)
            color = (color_debug,color_debug,color_debug)
            draw.line((x1-1,y1-1,x1+pixel_size,y1+pixel_size), fill=color, width=line_width)  # Top bridge
            draw.line((x2-1,y2-1,x2+pixel_size,y2+pixel_size), fill=color, width=line_width)  # Top bridge
            
            
            draw.line((x1+pixel_size-1,y2-1,x1,y2+(pixel_size)+1), fill=color, width=line_width)  # Top bridge
            draw.line((x2-1,y1+pixel_size-1,x2+pixel_size,y1-1), fill=color, width=line_width)  # Top bridge

        return image
    

    
    def generate_stl(self, file_name):
        qr_code_matrix = self.get_qr_code_matrix()
        size = len(qr_code_matrix)
        cube_size = int(math.ceil (200 / size))
        full_size = cube_size * size;
        main_cube = f"cube([{full_size},{full_size}, 3]);"
        identification_areas = self.get_identification_areas(len(qr_code_matrix))
        script = ""        
        for i in range(size):
            translate_x = int(i * cube_size);
            for j in range(size):
                factor = 0
                is_white = not qr_code_matrix[i][j]
                factor = 0.5
                for area in identification_areas:
                    x1, y1, x2, y2, color_debug = [i for i in area]
                    if i >= x1 and i <= x2 and j >= y1 and j <= y2:
                        factor = 0
                if not is_white:
                    translate_y = int(j * cube_size);
                    script += f"\n\ttranslate([{translate_x+factor/2}, {translate_y+factor/2},-2])\n\t\tcube([{cube_size-factor},{cube_size-factor},6]);"

        line_width = 0.8
        bridge = "";
        for area in identification_areas:
            x1, y1, x2, y2, color_debug = [i * cube_size for i in area]
            bridge += "\n"
            bridge += f"\ttranslate([ {x1-1}, {y1-1},0])\n\trotate([0,0,45])\n\t\t"
            bridge += f"cube([{cube_size*2}, {line_width},3]);\n"
            bridge += f"\ttranslate([ {x2-1}, {y2-1},0])\n\trotate([0,0,45])\n\t\t"
            bridge += f"cube([{cube_size*2}, {line_width},3]);\n"
            bridge += f"\ttranslate([ {x1+cube_size+1}, {y2-1},0])\n\trotate([0,0,135])\n\t\t"
            bridge += f"cube([{cube_size*2}, {line_width},3]);\n"
            bridge += f"\ttranslate([ {x2+cube_size}, {y1-1},0])\n\trotate([0,0,135])\n\t\t"
            bridge += f"cube([{cube_size*2}, {line_width},3]);\n"            
 

        with open('template.scad', 'r') as f:
            script = f.read().replace('__main_cube__',main_cube).replace('__holes__',script).replace('__bridges__', bridge)



            
            

        script =  "{\n" + script + "\n}"
        with open(f'{file_name}.scad', 'w') as source:
            source.write(script)
        
        subprocess.run(['openscad', "-o", f'{file_name}.stl', f'{file_name}.scad'])
        return file_name
        
        

    def get_identification_areas(self, size):
        """
        Get the coordinates of the identification areas in a QR Code matrix.

        Parameters:
            size: The size of the QR Code matrix.

        Returns:
            A list of tuples representing the coordinates of the identification areas.
        """
        # The identification areas are always located 7 modules from the edge of the matrix
        offset = 6


        return [(4, 4, 4+offset, 4+offset,255),  # Top-left area
                (4,size-5-offset, 4+offset, size-5,255),  # Top-right area
                (size-5-offset, 4, size-5, 4+offset,255),
                (size-offset*2-1, size-offset*2-1, size-offset-(offset/2), size-(offset*1.5),255)
                ]  # Bottom-left area

 