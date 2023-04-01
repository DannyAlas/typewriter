import drawsvg as draw
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.utils import get_characters_and_times

app = FastAPI()

app.mount("/typewriter-demo", StaticFiles(directory="api/demo"), name="static")
templates = Jinja2Templates(directory="api/demo")


@app.get("/typewriter-demo")
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/")
async def read_item(request: Request):
    return RedirectResponse(url="/typewriter-demo")


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

    true_duration = (lines.count(";") + 2 * pause) + duration

    lines_list = lines.split(";")

    total_characters, display_time = get_characters_and_times(
        lines_list, true_duration, multiline, pause
    )

    d = draw.Drawing(
        width,
        height,
        origin=(0, 0),
        animation_config=draw.types.SyncedAnimationConfig(
            duration=display_time[len(display_time) - 1],
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
            y = (height / 2 - (size * (lines.count(";") + 1)) / 2) + 17
        else:
            y = height / 2 + size / 3
    else:
        y = size
    if center:
        center = True
        x = width / 2
        y -= 9
    else:
        center = False
        x = 0
        draw.native_animation.animate_text_sequence(
            d,
            display_time,
            total_characters,
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
