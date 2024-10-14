# -*- coding: utf-8 -*-

import unittest
import os
import sys
import pathlib
import unittest.mock as mock

from unittest.mock import patch


class TestTrain(unittest.TestCase):

    @mock.patch.dict(
        os.environ, {"WXBHOME": str(pathlib.Path(__file__).parent.absolute())}
    )
    def test_train(self):
        import wxbtool.wxb as wxb

        testargs = ["wxb", "train", "-m", "models.tgt_mdl", "-b", "1", "-n", "1"]
        with patch.object(sys, "argv", testargs):
            wxb.main()
