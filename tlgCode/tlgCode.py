import qrcode
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageOps
import cv2
import numpy as np
from stl import mesh
import trimesh, trimesh.creation
import pymesh

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
        
        island_finder = IslandFinder(qr_code_matrix)
        island_finder.find_islands()
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

   
    def generate_stl2(self, stl_path):
        # Open the image and convert to grayscale
        image = image = self.generate_image().convert('L')
        image.save('qrcode1.png')
        image = ImageOps.invert(image)
        image.save('qrcode2.png')

        # Resize the image
        image = image.resize((600, 600), Image.ANTIALIAS)  # Change the size as needed
        image.save('qrcode3.png')

        # Convert the image to a numpy array
        data = np.array(image)

        # Normalize the data to the range [0, 1]
        data = data / np.max(data)

        # Scale the data to the desired height
        height = 2  # in mm
        data *= height

        # Create a grid of points
        nx, ny = data.shape
        x = np.linspace(0, 200, nx)  # Scale to 20 cm
        y = np.linspace(0, 200, ny)  # Scale to 20 cm
        x, y = np.meshgrid(x, y)

        # Create a 3D surface
        vertices = np.zeros((nx, ny, 3))
        vertices[..., 0] = x
        vertices[..., 1] = y
        vertices[..., 2] = data

        # Create the faces of the mesh
        faces = []
        for i in range(nx - 1):
            for j in range(ny - 1):
                # Two triangles forming a square
                faces.append([i * ny + j, (i + 1) * ny + j, i * ny + j + 1])
                faces.append([(i + 1) * ny + j, (i + 1) * ny + j + 1, i * ny + j + 1])
        faces = np.array(faces)

        # Add faces along the edges to close the sides
        for i in range(ny - 1):
            # Bottom side
            faces = np.append(faces, [[i, i + 1, ny * (nx - 1) + i]], axis=0)
            faces = np.append(faces, [[i + 1, ny * (nx - 1) + i + 1, ny * (nx - 1) + i]], axis=0)
            
            # Top side
            faces = np.append(faces, [[ny * (nx - 2) + i, ny * (nx - 2) + i + 1, ny * (nx - 1) + i]], axis=0)
            faces = np.append(faces, [[ny * (nx - 2) + i + 1, ny * (nx - 1) + i + 1, ny * (nx - 1) + i]], axis=0)
        
        for i in range(nx - 1):
            # Left side
            faces = np.append(faces, [[i * ny, (i + 1) * ny, (i + 1) * ny + ny - 1]], axis=0)
            faces = np.append(faces, [[i * ny, (i + 1) * ny + ny - 1, i * ny + ny - 1]], axis=0)
            
            # Right side
            faces = np.append(faces, [[(i + 1) * ny - 1, (i + 2) * ny - 1, i * ny - 1]], axis=0)
            faces = np.append(faces, [[(i + 2) * ny - 1, (i + 1) * ny, i * ny - 1]], axis=0)

        # Create the mesh
        mesh = trimesh.Trimesh(vertices=vertices.reshape(-1,3), faces=faces)

        # Save the mesh to an STL file
        mesh.export(stl_path)

    def generate_stl3(self, stl_path):
        # Open the image and convert to grayscale
        image = image = self.generate_image().convert('L')

        # Resize the image
        image = image.resize((600, 600), Image.ANTIALIAS)  # Change the size as needed

        # Convert the image to a numpy array
        data = np.array(image)

        # Normalize the data to the range [0, 255]
        data = data / np.max(data) * 255

        # Create a grid of points
        nx, ny = data.shape
        x = np.linspace(0, 200, nx)  # Scale to 20 cm
        y = np.linspace(0, 200, ny)  # Scale to 20 cm
        x, y = np.meshgrid(x, y)

        # Initialize an empty mesh
        mesh = pymesh.form_mesh(np.zeros((0,3)), np.zeros((0,3)))

        # Create a cube for each white pixel and add it to the mesh
        for i in range(nx):
            for j in range(ny):
                if data[i, j] > 128:  # If the pixel is white
                    # Create a cube
                    cube = pymesh.generate_box_mesh([x[i, j], y[i, j], 0], [x[i, j] + 200/nx, y[i, j] + 200/ny, 2])
                    # Add the cube to the mesh
                    mesh = pymesh.boolean(mesh, cube, operation='union')

        # Save the mesh to an STL file
        mesh.save(stl_path)

    
    def generate_stl(self, output_filename):
        """
        Convert a 2D image to a 3D STL file.
        """

        height = 20  # in mm
        width = 2000  # in mm (20 cm)
        length = 2000  # in mm (20 cm)

        # Get the 2D QR code image
        image = self.generate_image()

        # Convert the image to grayscale
        image = image.convert('L')
        image = image.resize((640, 640), Image.ANTIALIAS) 
        # image = ImageOps.invert(image)

        # Convert the image data to a numpy array
        data = np.array(image)

        # Scale the data to the desired height
        data = data / np.max(data) * height

        # Create a grid of points
        nx, ny = data.shape
        x = np.linspace(0, width, nx)
        y = np.linspace(0, length, ny)
        x, y = np.meshgrid(x, y)

        # Create a 3D surface
        vertices = np.zeros((nx * ny, 3))
        vertices[:, 0] = x.flatten()
        vertices[:, 1] = y.flatten()
        vertices[:, 2] = data.flatten()

        # Create the faces of the mesh
        faces = []
        for i in range(nx - 1):
            for j in range(ny - 1):
                # Two triangles forming a square
                faces.append([i * ny + j, (i + 1) * ny + j, i * ny + j + 1])
                faces.append([(i + 1) * ny + j, (i + 1) * ny + j + 1, i * ny + j + 1])
        faces = np.array(faces)

        # Create the mesh
        surface = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                surface.vectors[i][j] = vertices[f[j], :]

        # Write the mesh to file
        surface.save(output_filename)
        self.repair_mesh(output_filename)


    def repair_mesh(self, input_filename):
        # Load the mesh
        mesh = trimesh.load_mesh(input_filename)

        # Check if the mesh is watertight
        if not mesh.is_watertight:
            print("Mesh is not watertight! Attempting to repair...")

            # Attempt to repair the mesh
            mesh.fill_holes()
            mesh.remove_duplicate_faces()
            mesh.fix_normals()
            mesh.fix

            # Check if the mesh is now watertight
            if not mesh.is_watertight:
                print("Failed to repair mesh!")
            else:
                print("Mesh repaired successfully.")

        # Save the repaired mesh
        mesh.export(input_filename)
