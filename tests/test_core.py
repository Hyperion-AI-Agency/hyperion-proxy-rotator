import time

import pytest

from proxy_rotator import ProxyRotator

POOL = ["http://p1:8000", "http://p2:8000", "http://p3:8000"]


def test_empty_pool_raises():
    with pytest.raises(ValueError):
        ProxyRotator([])


def test_unknown_strategy_raises():
    with pytest.raises(ValueError):
        ProxyRotator(POOL, strategy="spiral")


def test_deduplicates_preserving_order():
    rot = ProxyRotator(["a", "b", "a", "c"], strategy="round_robin")
    assert [rot.next() for _ in range(4)] == ["a", "b", "c", "a"]


def test_round_robin_cycles_in_order():
    rot = ProxyRotator(POOL, strategy="round_robin")
    assert [rot.next() for _ in range(6)] == POOL + POOL


def test_random_stays_within_pool():
    rot = ProxyRotator(POOL, strategy="random")
    assert {rot.next() for _ in range(50)} <= set(POOL)


def test_bad_proxy_is_skipped_until_cooldown_expires():
    rot = ProxyRotator(POOL, strategy="round_robin", cooldown=10)
    rot.mark_bad("http://p1:8000")

    picks = {rot.next() for _ in range(4)}
    assert "http://p1:8000" not in picks


def test_cooldown_expiry_restores_proxy():
    rot = ProxyRotator(POOL, strategy="round_robin", cooldown=0.05)
    rot.mark_bad("http://p1:8000")
    time.sleep(0.06)

    picks = {rot.next() for _ in range(3)}
    assert "http://p1:8000" in picks


def test_all_blocked_returns_soonest_recovering():
    rot = ProxyRotator(["a", "b"], strategy="round_robin", cooldown=100)
    rot.mark_bad("a")
    rot.mark_bad("b")
    rot.cooldown = 1
    rot.mark_bad("a")  # a now recovers sooner than b

    assert rot.next() == "a"


def test_mark_good_clears_penalty():
    rot = ProxyRotator(["a", "b"], strategy="round_robin", cooldown=100)
    rot.mark_bad("a")
    rot.mark_good("a")

    assert {rot.next() for _ in range(2)} == {"a", "b"}
