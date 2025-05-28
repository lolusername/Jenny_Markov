import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_touchscreen
import math
import random
import time
import gc

# Initialize display
display = board.DISPLAY

# Initialize touchscreen
ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL, board.TOUCH_XR,
    board.TOUCH_YD, board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(display.width, display.height)
)

# Read quotes and build Markov chain with weights
def build_word_chain():
    chain = {}
    first_words = {}  # Changed to dict to track frequencies
    
    with open("/quotes.txt", "r") as f:
        for line in f:
            words = line.strip().split()
            if not words:
                continue
                
            # Store first word with frequency
            first_word = words[0]
            if first_word not in first_words:
                first_words[first_word] = 0
            first_words[first_word] += 1
            
            # Build chain with frequencies
            for i in range(len(words) - 1):
                current = words[i]
                next_word = words[i + 1]
                
                if current not in chain:
                    chain[current] = {}
                
                if next_word not in chain[current]:
                    chain[current][next_word] = 0
                chain[current][next_word] += 1
            
            # Add end marker with frequency
            last = words[-1]
            if last not in chain:
                chain[last] = {}
            if '<end>' not in chain[last]:
                chain[last]['<end>'] = 0
            chain[last]['<end>'] += 1
    
    return chain, first_words

# Choose next word based on weights
def weighted_choice(choices):
    total = sum(choices.values())
    r = random.uniform(0, total)
    running_sum = 0
    
    for word, weight in choices.items():
        running_sum += weight
        if running_sum > r:
            return word
    
    return list(choices.keys())[0]  # Fallback

# Generate a new quote using weighted Markov chain
def generate_quote(chain, first_words):
    # Choose first word based on its frequency
    word = weighted_choice(first_words)
    quote = [word]
    
    # Generate quote with reasonable length limits
    while len(quote) < 15:  # Max 15 words for screen space
        if word not in chain or not chain[word]:
            break
            
        word = weighted_choice(chain[word])
        if word == '<end>':
            break
            
        quote.append(word)
    
    return ' '.join(quote)

def wrap_text(text, width, font, scale):
    """Wrap text to fit given width."""
    words = text.split()
    lines = []
    current_line = []
    current_width = 0
    
    for word in words:
        word_width = (len(word) + 1) * 6 * scale
        
        if current_width + word_width <= width:
            current_line.append(word)
            current_width += word_width
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_width = len(word) * 6 * scale
    
    if current_line:
        lines.append(" ".join(current_line))
    
    return "\n".join(lines)

# Build Markov chain
print("Building Markov chain...")
word_chain, first_words = build_word_chain()
gc.collect()  # Clean up memory after building chain

# Create the main display group
main_group = displayio.Group()

# Create quote text with line wrapping
quote_text = label.Label(
    terminalio.FONT,
    text="",
    color=0xFFFFFF,
    scale=2,
    anchor_point=(0.5, 0.5),
    anchored_position=(display.width // 2, display.height // 3),
    line_spacing=1.25
)

# Create coordinate display text
coord_text = label.Label(
    terminalio.FONT,
    text="",
    color=0xFFFFFF,
    scale=2,
    anchor_point=(0.5, 0.5),
    anchored_position=(display.width // 2, display.height * 4 // 5)
)

# Create multiple scan lines with different intensities
NUM_SCAN_LINES = 2  # Reduced to 2 lines for clearer effect
scan_lines = []
scan_colors = [0x444444, 0x333333]  # Made colors lighter to be more visible
line_width = (display.width - 20) // 12

for i in range(NUM_SCAN_LINES):
    line = label.Label(
        terminalio.FONT,
        text="█" * line_width,  # Using solid block for more visible effect
        color=scan_colors[i],
        scale=2,
        anchor_point=(0.5, 0.5),
        anchored_position=(display.width // 2, 0)
    )
    scan_lines.append(line)
    main_group.append(line)

# Set initial quote
initial_quote = generate_quote(word_chain, first_words)
quote_text.text = wrap_text(initial_quote, display.width - 20, terminalio.FONT, 2)

# Add text to display group
main_group.append(quote_text)
main_group.append(coord_text)

# Show it
display.root_group = main_group

def hsv_to_rgb(h, s, v):
    """Convert HSV color to RGB color."""
    h = (h % 360) / 360
    s = min(1, max(0, s))
    v = min(1, max(0, v))
    
    if s == 0:
        return v, v, v

    i = int(h * 6)
    f = (h * 6) - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    i = i % 6

    if i == 0:
        return v, t, p
    elif i == 1:
        return q, v, p
    elif i == 2:
        return p, v, t
    elif i == 3:
        return p, q, v
    elif i == 4:
        return t, p, v
    else:
        return v, p, q

# Keep the code running and update coordinates on screen
last_color = 0xFFFFFF
last_touch_time = 0
touch_threshold = 0.5

def apply_crt_effect(color, time_val):
    """Apply a more aesthetic CRT effect to color."""
    # Subtle color shift based on time
    shift = math.sin(time_val * 2) * 0.1
    r = ((color >> 16) & 0xFF)
    g = ((color >> 8) & 0xFF)
    b = (color & 0xFF)
    
    # Add slight color bleeding
    if shift > 0:
        r = int(r * (1 + shift))
        b = int(b * (1 - shift * 0.5))
    else:
        b = int(b * (1 - shift))
        r = int(r * (1 + shift * 0.5))
        
    # Add subtle phosphor glow effect
    glow = 0.85 + 0.15 * math.sin(time_val * 3)
    r = int(r * glow)
    g = int(g * glow)
    b = int(b * glow)
    
    # Clamp values
    r = min(255, max(0, r))
    g = min(255, max(0, g))
    b = min(255, max(0, b))
    
    return (r << 16) | (g << 8) | b

while True:
    gc.collect()
    p = ts.touch_point
    current_time = time.monotonic()
    
    # Update scan lines with slower, more visible motion
    for i, line in enumerate(scan_lines):
        offset = i * (display.height // NUM_SCAN_LINES)
        y = int((current_time * 15 + offset) % display.height)  # Slowed down movement
        line.anchored_position = (display.width // 2, y)
    
    if p:
        x, y, _ = p
        coord_text.text = f"creating a 'new' truism"
        
        # Generate new quote on touch with time threshold
        if current_time - last_touch_time > touch_threshold:
            new_quote = generate_quote(word_chain, first_words)
            quote_text.text = wrap_text(new_quote, display.width - 20, terminalio.FONT, 2)
            last_touch_time = current_time
            gc.collect()  # Clean up memory after generating quote
        
        # Map x position to hue (0-360 degrees)
        hue = (x / display.width) * 360
        r, g, b = hsv_to_rgb(hue, 1.0, 1.0)
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        
        color = (r << 16) | (g << 8) | b
        last_color = color
        quote_text.color = color
    else:
        coord_text.text = ""
    
    # Apply CRT effect
    effect_color = apply_crt_effect(last_color, current_time)
    quote_text.color = effect_color
    coord_text.color = effect_color
    
    time.sleep(0.05)