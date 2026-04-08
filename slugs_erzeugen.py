from django.utils.text import slugify
from reisen.models import Reise 

for reise in Reise.objects.all():
    # 1. Basis-Slug vom Titel, aber auf 40 Zeichen gekürzt
    base_slug = slugify(reise.titel)[:40].rstrip('-')
    
    termin = reise.reisetermine_set.order_by('datum_beginn').first()
    jahr_suffix = f"-{termin.datum_beginn.year}" if (termin and termin.datum_beginn) else ""
    
    test_slug = f"{base_slug}{jahr_suffix}"
    final_slug = test_slug
    counter = 1
    
    # Eindeutigkeit sicherstellen (auch hier Kürzung beachten)
    while Reise.objects.filter(slug=final_slug).exclude(reiseID=reise.reiseID).exists():
        # Falls der Zähler den Slug wieder zu lang macht, nochmal kürzen
        final_slug = f"{test_slug[:35].rstrip('-')}-{counter}"
        counter += 1
    
    if reise.slug != final_slug:
        try:
            reise.slug = final_slug
            reise.save()
            print(f"Update: {final_slug}")
        except Exception as e:
            print(f"Fehler bei {reise.titel}: {e}")

print("Fertig!")