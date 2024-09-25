from PIL import Image

def resize_with_padding_and_buffer(image_path, output_path, target_width, target_height, buffer_percent=0.05):
    # Open the image file
    img = Image.open(image_path).convert("RGBA")
    
    # Get the original dimensions
    original_width, original_height = img.size
    
    # Calculate the aspect ratios
    target_aspect = target_width / target_height
    original_aspect = original_width / original_height
    
    # Resize image while maintaining aspect ratio
    if original_aspect > target_aspect:  # Wider than target
        new_width = target_width
        new_height = int(target_width / original_aspect)
    else:  # Taller than target
        new_height = target_height
        new_width = int(target_height * original_aspect)
    
    # Resize the image
    img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)
    
    # Calculate buffer size (5% on each side)
    buffer_width = int(target_width * buffer_percent)
    buffer_height = int(target_height * buffer_percent)
    
    # New target dimensions with buffer
    final_width = target_width + 2 * buffer_width
    final_height = target_height + 2 * buffer_height
    
    # Create a new image with transparent background and buffers
    new_img = Image.new("RGBA", (final_width, final_height), (0, 0, 0, 0))
    
    # Calculate padding (center the resized image with buffer)
    pad_left = (final_width - new_width) // 2
    pad_top = (final_height - new_height) // 2
    
    # Paste the resized image onto the new transparent background
    new_img.paste(img_resized, (pad_left, pad_top))
    
    # Save the result
    new_img.save(output_path, "PNG")
    print(f"Image saved at {output_path}")

# Example usage
resize_with_padding_and_buffer(
    image_path="img/tonal-logo.png",
    output_path="img/tonal-logo-resized.png",
    target_width=738,
    target_height=661,
    buffer_percent=0.12
)
