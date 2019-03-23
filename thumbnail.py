from PIL import Image as PIL_Image
from PyPDF2 import PdfFileWriter, PdfFileReader
from wand.image import Image as WAND_Image

fileDirectory = ''
inFileName = '1.pdf'

inputpdf = PdfFileReader(open(inFileName, 'rb'))
assert inputpdf.numPages > 0
output = PdfFileWriter()
output.addPage(inputpdf.getPage(0))
with open('document-page0.pdf', 'wb') as outputStream:
    output.write(outputStream)

outFileName = 'myOutputfile.png'
imageFromPdf = WAND_Image(filename='document-page0.pdf', resolution=300)
pages = len(imageFromPdf.sequence)
print(pages)
image = WAND_Image(
    width=imageFromPdf.width,
    height=imageFromPdf.height * pages
)
for i in range(pages):
    image.composite(
        imageFromPdf.sequence[i],
        top=imageFromPdf.height * i,
        left=0
    )
# image.background_color = Color('transparent')
# image.type = 'grayscale'
image.format = 'png'
image.save(filename=fileDirectory + outFileName)
# display(image)


img = PIL_Image.open(open(fileDirectory + outFileName, 'rb'))


def remove_transparency(im, bg_colour=(255, 255, 255)):
    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
        bg = PIL_Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im


img = remove_transparency(img)
img.save('hello_sir.png')
