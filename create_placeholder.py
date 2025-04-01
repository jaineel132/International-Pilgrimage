import os
from PIL import Image, ImageDraw, ImageFont
from app import create_app

def create_placeholder_image():
    # Create static/images directory if it doesn't exist
    app = create_app()
    with app.app_context():
        static_dir = os.path.join(app.root_path, 'static', 'images')
        os.makedirs(static_dir, exist_ok=True)
        
        # Create a placeholder image
        width, height = 800, 600
        image = Image.new('RGB', (width, height), color=(200, 200, 200))
        
        # Add text
        draw = ImageDraw.Draw(image)
        text = "Pilgrimage Image"
        
        # Try to use a font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            font = ImageFont.load_default()
            
        # Calculate text position to center it
        text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (200, 40)
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Draw text
        draw.text(position, text, fill=(100, 100, 100), font=font)
        
        # Save the image
        image.save(os.path.join(static_dir, 'placeholder.jpg'))
        print("Placeholder image created successfully.")

if __name__ == "__main__":
    create_placeholder_image()

