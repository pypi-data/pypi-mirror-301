import argparse
import time
import random
from PIL import Image
from tqdm import tqdm


def splatter(args: argparse.Namespace):
    """
    Main function to create the splatter image.
    """
    # Validate scale factors
    if args.min_scale > args.max_scale:
        raise ValueError('Minimum scale cannot be greater than maximum scale.')

    # Set up wallpaper size
    if args.width and args.height:
        wallpaper_width = args.width
        wallpaper_height = args.height
    elif args.width:
        wallpaper_width = wallpaper_height = args.width
    elif args.height:
        wallpaper_width = wallpaper_height = args.height
    else:
        wallpaper_width = 1920
        wallpaper_height = 1080

    # Load the list of images
    try:
        input_images = [Image.open(image_path).convert('RGBA') for image_path in args.input_image]
    except Exception as e:
        raise IOError(f"Error loading input images: {e}")

    # Create the base image
    wallpaper = Image.new("RGBA", (wallpaper_width, wallpaper_height), (255, 255, 255, 0))

    # Iterate and place images
    for _ in tqdm(range(args.iterations), desc='Processing'):
        # Randomly pick an image from the list
        img = random.choice(input_images)

        # Randomly resize the image
        scale_factor = random.uniform(args.min_scale, args.max_scale)
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
        img_resized = img.resize(new_size, resample=Image.LANCZOS)

        # Randomly rotate the image
        rotation_angle = random.randint(0, 360)
        img_rotated = img_resized.rotate(rotation_angle, expand=True)

        # Random position (allow negative values to place images outside the canvas)
        pos_x = random.randint(-img_rotated.width, wallpaper_width)
        pos_y = random.randint(-img_rotated.height, wallpaper_height)

        # Paste the rotated image onto the wallpaper
        wallpaper.paste(img_rotated, (pos_x, pos_y), img_rotated)

    # Set output filename
    if args.output_image:
        output_filename = args.output_image
    else:
        timestamp = int(time.time())
        output_filename = f'splatter-{timestamp}.jpg'

    # Save the wallpaper
    wallpaper.convert('RGB').save(output_filename, quality=args.jpeg_quality)