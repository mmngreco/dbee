import numpy as np
import pandas as pd

from dbee.cli import _read

from .utils import DataBaseTest


def test_db():

    with DataBaseTest("test.db") as url:
        obtained = _read(url, "select * from Hero")
        expected = pd.DataFrame(
            {
                'id': {0: 1, 1: 2, 2: 3},
                'name': {0: 'Deadpond', 1: 'Spider-Boy', 2: 'Rusty-Man'},
                'secret_name': {
                    0: 'Dive Wilson',
                    1: 'Pedro Parqueador',
                    2: 'Tommy Sharp',
                },
                'age': {0: np.nan, 1: np.nan, 2: 48.0},
            }
        )

    pd.testing.assert_frame_equal(obtained, expected)
