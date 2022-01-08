from enum import Enum
from pathlib import Path

from mongoengine.errors import DoesNotExist

from website import db


class ImgStatus(Enum):
    ''' Img status enumerator '''

    NEW = 'new'
    PROCESSED = 'processed'
    ARCHIVED = 'archived'


class Image(db.Document):  # type: ignore[name-defined]
    ''' Image ODM '''

    class Format(db.EmbeddedDocument):  # type: ignore[name-defined]
        ''' Image format subdocument '''

        format = db.StringField()
        quality = db.IntField(min_value=0, max_value=100, default=55)
        processing = db.DictField()
        outputs = db.ListField(db.StringField())

        def __str__(self):
            return self.format

        def __repr__(self):
            return f"<Format(format={self.format}), {len(self.outputs)} files>"

    name = db.StringField(required=True, unique=True)
    source_format = db.StringField(required=True)
    filepath = db.StringField(required=True)
    desc = db.StringField()
    status = db.EnumField(ImgStatus, default=ImgStatus.NEW)
    width = db.IntField()
    height = db.IntField()
    thumbnail_widths = db.ListField(db.IntField())
    formats = db.EmbeddedDocumentListField(Format)

    meta = {'indexes': ['name', 'filepath']}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Image(name='{self.name}'), {self.status.name}>"

    @property
    def path(self) -> Path:
        return Path(self.filepath)

    def check_outputs(self) -> bool:
        """ verify that listed output files in database match filesystem """
        outputs = (
            Path(path)
            for format in self.formats
            for path in format.outputs
            )

        # 1 check all listed files exist
        return all(path.exists for path in outputs)

    def set_format(self, format: str, quality: int, **params) -> None:
        try:
            format_info = self.formats.get(format=format)
        except DoesNotExist:
            format_info = self.formats.create(
                format=format,
                quality=quality,
                processing=params
                )
        else:
            format_info.quality = quality
            format_info.processing = params
        finally:
            self.save()

    def delete_format(self, format: str) -> int:
        return self.formats.filter(format=format).delete()
