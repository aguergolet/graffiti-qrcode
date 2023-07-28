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
