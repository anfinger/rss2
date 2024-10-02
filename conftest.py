import pytest
from django.core.management import call_command


REISEN_PKS = (
    # -- Mehrtagesfahrten --
    'b463933c6815449ea42054f86df1bd5c',  # Rom
    '194ea4467b644bdb93398c6daeb78211',  # Dankeschoen
    'c66486e37a5f44b7bece6c0a3db92e54',  # Flusskreuzfahrt Douro
    # -- Tagesfahrten --
    '208b718e19d04777beb821ce988caf04',  # Fahrt ins Blaue
    '4359c2aa63524b35a225ad6182c4e76a',  # Ozeaneum
    '7690921ab795480380830684e5c0fbfe',  # Elbphilharmonie
    # -- Musicals & Shows
    '7fe42660eeb44b5aa4f82dfba5712353',     # Musikalischer Advent in Leipzig
)


# NOTE: temp. Erinnerungsstütze
#
_MAKE_FIXTURES = """
from django.core.management import call_command
from conftest import REISEN_PKS
from reisen.models import Zusatzleistung
fp = './reisen/fixtures/zusatzleisungen.json'
r = Zusatzleistung.objects.filter(reise_id__in=REISEN_PKS).values_list('pk', flat=True)
rpks = ','.join([str(ui) for ui in r])
call_command('mydumpdata', 'reisen.zusatzleistung', pretty=True, indent=2, output=fp, pks=rpks)
"""


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        for model in (
                # TODO: for `autor_id` + `zuletzt_bearbeitet_von`;
                #       but we're setting them NULL for now
                #
                # "User",
                # need to get dependencies correct somehow;
                # using alphabetical order otherwise
                #
                "Reise",
                # ========
                "Abfahrtszeiten",
                # "Angebot",                         # NOTE: empty
                # "Auftragsbestaetigung",            # NOTE: empty
                "Ausflugspaket",
                "Reisetage",
                # "AusflugspaketeZuReisetagen",      # NOTE: empty
                "Preis",
                "Ausflugspaketpreise",
                "Reisepreise",
                "ReisepreisZusatz",
                "Bildanbieter",
                "Bild",
                "Reisebilder",
                "Zielregion",
                # "Bildzielregionen",                # NOTE: empty
                "Reisezielregionen",
                "Fruehbucherrabatt",
                "Hinweis",
                "Reisehinweise",
                "Katalog",
                "Reisekatalogzugehoerigkeit",
                "Kategorie",
                "Reisekategorien",
                "LeistungenAusflugspaket",
                "LeistungenReise",
                # "Reiseangebote",                    # NOTE: empty
                # "Reiseauftragsbestaetigungen",      # NOTE: empty
                "Reisebeschreibung",
                "Reisetermine",
                "Zusatzleistung",
        ):
            call_command(
                "loaddata",
                "{}.json".format(model),
                app="reisen"
            )
