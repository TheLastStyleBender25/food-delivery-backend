from pathlib import Path
from uuid import uuid4
from app.exceptions.all_exceptions import InvalidImageExtensionException, InvalidImageTypeException, InvalidImageContentException, FileTooLargeException
import aiofiles.os
import aiofiles
from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError
from io import BytesIO


class FileStorageService:
    ALLOWED_EXTENSIONS = {".jpg",".jpeg",".png",".webp"}
    ALLOWED_CONTENT_TYPES = {"image/jpeg","image/png","image/webp"}
    MAX_FILE_SIZE = 5 * 1024 * 1024

    def __init__(self):
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)


    def generate_filename(self, extension:str):
        return f"{uuid4()}{extension.lower()}"


    def get_file_path(self, filename:str):
        return self.upload_dir/filename

    async def save_menu_image(self, file: UploadFile):
        self.validate_extension(file.filename)
        self.validate_content_type(file.content_type)

        content = await file.read()

        self.validate_image_content(content)
        self.validate_file_size(content)

        name = self.generate_filename(Path(file.filename).suffix)
        path = self.get_file_path(name)

        print("Current Working Directory:", Path.cwd())
        print("Upload Directory:", self.upload_dir.resolve())
        print("Saving To:", path.resolve())

        async with aiofiles.open(path, "wb") as f:
            await f.write(content)

        print("Exists:", path.exists())

        return f"/uploads/{name}"


    def validate_extension(self, filename: str):
        extension = Path(filename).suffix.lower()
        if extension not in self.ALLOWED_EXTENSIONS:
            raise InvalidImageExtensionException()


    def validate_content_type(self, content_type: str):
        if content_type not in self.ALLOWED_CONTENT_TYPES:
            raise InvalidImageTypeException()


    def validate_image_content(self, image_bytes: bytes) -> None:
        try:
            with Image.open(BytesIO(image_bytes)) as image:
                image.verify()
        except (UnidentifiedImageError, OSError):
            raise InvalidImageContentException()

    def validate_file_size(self, image_bytes: bytes):
        if len(image_bytes) > self.MAX_FILE_SIZE:
            raise FileTooLargeException()


    async def delete_menu_image(self, image_url: str):
        filename = Path(image_url).name
        path = self.get_file_path(filename)
        if path.exists():
            await aiofiles.os.remove(path)



