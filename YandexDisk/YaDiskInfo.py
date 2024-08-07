class TemplateInfo:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path


class FontInfo:
    def __init__(self, path: str, name: str):
        self.path = path
        self.name = name


class ImageInfo:
    def __init__(self, position: str, path: str):
        self.position = position
        self.path = path


class YaDiskInfo:
    def __init__(self):
        self.templates = []
        self.fonts = []
        self.images = []

    def add_template(self, name: str, path: str):
        self.templates.append(TemplateInfo(name, path))

    def add_font(self, path: str, name: str):
        self.fonts.append(FontInfo(path, name))

    def add_image(self, position: str, path: str):
        self.images.append(ImageInfo(position, path))

    def get_templates(self) -> list:
        return self.templates

    def get_fonts(self) -> list:
        return self.fonts

    def get_images(self) -> list:
        return self.images

    def clear(self):
        self.templates.clear()
        self.fonts.clear()
        self.images.clear()
