from PIL import Image, ImageDraw, ImageColor, ImageFont
import os
import textwrap
import re

# Define gradient colors
gradient_colors = {
    '1': ('#2E3192', '#1BFFFF'),
    '2': ('#D4145A', '#FBB03B'),
    '3': ('#009245', '#FCEE21'),
    '4': ('#662D8C', '#ED1E79'),
    '5': ('#EE9CA7', '#FFDDE1'),
    '6': ('#614385', '#516395'),
    '7': ('#02AABD', '#00CDAC'),
    '8': ('#FF512F', '#DD2476'),
    '9': ('#FF5F6D', '#FFC371'),
    '10': ('#11998E', '#38EF7D'),
    '11': ('#C6EA8D', '#FE90AF'),
    '12': ('#EA8D8D', '#A890FE'),
    '13': ('#D8B5FF', '#1EAE98'),
    '14': ('#FF61D2', '#FE9090'),
    '15': ('#BFF098', '#6FD6FF'),
    '16': ('#4E65FF', '#92EFFD'),
    '17': ('#A9F1DF', '#FFBBBB'),
    '18': ('#C33764', '#1D2671'),
    '19': ('#93A5CF', '#E4EfE9'),
    '20': ('#868F96', '#596164'),
    '21': ('#09203F', '#537895'),
    '22': ('#FFECD2', '#FCB69F'),
    '23': ('#A1C4FD', '#C2E9FB'),
    '24': ('#764BA2', '#667EEA'),
    '25': ('#FDFCFB', '#E2D1C3')
}

# Define path to custom font
def get_custom_font():
    font_path = '/storage/emulated/0/Download/BebasNeue-Regular.ttf'
    font_size = 40  # Adjust the font size as needed
    return ImageFont.truetype(font_path, font_size)

# Define text colors including gold and silver
text_colors = {
    '1': 'black',
    '2': 'white',
    '3': '#FF0000',  # Red
    '4': '#00FF00',  # Green
    '5': '#0000FF',  # Blue
    '6': '#FFD700',  # Gold
    '7': '#C0C0C0'   # Silver
}

def draw_rectangle(aspect_ratio, color, output_filename, texts, text_color, text_effect):
    # Set predefined width and calculate height based on aspect ratio
    if aspect_ratio == "1:1":
        width, height = 500, 500
    elif aspect_ratio == "9:16":
        width, height = 500, 500 * 16 // 9
    else:
        raise ValueError("Invalid aspect ratio")

    # Create a blank image with the chosen background color
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Draw a rectangle with the selected color
    if color == '1':
        draw.rectangle([(0, 0), (width - 1, height - 1)], outline='black', fill='black')
    elif color == '2':
        draw.rectangle([(0, 0), (width - 1, height - 1)], outline='white', fill='white')
    elif color in gradient_colors:
        start_color, end_color = gradient_colors[color]
        for i in range(width):
            r1, g1, b1 = ImageColor.getrgb(start_color)
            r2, g2, b2 = ImageColor.getrgb(end_color)
            r = int(r1 + (r2 - r1) * i / width)
            g = int(g1 + (g2 - g1) * i / width)
            b = int(b1 + (b2 - b1) * i / width)
            draw.line([(i, 0), (i, height)], fill=(r, g, b))

    # Load the custom font
    font = get_custom_font()

    # Function to wrap text
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            if draw.textbbox((0, 0), test_line, font=font)[2] <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        lines.append(line.strip())
        return lines

    # Calculate text positioning
    margin = 20  # Margin around text
    line_spacing = 10  # Space between lines of text

    def draw_text_with_effects(draw, text, position, font, color, effect):
        if effect == 'shadow':
            shadow_offset = (2, 2)
            shadow_color = 'black'
            # Draw shadow
            shadow_position = (position[0] + shadow_offset[0], position[1] + shadow_offset[1])
            draw.text(shadow_position, text, font=font, fill=shadow_color)
        # Draw main text
        draw.text(position, text, font=font, fill=color)

    for text in texts:
        wrapped_lines = wrap_text(text, font, width - 2 * margin)  # Margin of 20 pixels on each side
        line_height = draw.textbbox((0, 0), wrapped_lines[0], font=font)[3] - draw.textbbox((0, 0), wrapped_lines[0], font=font)[1]
        total_text_height = line_height * len(wrapped_lines) + (len(wrapped_lines) - 1) * line_spacing
        text_y = (height - total_text_height) / 2

        for line in wrapped_lines:
            text_width = draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0]
            text_x = (width - text_width) / 2
            draw_text_with_effects(draw, line, (text_x, text_y), font, text_colors[text_color], text_effect)
            text_y += line_height + line_spacing

    # Ensure output directory exists
    output_dir = "/storage/emulated/0/MyAppImages/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the image in PNG format with high quality
    output_path = os.path.join(output_dir, output_filename)
    img.save(output_path, 'PNG', dpi=(300, 300))  # Save with DPI for higher quality
    print(f"Image saved as {output_path}")

