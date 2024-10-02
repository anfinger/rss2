import io
import pytest
from pytest_django.asserts import assertHTMLEqual
from reisen.models import Angebot, Reise, Reisetermine

ANGEBOT_TITEL = "Supi dupi, los mit Pupi!"


@pytest.mark.django_db
@pytest.fixture
def mein_angebot():
    angebot, _ = Angebot.objects.get_or_create(
        titel=ANGEBOT_TITEL,
    )
    yield angebot
    angebot.delete()


@pytest.mark.django_db
def test_home_stuff(mein_angebot):
    assert Angebot.objects.count() == 1
    assert Angebot.objects.first().titel == ANGEBOT_TITEL


@pytest.mark.django_db
@pytest.mark.parametrize(
    "reise_pk",
    [
        # -- Mehrtagesfahrten --
        'b463933c6815449ea42054f86df1bd5c',     # Rom
        '194ea4467b644bdb93398c6daeb78211',     # Dankeschoen
        'c66486e37a5f44b7bece6c0a3db92e54',     # Flusskreuzfahrt Douro
        # -- Tagesfahrten --
        # '208b718e19d04777beb821ce988caf04',     # Fahrt ins Blaue
        # '4359c2aa63524b35a225ad6182c4e76a',     # Ozeaneum
        # '7690921ab795480380830684e5c0fbfe',     # Elbphilharmonie
        # -- Musicals & Shows
        '7fe42660eeb44b5aa4f82dfba5712353',     # Musikalischer Advent in Leipzig
    ]
)
def test_home_detail(django_db_setup, client, mocker, reise_pk):
    endpoint = "/home/detail/"
    # reise = Reise.objects.get(pk=reise_pk)
    erster_reisetermin = Reisetermine.objects.filter(
        reise_id=reise_pk).only("markierung", "datum_ende").first()
    # TODO: use multi-value dict thingy + freezegun
    #
    data = dict(
        dm=erster_reisetermin.markierung,
        datum=erster_reisetermin.datum_ende.strftime("%d. %m. %Y")
    )
    # client.enforce_csrf_checks = False
    # NOTE: had to replace all `csrfmiddlewaretoken` input's values in html fixtures
    #  w/ this manually...
    #
    mocker.patch("django.template.context_processors.get_token", return_value="MOCKEDCSRFTOKEN")
    response = client.get(endpoint + reise_pk + "/", data)

    with io.open("reisen/fixtures/{}-detail.html".format(reise_pk), "r", encoding="utf8") as html:
        assertHTMLEqual(response.content.decode("utf8"), html.read())


@pytest.mark.django_db
@pytest.mark.parametrize("path", ["neustart", "tagesfahrten", "mehrtagesfahrten"])
def test_home_neustart(django_db_setup, client, mocker, path):
    endpoint = "/home/{}/".format(path)
    data = dict(version="nicepage") if path == "neustart" else dict()

    if path == "tagesfahrten":
        # NOTE: only "tagesfahrten" seems to have it!?
        #
        mocker.patch("django.template.context_processors.get_token", return_value="MOCKEDCSRFTOKEN")

    response = client.get(endpoint, data)

    with io.open("reisen/fixtures/{}.html".format(path), "r", encoding="utf8") as html:
        assertHTMLEqual(response.content.decode("utf8"), html.read())

