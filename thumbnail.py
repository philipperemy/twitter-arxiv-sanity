import os
import tempfile

import wget
from PIL import Image as PIL_Image
from PyPDF2 import PdfFileWriter, PdfFileReader
from wand.image import Image as WAND_Image


def pdf_to_thumbnail(pdf_url_path='https://arxiv.org/pdf/1902.10162v2.pdf', output_image_filename='out.png'):
    tmp_dir = tempfile.gettempdir()
    wget_output = os.path.join(tmp_dir, 'out_wget.pdf')
    wget.download(pdf_url_path, out=wget_output)
    input_pdf = PdfFileReader(open(wget_output, 'rb'))
    assert input_pdf.numPages > 0
    output = PdfFileWriter()
    output.addPage(input_pdf.getPage(0))
    wget_output_1page = os.path.join(tmp_dir, 'out_wget_1page.pdf')
    with open(wget_output_1page, 'wb') as outputStream:
        output.write(outputStream)

    image_from_df = WAND_Image(filename=wget_output_1page, resolution=300)
    pages = len(image_from_df.sequence)
    # print(pages)
    image = WAND_Image(
        width=image_from_df.width,
        height=image_from_df.height * pages
    )
    for i in range(pages):
        image.composite(
            image_from_df.sequence[i],
            top=image_from_df.height * i,
            left=0
        )
    # image.background_color = Color('transparent')
    # image.type = 'grayscale'
    image.format = 'png'
    img_output_transparent = os.path.join(tmp_dir, 'out_wget_1page.png')
    image.save(filename=img_output_transparent)
    # display(image)

    img = PIL_Image.open(open(img_output_transparent, 'rb'))

    def remove_transparency(im, bg_colour=(255, 255, 255)):
        # Only process if image has transparency (http://stackoverflow.com/a/1963146)
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

            # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
            alpha = im.convert('RGBA').split()[-1]

            # Create a new background image of our matt color.
            # Must be RGBA because paste requires both images have the same format
            # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
            bg = PIL_Image.new('RGBA', im.size, bg_colour + (255,))
            bg.paste(im, mask=alpha)
            return bg

        else:
            return im

    img = remove_transparency(img)
    img.save(output_image_filename)


if __name__ == '__main__':
    pdf_to_thumbnail()
