"""
Convert a photo to cleaner ASCII art for GitHub profile README.
Optimized for monospace code blocks on GitHub dark theme.
"""
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import sys

# Ordered from darkest to lightest - carefully chosen for visual quality
ASCII_DARK_TO_LIGHT = "@$#%&8BWM*mwqpdbkhaoOQZC0UYXJ/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def image_to_ascii(image_path, width=45):
    """Convert an image to high-quality ASCII art."""
    img = Image.open(image_path)
    
    # Crop the black border
    w, h = img.size
    border_x = int(w * 0.07)
    border_y = int(h * 0.04)
    img = img.crop((border_x, border_y, w - border_x, h - border_y))
    
    # Auto-adjust levels 
    img = ImageOps.autocontrast(img, cutoff=2)
    
    # Slight blur to reduce noise artifacts in ASCII
    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.4)
    
    # Enhance brightness slightly (lighter = cleaner ASCII)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)
    
    # Calculate dimensions
    w, h = img.size
    aspect_ratio = h / w
    new_height = int(width * aspect_ratio * 0.47)
    
    # Resize with high-quality resampling
    img = img.resize((width, new_height), Image.LANCZOS)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Invert for dark background (GitHub dark theme) - dark areas get dense chars
    # Actually for code blocks on dark theme, we want: 
    # dark skin/hair = dense characters (they show as light text on dark bg)
    # light background = sparse characters (spaces)
    # So we DON'T invert - dark pixels -> dense chars is correct
    
    chars = ASCII_DARK_TO_LIGHT
    
    # Map pixels to ASCII
    pixels = list(img.getdata())
    ascii_lines = []
    for row in range(new_height):
        line = ""
        for col in range(width):
            pixel = pixels[row * width + col]
            # Map 0(black) -> dense chars, 255(white) -> space
            idx = int(pixel / 255 * (len(chars) - 1))
            line += chars[idx]
        ascii_lines.append(line)
    
    return ascii_lines


def format_neofetch(ascii_lines, info_lines, gap=3):
    """Combine ASCII art with info text side-by-side."""
    max_w = max(len(l) for l in ascii_lines)
    padded = [l.ljust(max_w) for l in ascii_lines]
    
    sep = " " * gap
    result = []
    total = max(len(padded), len(info_lines))
    
    for i in range(total):
        art = padded[i] if i < len(padded) else " " * max_w
        info = info_lines[i] if i < len(info_lines) else ""
        result.append(f"  {art}{sep}{info}")
    
    return result


def main():
    image_path = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 45
    
    ascii_lines = image_to_ascii(image_path, width=width)
    
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
    
    # Write the full output
    output_file = "ascii_art_output.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for line in combined:
            f.write(line + "\n")
    
    # Also print
    for line in combined:
        print(line)
    
    print(f"\n--- Saved to {output_file} ---")
    print(f"--- ASCII art is {len(ascii_lines)} lines x {width} chars ---")


if __name__ == "__main__":
    main()
