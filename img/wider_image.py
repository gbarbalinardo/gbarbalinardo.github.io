from PIL import Image

def make_image_wider_and_taller(image_path, output_path, width_percentage):
    # Open the original image
    img = Image.open(image_path)

    # Calculate the new width and height
    added_width = int(img.width * (width_percentage / 100))
    added_height = int(img.height * (width_percentage / 2 / 100))
    new_width = img.width + added_width
    new_height = img.height + added_height

    # Create a new transparent image with the new dimensions
    new_img = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))

    # Calculate the position to paste the original image in the center horizontally
    # and keep it at the top vertically
    x_offset = (new_width - img.width) // 2
    y_offset = 0  # Keep the image at the top of the new canvas

    # Paste the original image onto the new image
    new_img.paste(img, (x_offset, y_offset))

    # Save the new image
    new_img.save(output_path, format="PNG")


# Example usage
make_image_wider_and_taller("img/input_image.png", "img/profile.png", 30)  # Increase width by 50%