class IslandFinder:
    def __init__(self, matrix):
        self.matrix = matrix
        self.n = len(matrix)
        self.visited = [[False] * self.n for _ in range(self.n)]
        self.border = [[False] * self.n for _ in range(self.n)]
        self.bridges = [] # 0 - None or Angle 0 to 360
        for i in range(len(matrix)):
            self.border[i][0] = True
            self.border[i][len(self.matrix[i])-1] = True
        for j in range(len(matrix[0])):
            self.border[0][j] = True
        for j in range(len(matrix[len(matrix)-1])):
            self.border[len(matrix)-1][j] = True
            
        self.islands = []
        self.bridges_destination = []
    
    def select_bridges(self):
        for island in self.islands:
             for point in island:
                 x = point[0]
                 y = point[1]
                 
                 d1 = [x-1, y-1]
                 d2 = [x-1, y+1]
                 d3 = [x+1, y-1]
                 d4 = [x+1, y+1]
                 
                 if self.matrix[d1[0]][d1[1]]:
                    self.bridges_destination.append(d1)
                 elif self.matrix[d2[0]][d2[1]]:
                    self.bridges_destination.append(d2)
                 elif self.matrix[d3[0]][d3[1]]:
                     self.bridges_destination.append(d3)
                 elif self.matrix[d4[0]][d4[1]]:
                     self.bridges_destination.append(d4)
                 
                 
               
       
            
        
    def find_islands(self):
        def dfs(i, j, island):
            if i < 0 or i >= self.n or j < 0 or j >= self.n:
                return 
            if self.visited[i][j] or self.matrix[i][j]:
                return 

            self.visited[i][j] = True
            island.append((i, j))

            dfs(i + 1, j, island)
            dfs(i - 1, j, island)
            dfs(i, j + 1, island)
            dfs(i, j - 1, island)

        for i in range(1, self.n - 1):
            for j in range(1, self.n - 1):
                if not self.visited[i][j] and not self.matrix[i][j]:
                    island = []
                    dfs(i, j, island)
                    self.islands.append(island)

        filtered_islands = [item for item in self.islands if not self.has_borders(item)]
        self.islands = filtered_islands
        self.select_bridges()

    def has_borders(self, island):
        for i in range(len(island)-1): 
            pos = island[i]
            pos_i = pos[0]
            pos_j = pos[1]           
            if self.border[pos_i][pos_j]:
                return True
        return False;

    def is_bridge(self, i, j):
        if [i,j] in self.bridges_destination:
            return True
        return False         

    def is_island(self, i, j):
        for island in self.islands:
            if (i, j) in island:
                return True
        return False


        for island in self.islands:
            if (i, j) in island:
                return True
        return False