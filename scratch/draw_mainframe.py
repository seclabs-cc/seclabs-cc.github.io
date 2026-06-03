from PIL import Image, ImageDraw

# Create a 512x512 image with a dark theme background
bg_color = (13, 14, 18)  # Deep dark gray
img = Image.new("RGB", (512, 512), bg_color)
draw = ImageDraw.Draw(img)

# Helper function to draw glowing lines
def draw_glow_line(xy, color, width=4, glow_color=None):
    if glow_color is None:
        glow_color = color
    # Draw glow layers
    for w, opacity in [(width * 3, 20), (width * 2, 50), (width * 1.5, 100)]:
        c = glow_color + (opacity,)
        # We need an RGBA overlay to support opacity
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.line(xy, fill=c, width=w, joint="round")
        img.paste(overlay, (0, 0), overlay)
    
    # Draw solid core
    draw.line(xy, fill=color, width=width, joint="round")

# Helper function to draw glowing rect (no rounded corners for absolute safety)
def draw_glow_rect(xy, color, width=4, glow_color=None):
    if glow_color is None:
        glow_color = color
    for w, opacity in [(width * 3, 20), (width * 2, 50), (width * 1.5, 100)]:
        c = glow_color + (opacity,)
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(xy, outline=c, width=w)
        img.paste(overlay, (0, 0), overlay)
    draw.rectangle(xy, outline=color, width=width)

# Helper function to draw glowing circle
def draw_glow_circle(xy, radius, color, glow_color=None):
    x, y = xy
    box = [x - radius, y - radius, x + radius, y + radius]
    if glow_color is None:
        glow_color = color
    for r_offset, opacity in [(radius * 1.5, 30), (radius * 1.2, 80)]:
        c = glow_color + (opacity,)
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        b = [x - r_offset, y - r_offset, x + r_offset, y + r_offset]
        overlay_draw.ellipse(b, fill=c)
        img.paste(overlay, (0, 0), overlay)
    draw.ellipse(box, fill=color)

# Draw a subtle background technical grid
grid_color = (255, 255, 255, 10)  # Very faint white
overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
overlay_draw = ImageDraw.Draw(overlay)
for i in range(32, 512, 32):
    overlay_draw.line([(i, 0), (i, 512)], fill=grid_color, width=1)
    overlay_draw.line([(0, i), (512, i)], fill=grid_color, width=1)
img.paste(overlay, (0, 0), overlay)

# Define Theme Colors (RGBA format)
indigo_glow = (99, 102, 241)     # Brand indigo
indigo_core = (165, 180, 252)    # Bright light indigo for core
gray_core = (107, 114, 128)      # Gray structure

# 1. Draw Mainframe Cabinet Frame
# Center: X from 156 to 356, Y from 66 to 446
draw_glow_rect([156, 66, 356, 446], color=gray_core, width=6, glow_color=indigo_glow)

# 2. Draw Stacked Server Blades
# Blade 1: Y from 106 to 196 (width 160)
draw_glow_rect([176, 106, 336, 196], color=indigo_core, width=4, glow_color=indigo_glow)
# LEDs on Blade 1
draw_glow_circle((206, 151), radius=6, color=indigo_core, glow_color=indigo_glow)
draw.ellipse([226 - 4, 151 - 4, 226 + 4, 151 + 4], fill=gray_core) # inactive LED
# Ventilation grill lines on Blade 1
draw.line([(256, 141), (306, 141)], fill=gray_core, width=3)
draw.line([(256, 151), (306, 151)], fill=gray_core, width=3)
draw.line([(256, 161), (306, 161)], fill=gray_core, width=3)

# Blade 2: Y from 216 to 306
draw_glow_rect([176, 216, 336, 306], color=indigo_core, width=4, glow_color=indigo_glow)
# LEDs on Blade 2
draw_glow_circle((206, 261), radius=6, color=indigo_core, glow_color=indigo_glow)
draw.ellipse([226 - 4, 261 - 4, 226 + 4, 261 + 4], fill=gray_core)
# Port socket on Blade 2 (draw standard rectangle)
draw.rectangle([256, 246, 306, 276], outline=gray_core, width=3)

# Blade 3: Y from 326 to 416
draw_glow_rect([176, 326, 336, 416], color=indigo_core, width=4, glow_color=indigo_glow)
# LEDs on Blade 3
draw_glow_circle((206, 371), radius=6, color=indigo_core, glow_color=indigo_glow)
draw.ellipse([226 - 4, 371 - 4, 226 + 4, 371 + 4], fill=gray_core)
# Ventilation lines on Blade 3
draw.line([(256, 361), (306, 361)], fill=gray_core, width=3)
draw.line([(256, 371), (306, 371)], fill=gray_core, width=3)
draw.line([(256, 381), (306, 381)], fill=gray_core, width=3)

# 3. Draw Connecting Cables (bezier-like curves using points)
# Cable 1: from (316, 151) to (316, 261) curving right
c1_points = []
for t in range(101):
    ti = t / 100.0
    # Quadratic bezier: P0=(316, 151), P1=(376, 206), P2=(316, 261)
    x = (1-ti)**2 * 316 + 2*(1-ti)*ti * 376 + ti**2 * 316
    y = (1-ti)**2 * 151 + 2*(1-ti)*ti * 206 + ti**2 * 261
    c1_points.append((x, y))
draw_glow_line(c1_points, color=indigo_core, width=3, glow_color=indigo_glow)

# Cable 2: from (196, 261) to (196, 371) curving left
c2_points = []
for t in range(101):
    ti = t / 100.0
    # Quadratic bezier: P0=(196, 261), P1=(136, 316), P2=(196, 371)
    x = (1-ti)**2 * 196 + 2*(1-ti)*ti * 136 + ti**2 * 196
    y = (1-ti)**2 * 261 + 2*(1-ti)*ti * 316 + ti**2 * 371
    c2_points.append((x, y))
draw_glow_line(c2_points, color=indigo_core, width=3, glow_color=indigo_glow)

# Save the final high-quality image
img.save("images/setup_card.png")
print("Mainframe server rack image generated successfully!")
