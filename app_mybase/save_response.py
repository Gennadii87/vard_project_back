from django.utils import timezone
from django.core.files import File as DjangoFile
from django.core.files.base import ContentFile
import mimetypes
import json

from app_database.models import File


class SqlSaveResponse:
    @staticmethod
    def save_file(response, database):
        filename = f"Response_SQL_{timezone.now().strftime('%Y_%m_%d_%H_%M_%S')}.json"
        name, extension = filename.rsplit('.', 1)
        mime_type, encoding = mimetypes.guess_type(filename)
        if mime_type:
            extension_type = mime_type.split('/')[-1].upper()
        else:
            extension_type = 'OTHER'

        file_model = File(
            user_id=database.user,
            place_id='MF',
            name=name,
            link=DjangoFile(ContentFile(json.dumps(response, indent=4).encode()), name=filename),
            type_id=extension_type,
            publish=1
        )
        file_model.save()


