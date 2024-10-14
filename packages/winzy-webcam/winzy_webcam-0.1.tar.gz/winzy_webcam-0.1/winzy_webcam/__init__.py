import winzy
import tempfile
import imageio
from datetime import datetime
import os


def get_filename_as_current_time():
    now = datetime.now()
    month = now.strftime("%b").upper() # Get month as uppercase abbreviation (APR)
    day = now.strftime("%d") # Get day as zero-padded string (09)
    year = now.strftime("%Y") # Get year (2024)
    hour = now.strftime("%H") # Get hour in 24-hour format (10)
    minute = now.strftime("%M") # Get minute as zero-padded string (25)
    seconds = now.strftime("%S") # get seconds as zero-padded string

    # Check for AM/PM
    meridian = "AM" if now.hour < 12 else "PM"

    filename = f"{month}_{day}_{year}_{hour}_{minute}_{seconds}_{meridian}.png"
    return filename


def get_image(filename):
    cap = imageio.get_reader("")
    # Capture frame-by-frame
    frame = cap.get_next_data()
    # Save the image to a file
    imageio.imsave(filename, frame)
    cap.close()
    print(filename)


def create_parser(subparser):
    parser = subparser.add_parser("webcam", description="Take image capture from webcam on laptop")
    # Add subprser arguments here.
    parser.add_argument("-p", "--path", default= tempfile.gettempdir(), help="Path where screenshot is saved.")
    return parser


class HelloWorld:
    """ An example plugin """
    __name__ = "webcam"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.hello)

    def webcam(self, args):
        get_image(os.path.join(args.path, get_filename_as_current_time()))
    
    def hello(self, args):
        # this routine will be called when "winzy "webcam is called."
        print("Hello! This is an example ``winzy`` plugin.")

webcam_plugin = HelloWorld()
