# -*- coding: utf-8 -*-

from nose.tools import ok_

from synthesizer import Player


def test_enumerate_device():
    player = Player()
    player.enumerate_device()
    ok_("enumerate_device() succeeded.")


def test_open_default_stream():
    player = Player()
    player.open_stream()
    ok_("open_stream() succeeded.")
