# -*- coding: utf-8 -*-
import os

PATH_LIB = os.path.dirname(__file__)
PATH_FURINA = os.path.dirname(PATH_LIB)

PATH_ROOT = os.getcwd()
PATH_ASSERT = os.path.join(PATH_ROOT, "assert")
PATH_ASSERT_ENGINE = os.path.join(PATH_ASSERT, "engine")
PATH_ASSERT_LIB = os.path.join(PATH_ASSERT, "lib")
PATH_ASSERT_MODEL = os.path.join(PATH_ASSERT, "model")
