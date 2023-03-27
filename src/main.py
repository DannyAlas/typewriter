import drawsvg as draw
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/typewriter-demo", StaticFiles(directory="demo"), name="static")
templates = Jinja2Templates(directory="demo")

@app.get("/typewriter-demo")
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/typewriter")
def main(
    font: str = "Fira+Code",
    weight: int = 400,
    size: int = 20,
    style: str = "normal",
    duration: int = 5000,
    color: str = "36BCF7FF",
    background: str = "00000000",
    center: bool = False,
    vCenter: bool = True,
    multiline: bool = False,
    width: int = 435,
    height: int = 50,
    pause: int = 1000,
    lines: str = "The+five+boxing+wizards+jump+quickly;How+vexingly+quick+daft+zebras+jump",
) -> StreamingResponse:
    d = draw.Drawing(
        width,
        height,
        origin=(0, 0),
        animation_config=draw.types.SyncedAnimationConfig(
            duration=(lines.count(";")+1 * pause/1000) + duration/1000
        ),
    )

    # FONTS
    font = font.replace("+", " ")
    d.embed_google_font(font)

    # BACKGROUND
    d.append(draw.Rectangle(0, 0, width, height, fill=f"#{background}"))
    
    # TEXT POSITION
    if vCenter:
        if multiline:
            # i have no idea why i need to add 17 to the y position to center it vertically, but it works
            y = (height / 2 - (size * (lines.count(";")+1)) / 2) + 17 
        else:
            y = height / 2 + size / 3
            print("AHHHHHHHHH", y)
    else:
        y = size
    if center:
        center = True
        x = width / 2
        y -= 9
    else:
        center = False
        x = 0

    # ANIMATION
    if not multiline:
        characters = []
        for i in range(len(lines)):
            if i == 0:
                characters.append(lines[i])
            elif lines[i] == ";":
                characters.append("")
            else:
                characters.append(characters[i - 1] + lines[i])
    else:
        characters = []
        for i in range(len(lines)):
            if i == 0:
                characters.append(lines[i])
            elif lines[i] == ";":
                characters.append(characters[i - 1] + "\n")
            # on the last character, add an empty string to the last keyframe
            # elif i == len(lines) - 1:
            #     characters.append(characters[i - 1] + "")
            else:
                characters.append(characters[i - 1] + lines[i])

    
    display_time = [] # keyframes
    for i in range(len(characters)):
        if i == 0:
            display_time.append(0)
        elif lines[i] == ";":
            display_time.append(display_time[i - 1] + (duration / 1000) / len(lines) + (pause / 1000))
        # on the last character, add the pause time to the last keyframe
        elif i == len(lines):
            print("last character", lines[i])
            display_time.append(display_time[i - 1] + (duration / 1000) / len(lines) + (pause / 1000))
        else:
            display_time.append(display_time[i - 1] + (duration / 1000) / len(lines))

    draw.native_animation.animate_text_sequence(
        d,
        display_time,
        characters,
        size,
        x,
        y,
        font_family=font,
        font_weight=weight,
        font_style=style,
        fill=f"#{color}",
        center=center,
    )

    def iter():
        yield d.as_svg()
    
    return StreamingResponse(iter(), media_type="image/svg+xml")
