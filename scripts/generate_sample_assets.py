"""
Generate realistic sample images for construction site safety audit and crack diagnostics.
"""

import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("assets/sample_images", exist_ok=True)

def create_site_safety_sample_1():
    # Construction site safety sample 1: Scaffolding, Workers with hard hats & vests, one edge hazard
    img = Image.new("RGB", (900, 600), color=(35, 45, 60))
    draw = ImageDraw.Draw(img)

    # Sky gradient / building backdrop
    for y in range(250):
        r = int(45 + (y / 250) * 30)
        g = int(60 + (y / 250) * 40)
        b = int(90 + (y / 250) * 50)
        draw.line([(0, y), (900, y)], fill=(r, g, b))

    # Concrete structure / floor slabs
    draw.rectangle([60, 180, 840, 220], fill=(120, 125, 130), outline=(80, 85, 90), width=3)
    draw.rectangle([60, 380, 840, 420], fill=(110, 115, 120), outline=(70, 75, 80), width=3)
    draw.rectangle([0, 520, 900, 600], fill=(70, 65, 60))  # Ground

    # Scaffolding pipes (steel tubes)
    for x in range(100, 820, 120):
        draw.line([(x, 120), (x, 520)], fill=(200, 205, 210), width=6)
        draw.line([(x+6, 120), (x+6, 520)], fill=(160, 165, 170), width=2)
    # Cross bracings
    for x in range(100, 700, 120):
        draw.line([(x, 220), (x+120, 380)], fill=(180, 185, 190), width=3)
        draw.line([(x, 380), (x+120, 220)], fill=(180, 185, 190), width=3)

    # Worker 1: Upper deck (Helmet, Vest, Working on shuttering)
    # Body
    draw.rectangle([210, 130, 240, 180], fill=(245, 158, 11)) # Safety vest
    draw.line([(220, 140), (220, 175)], fill=(240, 240, 240), width=3) # Reflective stripe
    draw.ellipse([215, 105, 235, 125], fill=(220, 180, 150)) # Face
    draw.arc([210, 98, 240, 118], 180, 360, fill=(250, 204, 21), width=6) # Hard hat yellow
    draw.line([(205, 115), (245, 115)], fill=(250, 204, 21), width=4) # Brim

    # Worker 2: Upper deck edge (Harness lanyard not attached - Hazard!)
    draw.rectangle([450, 130, 480, 180], fill=(245, 158, 11))
    draw.ellipse([455, 105, 475, 125], fill=(220, 180, 150))
    draw.arc([450, 98, 480, 118], 180, 360, fill=(255, 255, 255), width=6) # White hard hat
    draw.line([(445, 115), (485, 115)], fill=(255, 255, 255), width=4)
    # Hanging unattached lanyard
    draw.line([(475, 150), (490, 175), (495, 200)], fill=(239, 68, 68), width=3)

    # Worker 3 & 4: Ground level
    draw.rectangle([300, 440, 335, 510], fill=(16, 185, 129)) # Green vest
    draw.ellipse([308, 415, 328, 435], fill=(210, 170, 140))
    draw.arc([303, 408, 333, 428], 180, 360, fill=(250, 204, 21), width=6)
    draw.line([(298, 425), (338, 425)], fill=(250, 204, 21), width=4)

    draw.rectangle([620, 440, 655, 510], fill=(245, 158, 11))
    draw.ellipse([628, 415, 648, 435], fill=(210, 170, 140))
    # Worker 4 has cloth cap instead of hard hat (Violation)
    draw.ellipse([625, 410, 650, 422], fill=(70, 70, 160))

    # Site Safety Board & Grid label
    draw.rectangle([30, 30, 430, 85], fill=(15, 23, 42, 220), outline=(245, 158, 11), width=2)
    draw.text((45, 38), "SITE SAFETY AUDIT #AUD-2026-A1", fill=(245, 158, 11))
    draw.text((45, 58), "Location: Tower B - 4th Floor Cantilever Shuttering Deck", fill=(220, 225, 230))

    # Red hazard highlight box on Worker 2
    draw.rectangle([430, 90, 520, 215], outline=(239, 68, 68), width=3)
    draw.text((435, 75), "HAZ-001: LANYARD UNATTACHED", fill=(239, 68, 68))

    img.save("assets/sample_images/site_safety_sample_1.jpg", "JPEG", quality=90)


def create_site_safety_sample_2():
    # Site safety sample 2: High compliance rebar fixing zone
    img = Image.new("RGB", (900, 600), color=(40, 50, 65))
    draw = ImageDraw.Draw(img)

    # Steel rebar matting on ground
    for y in range(320, 580, 25):
        draw.line([(80, y), (820, y)], fill=(120, 115, 110), width=4)
    for x in range(100, 800, 30):
        draw.line([(x, 300), (x, 580)], fill=(130, 125, 120), width=4)

    # Workers kneeling & standing with 100% PPE compliance
    for idx, wx in enumerate([220, 410, 600]):
        draw.rectangle([wx, 260, wx+38, 350], fill=(245, 158, 11)) # Hi-vis vest
        draw.line([(wx+8, 275), (wx+8, 345)], fill=(255, 255, 255), width=3)
        draw.line([(wx+30, 275), (wx+30, 345)], fill=(255, 255, 255), width=3)
        draw.ellipse([wx+8, 232, wx+30, 254], fill=(220, 175, 140)) # Face
        draw.arc([wx+3, 224, wx+35, 246], 180, 360, fill=(250, 204, 21), width=7) # Helmet
        draw.line([(wx-2, 244), (wx+40, 244)], fill=(250, 204, 21), width=4)
        # Steel-toe boots
        draw.rectangle([wx-2, 350, wx+16, 368], fill=(30, 30, 30))
        draw.rectangle([wx+22, 350, wx+40, 368], fill=(30, 30, 30))

    # Header Card
    draw.rectangle([30, 30, 480, 85], fill=(15, 23, 42, 220), outline=(16, 185, 129), width=2)
    draw.text((45, 38), "SITE SAFETY AUDIT #AUD-2026-B2 (REBAR CREW)", fill=(16, 185, 129))
    draw.text((45, 58), "Full Compliance Zone: Steel deck footwear & IS 2925 Helmets", fill=(220, 225, 230))

    img.save("assets/sample_images/site_safety_sample_2.jpg", "JPEG", quality=90)


