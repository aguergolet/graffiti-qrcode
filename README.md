# QRCode Stencil Generator

This repository houses a Python script that generates QRCode stencils for graffiti use. The script is designed to run in a web server container and it outputs two main results:

1. **PNG Image:** A black-and-white image of the QRCode, designed for printing and cutting with a utility knife. The image is engineered to maintain the integrity of the QRCode, ensuring it can be accurately scanned when painted.

2. **STL File:** A 3D model of the QRCode, suitable for 3D printing. The STL file can be loaded directly into a 3D slicer like Cura to be transformed into a 3D stencil.

The server will be available on my website at https://www.guergolet.art.br/qrcode-stencil.

## How It Works

The script uses a custom approach to turn a conventional QRCode into a stencil. The process is broken down into several steps:

1. Generate a QRCode from a supplied text.
2. Process the QRCode image to transform it into a stencil, preserving features that allow the code to be correctly scanned.
3. Save the stencil image as a PNG file.
4. Convert the stencil image into a 3D model and save it as an STL file.

The server runs in a container and uses both Python and OpenSCAD to generate the stencils.

Although this script has been specifically developed for creating QRCode stencils for graffiti, it can be adapted for other stencil applications. The approach used to create the stencil ensures the final QRCode will be scannable when applied, allowing for the effective incorporation of QRCodes into graffiti artworks.


## Code

1. `__init__`: This is the constructor of the `TLGCode` class. It initializes the `qr_code` attribute to `None`.

2. `generate_qr_code`: This method accepts a URL as input and generates a QR code for that URL.

3. `get_qr_code_matrix`: This method returns the matrix of the generated QR code. The matrix is a list of lists representing the black and white areas of the QR code.

4. `display_qr_code`: This method displays the generated QR code as an image.

5. `generate_image`: This method generates an image of the QR code, highlighting the identification areas (top-left, top-right, bottom-left, and bottom-right corners of the QR code).

6. `generate_stl`: This method generates an STL file (used for 3D printing) of the QR code. The STL file includes the QR code and the identification areas.

7. `get_identification_areas`: This method returns the coordinates of the identification areas in the QR code matrix.

The `TLGCode` class uses the following external Python libraries: `qrcode`, `PIL` (for image processing), `math`, `subprocess`, `uuid`, and `os`.

For the `template.scad` file, I understand that it's a template used by the library to generate the base `.scad` file, which is then converted into an STL file for 3D printing. I'll incorporate this information into the documentation.

Next, I will generate a basic structure for your documentation, including installation instructions, function descriptions, and usage examples based on my understanding of the code.
