"""
Convert a photo to color ASCII art for GitHub profile README.
Removes background and uses ANSI escape codes for colors in markdown.
"""
from PIL import Image, ImageEnhance, ImageOps, ImageDraw, ImageFilter
import sys

# Characters for density
ASCII_CHARS = "@$#%&8BWM*mwqpdbkhaoOQZC0UYXJ/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def rgb_to_ansi(r, g, b):
    """Convert RGB to ANSI 24-bit color escape sequence."""
    return f"\x1b[38;2;{r};{g};{b}m"

def image_to_ansi_ascii(image_path, width=45):
    """Convert image to ANSI colored ASCII art with transparent background."""
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size
    
    # Create an elliptical mask to isolate the face and remove the background
    # The face is usually in the center, slightly towards the top
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    
    # Define an ellipse for the face (approximate based on standard portrait)
    # left, top, right, bottom
    ellipse_box = (
        int(w * 0.15), 
        int(h * 0.15), 
        int(w * 0.85), 
        int(h * 0.85)
    )
    draw.ellipse(ellipse_box, fill=255)
    
    # Blur the mask for a soft edge
    mask = mask.filter(ImageFilter.GaussianBlur(radius=int(w * 0.05)))
    
    # Apply the mask to the alpha channel
    r, g, b, a = img.split()
    a = Image.composite(a, Image.new("L", a.size, 0), mask)
    img = Image.merge("RGBA", (r, g, b, a))
    
    # Crop to the mask area
    img = img.crop(ellipse_box)
    
    # Enhance slightly for better visibility
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.3)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)
    
    # Calculate dimensions
    w, h = img.size
    aspect_ratio = h / w
    # Adjust aspect ratio for terminal font character proportions (typically ~0.45-0.5)
    new_height = int(width * aspect_ratio * 0.47)
    
    img = img.resize((width, new_height), Image.LANCZOS)
    
    ascii_lines = []
    # For GitHub markdown `ansi` code blocks, we need a reset at the end of colored segments
    ansi_reset = "\x1b[0m"
    
    for y in range(new_height):
        line = ""
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            
            # If transparent (removed background), output a space
            if a < 50:
                line += " "
            else:
                # Convert to grayscale for character selection (brightness)
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                # Map grayscale (0-255) to index in ASCII_CHARS
                # darker pixels -> denser characters
                idx = int((gray / 255) * (len(ASCII_CHARS) - 1))
                char = ASCII_CHARS[idx]
                
                # Apply color
                line += f"{rgb_to_ansi(r, g, b)}{char}"
        
        # Add reset at end of line to prevent color bleeding
        ascii_lines.append(line + ansi_reset)
        
    return ascii_lines

def format_neofetch(ascii_lines, info_lines, gap=3):
    """Combine colored ASCII art with info text side-by-side."""
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    
    max_visual_width = max(len(ansi_escape.sub('', line)) for line in ascii_lines) if ascii_lines else 0
    
    sep = " " * gap
    result = []
    total = max(len(ascii_lines), len(info_lines))
    
    for i in range(total):
        if i < len(ascii_lines):
            art = ascii_lines[i]
            visual_len = len(ansi_escape.sub('', art))
            padding = " " * (max_visual_width - visual_len)
            art_padded = art + padding
        else:
            art_padded = " " * max_visual_width
            
        info = info_lines[i] if i < len(info_lines) else ""
        
        # Reset color before the separator and info text just to be safe
        result.append(f"  {art_padded}\x1b[0m{sep}{info}")
    
    return result

def main():
    image_path = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    
    print(f"Processing image {image_path} with width {width}...")
    ascii_lines = image_to_ansi_ascii(image_path, width=width)
    
    info_lines = [
        "shashikant@github ─────────────────────────────",
        "",
        "OS: ........................ Windows 11, Linux",
        "Uptime: .............. 2+ years in Data & AI",
        "Host: .................. CoderCops (Tech Ops)",
        "Kernel: ............ Data Analyst & AI/ML Dev",
        "IDE: ......... VS Code, Jupyter, IntelliJ IDEA",
        "Resolution: ............ 1920x1080, always",
        "Shell: .................. PowerShell, Bash",
        "",
        "Languages.Programming: ...... Python, SQL, DAX",
        "Languages.Viz_&_BI: ... Power BI, Tableau, Looker",
        "Languages.Computer: ... HTML, CSS, JSON, YAML",
        "Languages.Real: ........... English, Hindi",
        "",
        "Hobbies.Data: .. Analytics, ML, Dashboarding",
        "Hobbies.Cloud: ................ AWS, Azure, GCP",
        "Hobbies.Automation: ....... Workflow, Pipeline",
        "",
        "─ Contact ──────────────────────────────────────",
        "Email: ........... shashikantgupta163@gmail.com",
        "LinkedIn: .... in/shashikant-gupta-0b7799254",
        "GitHub: .................. Shasikantgupta",
        "",
        "─ GitHub Stats ─────────────────────────────────",
        "Repos: ...... 12  |  Stars: ................ 7",
        "Followers: ... 0  |  Following: ............ 1",
        "Badge: .......................... ⭐ Pro",
    ]
    
    combined = format_neofetch(ascii_lines, info_lines, gap=3)
    
    output_file = "ascii_art_color_output.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        # We don't write the ```ansi here because we will inject it in the main README
        for line in combined:
            f.write(line + "\n")
    
    print(f"--- Saved to {output_file} ---")
    print(f"--- ASCII art is {len(ascii_lines)} lines x {width} visible chars ---")

if __name__ == "__main__":
    main()
