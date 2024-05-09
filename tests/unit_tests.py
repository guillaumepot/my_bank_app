"""
This file is used to run unit tests with Pytest
"""


"""
LIBS
"""
import os
import pytest
from datetime import datetime

from myBankPackage import generate_uuid

"""

"""
def test_generate_uuid() -> None:
    """
    Test the generate_uuid function.
    """
    uuid = generate_uuid()
    assert len(uuid) == 32
    assert isinstance(uuid, str)