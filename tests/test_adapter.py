import pytest
import requests
import responses

from proxy_rotator import ProxyRotator, RotatingProxyAdapter

URL = "https://target.test/"
PA = "http://pA:1"
PB = "http://pB:1"


def make_session(attempts=3, cooldown=100):
    rot = ProxyRotator([PA, PB], strategy="round_robin", cooldown=cooldown)
    session = requests.Session()
    session.mount("https://", RotatingProxyAdapter(rot, attempts=attempts))
    return session, rot


def test_attempts_must_be_positive():
    with pytest.raises(ValueError):
        RotatingProxyAdapter(ProxyRotator([PA]), attempts=0)


@responses.activate
def test_retires_bad_proxy_and_returns_good_response():
    responses.add(responses.GET, URL, status=503)
    responses.add(responses.GET, URL, status=200, body="ok")

    session, rot = make_session()
    r = session.get(URL)

    assert r.status_code == 200
    assert r.text == "ok"
    assert len(responses.calls) == 2
    assert PA in rot._blocked
    assert PB not in rot._blocked


@responses.activate
def test_retries_on_transport_error():
    responses.add(responses.GET, URL, body=requests.exceptions.ConnectionError("boom"))
    responses.add(responses.GET, URL, status=200, body="ok")

    session, rot = make_session()
    r = session.get(URL)

    assert r.status_code == 200
    assert PA in rot._blocked


@responses.activate
def test_raises_when_all_attempts_error():
    responses.add(responses.GET, URL, body=requests.exceptions.ConnectionError("boom"))

    session, _ = make_session(attempts=2)
    with pytest.raises(requests.exceptions.ConnectionError):
        session.get(URL)


@responses.activate
def test_returns_last_response_when_all_attempts_retire():
    responses.add(responses.GET, URL, status=503, body="blocked")

    session, _ = make_session(attempts=2)
    r = session.get(URL)

    assert r.status_code == 503
    assert r.text == "blocked"
