import winzy
from PIL import Image, ImageDraw, ImageFont
import os
import tempfile
import sys

def add_text_to_image(image_path, text, font_size=24, padding=10):
    # Open the image
    with Image.open(image_path) as img:
    # Create a drawing object
        draw = ImageDraw.Draw(img)
        # Load a default font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
            # Get image dimensions
            img_width, img_height = img.size
            # Get text dimensions

        max_font_size = 200
        # avg_dimension = (img_width + img_height) / 2
        font_size = max_font_size
        while True:
            font = ImageFont.truetype("arial.ttf", font_size)
            text_bbox = draw.textbbox((0,0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            if text_width + text_height < 0.7 * img_width and text_height < 0.2 * img_height:
                break
            font_size -= 1
            if font_size <= 0:
                raise ValueError("Text too long for image size")

        # Calculate position (lower left corner with padding) 
        position = (padding, img_height - text_height - padding) 
        # Add text to image 
        draw.text(position, text, font=font, fill=(255, 255, 255))
        # White text 
        # Generate new filename 
        temp_dir = tempfile.gettempdir()
        filename, ext = os.path.splitext(os.path.basename(image_path))
        new_filename = os.path.join(temp_dir, f"{filename}_with_text{ext}")
        # Save the new image 
        img.save(new_filename)
    return new_filename

def create_parser(subparser):
    parser = subparser.add_parser("txtonimg", description="Add text to an image.")
    # Add subprser arguments here.
    parser.add_argument("-i","--image_path", type=str, help="Path to the image.", required=True)
    parser.add_argument("text", type=str, nargs="*", help="Text to be added.")
    parser.add_argument("-f", "--font-size", type=int, help="Font size, Default %(default)s", default=24)
    parser.add_argument("-p", "--padding", type=int, help="Padding to use. Default %(default)s", default=100)
    return parser


class HelloWorld:
    """ An example plugin """
    __name__ = "txtonimg"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.run)
    
    def run(self, args):
        if not args.text:
            text= sys.stdin.read()
        else:
            text=" ".join(args.text)
        file_name =add_text_to_image(args.image_path, text, args.font_size, args.padding)
        print(file_name)
        
    def hello(self, args):
        # this routine will be called when "winzy "txtonimg is called."
        print("Hello! This is an example ``winzy`` plugin.")

txtonimg_plugin = HelloWorld()