# Function to remove numbers from quotes
def clean_quote(quote):
    # Remove leading numbers and periods
    return re.sub(r'^\d+\.\s*', '', quote).strip()

def generate_images():
    # Show options to select aspect ratio
    print("Select the aspect ratio:")
    print("1. 1:1")
    print("2. 9:16")
    aspect_ratio_choice = input("Enter your choice (1 or 2): ")
    aspect_ratio = "1:1" if aspect_ratio_choice == "1" else "9:16"

    # Show options to select color
    print("Select the color:")
    print("1. Black")
    print("2. White")
    print("3. Gradient 1")
    print("4. Gradient 2")
    print("5. Gradient 3")
    print("6. Gradient 4")
    print("7. Gradient 5")
    print("8. Gradient 6")
    print("9. Gradient 7")
    print("10. Gradient 8")
    print("11. Gradient 9")
    print("12. Gradient 10")
    print("13. Gradient 11")
    print("14. Gradient 12")
    print("15. Gradient 13")
    print("16. Gradient 14")
    print("17. Gradient 15")
    print("18. Gradient 16")
    print("19. Gradient 17")
    print("20. Gradient 18")
    print("21. Gradient 19")
    print("22. Gradient 20")
    print("23. Gradient 21")
    print("24. Gradient 22")
    print("25. Gradient 23")
    print("26. Gradient 24")
    print("27. Gradient 25")
    color_choice = input("Enter your choice (1-27): ")

    # Show options to select text color
    print("Select the text color:")
    print("1. Black")
    print("2. White")
    print("3. Red")
    print("4. Green")
    print("5. Blue")
    print("6. Gold")
    print("7. Silver")
    text_color_choice = input("Enter your choice (1-7): ")
    
    # Show options to select text effect
    print("Select the text effect:")
    print("1. None")
    print("2. Shadow")
    text_effect_choice = input("Enter your choice (1 or 2): ")
    text_effect = 'shadow' if text_effect_choice == "2" else 'none'

    # Get quotes from the user
    print("Enter each quote and press Enter. Type 'DONE' when finished.")
    quotes = []
    while True:
        quote = input()
        if quote.upper() == 'DONE':
            break
        quotes.append(clean_quote(quote))  # Clean quotes before adding

    # Choose image generation mode
    print("Do you want to add text to:")
    print("1. All gradient images")
    print("2. Just the selected gradient image")
    option_choice = input("Enter your choice (1 or 2): ")

    if option_choice == "1":
        # Generate images for all gradients with each quote
        for grad_choice in gradient_colors.keys():
            for idx, quote in enumerate(quotes):
                output_filename = f"rectangle_{aspect_ratio.replace(':', 'x')}_gradient{grad_choice}_quote{idx + 1}.png"
                draw_rectangle(aspect_ratio, grad_choice, output_filename, [quote], text_color_choice, text_effect)
    elif option_choice == "2":
        # Generate images for selected gradient with each quote
        for idx, quote in enumerate(quotes):
            output_filename = f"rectangle_{aspect_ratio.replace(':', 'x')}_gradient{color_choice}_quote{idx + 1}.png"
            draw_rectangle(aspect_ratio, color_choice, output_filename, [quote], text_color_choice, text_effect)
    else:
        print("Invalid choice.")

generate_images()
