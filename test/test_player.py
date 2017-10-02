# -*- coding: utf-8 -*-

from nose.tools import ok_, nottest

from synthesizer import Player


def test_enumerate_device():
    player = Player()
    player.enumerate_device()
    ok_("enumerate_device() succeeded.")


@nottest
def test_open_default_stream():
    player = Player()
    player.open_stream()
    ok_("open_stream() succeeded.")
