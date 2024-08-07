
import vobject
from django.core.management.base import BaseCommand
from .models import Contact  # Asegúrate de reemplazar 'your_app' con el nombre de tu aplicación Django

class Command(BaseCommand):
    help = 'Importa contactos desde un archivo VCARD'

    def add_arguments(self, parser):
        parser.add_argument('vcard_file', type=str, help='Ruta al archivo VCARD')

    def handle(self, *args, **options):
        vcard_file = options['vcard_file']

        with open(vcard_file, 'r', encoding='utf-8') as file:
            vcards = vobject.readComponents(file)

            for vcard in vcards:
                contact = Contact()

                # Mapea los campos VCARD a los campos del modelo Contact
                if hasattr(vcard, 'fn'):
                    contact.full_name = vcard.fn.value
                if hasattr(vcard, 'n'):
                    contact.last_name = vcard.n.value.family
                    contact.first_name = vcard.n.value.given
                if hasattr(vcard, 'tel'):
                    contact.phone = vcard.tel.value
                if hasattr(vcard, 'email'):
                    contact.email = vcard.email.value
                if hasattr(vcard, 'adr'):
                    contact.address = ', '.join(vcard.adr.value)
                if hasattr(vcard, 'org'):
                    contact.organization = vcard.org.value[0]
                if hasattr(vcard, 'title'):
                    contact.title = vcard.title.value

                contact.save()

        self.stdout.write(self.style.SUCCESS('Contactos importados exitosamente'))