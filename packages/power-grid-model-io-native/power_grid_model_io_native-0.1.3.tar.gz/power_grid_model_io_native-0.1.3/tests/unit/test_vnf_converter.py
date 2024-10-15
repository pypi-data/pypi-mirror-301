# SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
#
# SPDX-License-Identifier: MPL-2.0

from power_grid_model_io_native._core.power_grid_model_io_core import pgm_io_core


def test_nothing():
    assert pgm_io_core.error_code() == 0
    assert pgm_io_core.error_message() == ""
