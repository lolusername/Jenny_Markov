# Jenny Markov - Interactive Digital Art Installation

A generative art installation that combines Markov chain text generation with interactive CRT-style visual effects, running on an Adafruit PyPortal Titano. This project creates an engaging, ever-evolving display of philosophical statements that respond to user interaction through touch and visual effects.

## Technical Overview

### Hardware Requirements
- Adafruit PyPortal Titano
- Touchscreen display
- Power supply

### Software Components
- CircuitPython
- Required Libraries:
  - `board`
  - `displayio`
  - `terminalio`
  - `adafruit_display_text`
  - `adafruit_touchscreen`

## How It Works

### Understanding Markov Chains: The Art of Generative Text
The installation uses Markov chains to create new philosophical statements that maintain the style and tone of the original quotes. Here's how this mathematical concept becomes an artistic tool:

1. **What is a Markov Chain?**
   - A Markov chain is a mathematical system that predicts the next state based only on the current state
   - In our case, it predicts the next word based on the current word
   - It's like having a conversation where each word influences the next, but not the entire history
   - This creates text that feels natural while being completely new

2. **How It Works in the Installation**
   ```
   Original Quote: "A LITTLE KNOWLEDGE CAN GO A LONG WAY"
   
   The chain learns:
   - "A" → "LITTLE" (100% chance)
   - "LITTLE" → "KNOWLEDGE" (100% chance)
   - "KNOWLEDGE" → "CAN" (100% chance)
   - "CAN" → "GO" (100% chance)
   - "GO" → "A" (100% chance)
   - "A" → "LONG" (100% chance)
   - "LONG" → "WAY" (100% chance)
   ```

3. **The Weighted System**
   - Each word connection has a "weight" based on how often it appears
   - For example, if "A" is followed by "LITTLE" 10 times and "POSITIVE" 5 times:
     ```
     "A" → "LITTLE" (weight: 10)
     "A" → "POSITIVE" (weight: 5)
     ```
   - This means "LITTLE" is twice as likely to follow "A" as "POSITIVE"
   - The system preserves the natural flow of the original text

4. **The Artistic Process**
   - The system reads all quotes and builds a probability map
   - It tracks:
     - Which words start sentences
     - Which words follow each other
     - How often each transition occurs
   - When generating new text:
     - Starts with a common first word
     - Uses the probability map to choose each next word
     - Continues until reaching a natural end or length limit

5. **Why This Matters**
   - Creates text that feels familiar yet new
   - Maintains the philosophical tone of the original quotes
   - Each generated statement is unique but coherent
   - The system learns the "style" of the original text
   - Creates an endless stream of new philosophical statements

6. **Example Generation**
   ```
   Original Quotes:
   - "A LITTLE KNOWLEDGE CAN GO A LONG WAY"
   - "A POSITIVE ATTITUDE MEANS ALL THE DIFFERENCE"
   
   Possible Generated Output:
   "A LITTLE ATTITUDE CAN MEANS A LONG DIFFERENCE"
   ```
   The generated text maintains the structure and style while creating new combinations.

This use of Markov chains transforms the original philosophical statements into a living, evolving artwork. Each interaction with the installation creates new combinations of words, new philosophical statements, and new ways of thinking about the original ideas. It's like having a conversation with the original text, where each response is both familiar and surprising.

### Text Generation
The installation uses a weighted Markov chain algorithm to generate new philosophical statements from a curated collection of quotes. The system:
- Analyzes word relationships in the source text
- Maintains frequency weights for word transitions
- Generates new statements while preserving the style and tone of the original quotes
- Limits output to 15 words for optimal display

### Visual Effects
The display features several artistic elements:
1. **CRT-Style Effects**
   - Dynamic color shifting
   - Phosphor glow simulation
   - Subtle color bleeding
   - Scan line animation

2. **Interactive Elements**
   - Touch-responsive color changes
   - Dynamic text wrapping
   - Smooth transitions between states

### Memory Management
- Implements garbage collection for optimal performance
- Efficient data structures for Markov chain storage
- Optimized display updates

## Artistic Statement

This installation explores the intersection of:
- Generative text art
- Interactive media
- Retro computing aesthetics
- Philosophical inquiry

The piece creates a dialogue between human interaction and algorithmic generation, where each touch transforms both the visual and textual elements of the display.

## Technical Implementation Details

### PyPortal Titano Hardware Specifications
- **Display**: 3.5" 480x320 TFT display with capacitive touch
- **Processor**: ATSAMD51J20 (120MHz ARM Cortex-M4)
- **Memory**: 512KB Flash, 192KB RAM
- **Storage**: 2MB QSPI Flash
- **Power**: 5V DC input with 3.3V logic level
- **Touch Interface**: FT6206 capacitive touch controller
- **Display Interface**: ILI9488 TFT driver with 16-bit color depth

### Color Management System
The installation implements an efficient color management system that balances visual quality with performance:

