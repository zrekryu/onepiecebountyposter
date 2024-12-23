import importlib.resources
from io import BytesIO
from random import randint

from PIL import Image, ImageDraw, ImageFont

class BountyPoster:
    BOUNTY_POSTER_TEMPLATE_PATH: str = "resources/images/bounty_poster_template.png"
    
    NAME_FONT_PATH: str = "resources/fonts/PlayfairDisplay-Bold.ttf"
    NAME_FONT_SIZE: int = 50
    
    PRICE_FONT_PATH: str = "resources/fonts/PlayfairDisplay-Bold.ttf"
    PRICE_FONT_SIZE: int = 80
    
    PRICE_RANGE_START: int = 99_999_999
    PRICE_RANGE_END: int = 999_999_999
    
    NAME_FONT_FILL: str = "#5f4d33"
    PRICE_FONT_FILL: str = "#5f4d33"
    
    POSTER_FILE_FORMAT: str = "PNG"
    
    def __init__(
        self,
        bounty_poster_template_path: str | bytes | BytesIO | None = None,
        name_font_path: str | bytes | BytesIO | None = None,
        name_font_size: int = NAME_FONT_SIZE,
        name_font_fill: str = NAME_FONT_FILL,
        price_font_path: str | bytes | BytesIO | None = None,
        price_font_size: int = PRICE_FONT_SIZE,
        price_font_fill: str = PRICE_FONT_FILL,
        price_range_start: int = PRICE_RANGE_START,
        price_range_end: int = PRICE_RANGE_END,
        poster_file_format: str = POSTER_FILE_FORMAT
        ) -> None:
        self.bounty_poster_template_path = bounty_poster_template_path
        
        self.name_font_path = name_font_path
        self.name_font_size = name_font_size
        self.name_font_fill = name_font_fill
        
        self.price_font_path = price_font_path
        self.price_font_size = price_font_size
        self.price_font_fill = price_font_fill
        
        self.price_range_start = price_range_start
        self.price_range_end = price_range_end
        
        self.poster_file_format = poster_file_format
    
    def _load_user_image_file(self, path: str | bytes | BytesIO | None) -> Image:
        if isinstance(path, bytes):
            return Image.open(BytesIO(path))
        
        return Image.open(path)
    
    def _load_template_image_file(self, path: str | bytes | BytesIO | None) -> Image:
        if path is None:
            return Image.open(importlib.resources.files(__package__).joinpath(self.BOUNTY_POSTER_TEMPLATE_PATH))
        
        if isinstance(path, bytes):
            return Image.open(BytesIO(path))
        
        return Image.open(path)
    
    def _load_name_font_file(self, path: str | bytes | BytesIO | None, size: int) -> ImageFont:
        if path is None:
            return ImageFont.truetype(
                font=importlib.resources.files(__package__).joinpath(self.NAME_FONT_PATH),
                size=size
                )
        
        if isinstance(path, bytes):
            return ImageFont.truetype(BytesIO(path), size)
        
        return ImageFont.truetype(path, size)
    
    def _load_price_font_file(self, path: str | bytes | BytesIO | None, size: int) -> ImageFont:
        if path is None:
            return ImageFont.truetype(
                font=importlib.resources.files(__package__).joinpath(self.PRICE_FONT_PATH).open("rb"),
                size=size
                )
        
        if isinstance(path, bytes):
            return ImageFont.truetype(BytesIO(path), size)
        
        return ImageFont.truetype(path, size)
    
    def _get_random_price(self, price_range_start: int, price_range_end: int) -> int:
        return randint(price_range_start, price_range_end)
    
    def create_poster(
        self,
        user_image_path: str | bytes | BytesIO,
        name: str,
        price: int | None = None,
        bounty_poster_template_path: str | bytes | BytesIO | None = None,
        name_font_path: str | bytes | BytesIO | None = None,
        name_font_size: int | None = None,
        name_font_fill: str | None = None,
        price_font_path: str | bytes | BytesIO | None = None,
        price_font_size: int | None = None,
        price_font_fill: str | None = None,
        price_range_start: int | None = None,
        price_range_end: int | None = None,
        poster_file_format: str | None = None
        ) -> BytesIO:
        if not price:
            price = self._get_random_price(
                price_range_start=price_range_start or self.price_range_start,
                price_range_end=price_range_end or self.price_range_end
                )
        user_img: Image = self._load_user_image_file(user_image_path)
        template_img: Image = self._load_template_image_file(bounty_poster_template_path or self.bounty_poster_template_path)
        
        resized_user_img = user_img.resize((615, 447), Image.Resampling.LANCZOS)
        template_img.paste(resized_user_img, (70, 227))
        
        name_font: ImageFont = self._load_name_font_file(
            path=name_font_path or self.name_font_path,
            size=name_font_size or self.name_font_size
            )
        price_font: ImageFont = self._load_price_font_file(
            path=price_font_path or self.price_font_path,
            size=price_font_size or self.price_font_size
            )
        
        draw = ImageDraw.Draw(template_img)
        
        W, H = (790, 1640)
        _, _, w, h = draw.textbbox((0, 0), name, name_font)
        draw.text(((W-w)/2, (H-h)/2), name, fill=name_font_fill or self.name_font_fill, font=name_font)
        draw.text((180, 860), f"{price:,} -", fill=price_font_fill or self.price_font_fill, font=price_font)
        
        output: BytesIO = BytesIO()
        template_img.save(output, format=poster_file_format or self.poster_file_format)
        
        return output