def create_crack_sample_1():
    # Structural Shear Crack (Diagonal 45 deg) on concrete beam
    img = Image.new("RGB", (900, 600), color=(145, 148, 150))
    draw = ImageDraw.Draw(img)

    # Concrete texture noise
    import random
    random.seed(42)
    for _ in range(8000):
        rx = random.randint(0, 899)
        ry = random.randint(0, 599)
        shade = random.randint(120, 170)
        draw.point((rx, ry), fill=(shade, shade, shade))

    # Beam boundary lines
    draw.line([(0, 100), (900, 100)], fill=(90, 92, 95), width=4)
    draw.line([(0, 500), (900, 500)], fill=(90, 92, 95), width=4)

    # Diagonal 45-degree Structural Shear Crack with branches
    crack_points = [
        (220, 490), (250, 450), (290, 410), (330, 370), (380, 320),
        (430, 280), (490, 230), (550, 180), (610, 130), (660, 105)
    ]
    # Draw dark inner crack fissure
    for i in range(len(crack_points)-1):
        p1, p2 = crack_points[i], crack_points[i+1]
        draw.line([p1, p2], fill=(25, 25, 25), width=6)
        # Random spall flakes
        draw.line([(p1[0]+3, p1[1]), (p2[0]+3, p2[1])], fill=(60, 60, 60), width=3)
        draw.line([(p1[0]-3, p1[1]), (p2[0]-3, p2[1])], fill=(185, 185, 185), width=2)

    # Micro-fissure branching
    draw.line([(380, 320), (420, 340), (450, 355)], fill=(35, 35, 35), width=3)
    draw.line([(490, 230), (510, 255), (530, 270)], fill=(40, 40, 40), width=2)

    # Calibrated Scale Marker & Crack Width tag
    draw.rectangle([50, 50, 380, 90], fill=(20, 25, 35), outline=(239, 68, 68), width=2)
    draw.text((65, 58), "DIAGNOSTIC TEST: BEAM B4 SHEAR ZONE", fill=(239, 68, 68))
    draw.text((65, 72), "Estimated Crack Width: ~3.8mm | Angle: ~42 deg", fill=(240, 240, 240))

    # Inspection gauge graphics
    draw.rectangle([680, 220, 840, 340], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.line([(700, 280), (820, 280)], fill=(200, 0, 0), width=2)
    for gx in range(710, 815, 10):
        draw.line([(gx, 275), (gx, 285)], fill=(0, 0, 0), width=1)
    draw.text((705, 235), "AVONGARD GAUGE", fill=(0, 0, 0))
    draw.text((715, 295), "+3.8 mm Shear", fill=(200, 0, 0))

    img.save("assets/sample_images/crack_structural_sample_1.jpg", "JPEG", quality=90)


def create_crack_sample_2():
    # Hairline thermal/shrinkage crack on plastered wall
    img = Image.new("RGB", (900, 600), color=(215, 218, 220))
    draw = ImageDraw.Draw(img)

    # Subtle plaster stipple
    import random
    random.seed(99)
    for _ in range(12000):
        rx = random.randint(0, 899)
        ry = random.randint(0, 599)
        val = random.randint(200, 225)
        draw.point((rx, ry), fill=(val, val, val))

    # Hairline meandering vertical/curving fissure (< 0.5 mm)
    pts = [
        (450, 40), (455, 110), (448, 170), (460, 240), (452, 310),
        (465, 380), (458, 440), (462, 510), (455, 570)
    ]
    for i in range(len(pts)-1):
        p1, p2 = pts[i], pts[i+1]
        draw.line([p1, p2], fill=(95, 95, 95), width=2)
        draw.line([(p1[0]+1, p1[1]), (p2[0]+1, p2[1])], fill=(180, 180, 180), width=1)

    # Hairline tag
    draw.rectangle([50, 50, 420, 90], fill=(20, 25, 35), outline=(56, 189, 248), width=2)
    draw.text((65, 58), "DIAGNOSTIC TEST: PLASTER SURFACE SCREED", fill=(56, 189, 248))
    draw.text((65, 72), "Defect: Hairline Crazing (< 0.5mm) | Non-Structural", fill=(240, 240, 240))

    img.save("assets/sample_images/crack_hairline_sample_2.jpg", "JPEG", quality=90)


if __name__ == "__main__":
    create_site_safety_sample_1()
    create_site_safety_sample_2()
    create_crack_sample_1()
    create_crack_sample_2()
    print("Sample images generated successfully.")