1. **HSV to RGB Conversion**
   - Custom optimized HSV to RGB conversion algorithm
   - Direct bit manipulation for color component extraction
   - Efficient color space transformations using bit shifts
   ```python
   def hsv_to_rgb(h, s, v):
       h = (h % 360) / 360
       i = int(h * 6)
       f = (h * 6) - i
       p = v * (1 - s)
       q = v * (1 - s * f)
       t = v * (1 - s * (1 - f))
       i = i % 6
       # Efficient color component selection
       if i == 0: return v, t, p
       elif i == 1: return q, v, p
       elif i == 2: return p, v, t
       elif i == 3: return p, q, v
       elif i == 4: return t, p, v
       else: return v, p, q
   ```

2. **CRT Effect Optimization**
   - Time-based color shifting using sine waves
   - Efficient color bleeding simulation
   - Phosphor glow effect using multiplication
   - Memory-efficient color component manipulation
   ```python
   def apply_crt_effect(color, time_val):
       # Efficient bit manipulation for color components
       r = ((color >> 16) & 0xFF)
       g = ((color >> 8) & 0xFF)
       b = (color & 0xFF)
       
       # Optimized color transformations
       shift = math.sin(time_val * 2) * 0.1
       glow = 0.85 + 0.15 * math.sin(time_val * 3)
       
       # Single-pass color modification
       r = int(min(255, max(0, r * glow * (1 + shift)))
       g = int(min(255, max(0, g * glow)))
       b = int(min(255, max(0, b * glow * (1 - shift * 0.5))))
       
       return (r << 16) | (g << 8) | b
   ```

3. **Performance Optimizations**
   - Pre-calculated color tables for common values
   - Bit-level operations for color manipulation
   - Efficient memory usage for color storage
   - Optimized color transition calculations
   - Touch response thresholding to prevent excessive updates

4. **Memory Management**
   - Efficient color storage using 24-bit integers
   - Garbage collection optimization for color calculations
   - Minimal memory allocation during color transitions
   - Reuse of color objects to reduce memory fragmentation

### Understanding Bit Shifting: The Digital Color Palette
To understand how colors are manipulated in the installation, let's explore the concept of bit shifting through an artistic lens:

1. **The Digital Color Canvas**
   A color in digital art is like a 24-bit canvas, where:
   ```
   [Red 8 bits][Green 8 bits][Blue 8 bits]
   ```
   For example, the color white (255, 255, 255) looks like this in binary:
   ```
   [11111111][11111111][11111111]
   ```

2. **Bit Shifting as Color Separation**
   The `>>` (right shift) operation is like sliding a color filter:
   ```python
   r = ((color >> 16) & 0xFF)  # Slide right 16 places to get red
   g = ((color >> 8) & 0xFF)   # Slide right 8 places to get green
   b = (color & 0xFF)          # Keep last 8 bits for blue
   ```
   
   Let's see how this works with a purple color (255, 0, 255):
   ```
   Original:  [11111111][00000000][11111111]
   
   After >>16: [00000000][00000000][11111111]  # Red component
   After >>8:  [00000000][11111111][00000000]  # Green component
   After &0xFF:[00000000][00000000][11111111]  # Blue component
   ```

3. **The Color Mask (0xFF)**
   The `& 0xFF` operation is like using a stencil:
   - `0xFF` in binary is `11111111`
   - It acts like a mask that only lets through the last 8 bits
   - Think of it as a color filter that only shows one primary color

4. **Color Recomposition**
   The `<<` (left shift) operation is like layering colors:
   ```python
   return (r << 16) | (g << 8) | b
   ```
   
   For example, to create purple:
   ```
   Red:    [11111111][00000000][00000000]  # << 16
   Green:  [00000000][00000000][00000000]  # << 8
   Blue:   [00000000][00000000][11111111]  # No shift
   Result: [11111111][00000000][11111111]  # Purple!
   ```

5. **The Artistic Impact**
   - Bit shifting is like having precise control over each color channel
   - It allows for efficient color manipulation without floating-point math
   - The operations are fast enough to create smooth animations
   - It's like having a digital color mixer that can instantly separate and recombine colors

This digital color manipulation is what enables the installation to create its warm, organic CRT effects while maintaining smooth performance on the embedded hardware. It's a perfect example of how technical precision can be used to create artistic effects that feel natural and alive.

### Display Features
- 320x240 resolution display
- Touch calibration for precise interaction
- Dynamic text wrapping for optimal readability
- Multiple scan lines with varying intensities

### Performance Optimizations
- Efficient memory management
- Optimized color calculations
- Smooth animation timing
- Touch response thresholding

## Setup Instructions

1. Install CircuitPython on your PyPortal Titano
2. Copy the required libraries to the `lib` folder
3. Place `quotes.txt` in the root directory
4. Upload `code.py` to the device
5. Power on and enjoy the interactive display

## Customization

The installation can be customized by:
- Modifying the `quotes.txt` file with new source material
- Adjusting visual parameters in the code
- Changing color schemes and animation speeds
- Modifying the Markov chain parameters

## Credits

Created as an interactive art project exploring the intersection of technology and philosophy. The project uses the PyPortal Titano's capabilities to create an engaging, ever-evolving display that responds to user interaction while maintaining a unique aesthetic quality.

### Acknowledgments
This project was inspired by the work of [@kuiperobjects](https://github.com/kuiperobjects), who introduced the concept of using Markov chains for generative text art. Their innovative approach to text generation and analysis has been a significant influence on this project's development.

## License

This project is open source and available for modification and personal use. 