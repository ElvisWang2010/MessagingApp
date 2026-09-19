from PIL import Image, ImageDraw
import math


SIZES = [16, 24, 32, 48, 64, 128, 256]

PETAL_COLOR = "#FF8FAB"
PETAL_OUTLINE = "#FF6F91"
CENTER_COLOR = "#FF6F91"
CENTER_OUTLINE = "#FFFFFF"


def create_flower(size):

    image = Image.new(
        "RGBA",
        (size, size),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(image)

    center = size / 2

    petal_radius = size * 0.23
    petal_distance = size * 0.22
    center_radius = size * 0.17

    # Five petals
    for i in range(5):

        angle = math.radians(
            -90 + i * 72
        )

        petal_x = (
            center
            + math.cos(angle) * petal_distance
        )

        petal_y = (
            center
            + math.sin(angle) * petal_distance
        )

        box = (
            petal_x - petal_radius,
            petal_y - petal_radius,
            petal_x + petal_radius,
            petal_y + petal_radius
        )

        draw.ellipse(
            box,
            fill=PETAL_COLOR,
            outline=PETAL_OUTLINE,
            width=max(1, int(size * 0.035))
        )

    # Center
    center_box = (
        center - center_radius,
        center - center_radius,
        center + center_radius,
        center + center_radius
    )

    draw.ellipse(
        center_box,
        fill=CENTER_COLOR,
        outline=CENTER_OUTLINE,
        width=max(1, int(size * 0.035))
    )

    return image


icons = [
    create_flower(size)
    for size in SIZES
]

icons[0].save(
    "petal.ico",
    format="ICO",
    sizes=[
        (16, 16),
        (24, 24),
        (32, 32),
        (48, 48),
        (64, 64),
        (128, 128),
        (256, 256)
    ]
)

print("Created petal.ico")