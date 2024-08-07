import vobject
import os

from minicrm.models import Contact, Estado

def import_vcard_to_contacts(file_path):
    estado = Estado.objects.get(estado='customer')
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Dividir el contenido en tarjetas vCard
    vcard_entries = content.split("END:VCARD")
    
    for entry in vcard_entries:
        if "BEGIN:VCARD" in entry:
            try:
                # Parsear el vCard
                vcard = vobject.readOne(entry + "END:VCARD")
                
                full_name = vcard.fn.value if vcard.fn else ''
                email = vcard.email.value if vcard.email else ''
                
                # Descomponer el nombre completo en nombre y apellido
                names = full_name.split(' ', 1)
                first_name = names[0] if len(names) > 0 else ''
                last_name = names[1] if len(names) > 1 else ''
                
                contact, created = Contact.objects.update_or_create(
                    email=email,  # Utiliza el campo email como identificador único
                    status = estado,
                    defaults={
                        'full_name': full_name,
                        'first_name': first_name,
                        'last_name': last_name,
                        'phone': '',  # No hay información de teléfono en el vCard
                        'address': '',  # No hay información de dirección en el vCard
                        'organization': '',  # No hay información de organización en el vCard
                        'title': '',  # No hay información de título en el vCard
                    }
                )
                if created:
                    print(f'Contact created: {contact}')
                else:
                    print(f'Contact updated: {contact}')
                
            except Exception as e:
                print(f"Error processing vCard entry: {e}")


#    import_vcard_to_contacts(file_path)
