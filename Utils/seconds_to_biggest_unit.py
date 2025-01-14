#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 30/03/2019

@author: Maurizio Ferrari Dacrema
"""


def seconds_to_biggest_unit(time_in_seconds):
    conversion_factor = [
        ("sec", 60),
        ("min", 60),
        ("hour", 24),
        ("day", 365),
    ]

    terminate = False
    unit_index = 0

    new_time_value = time_in_seconds
    new_time_unit = "sec"

    while not terminate:

        next_time = new_time_value / conversion_factor[unit_index][1]

        if next_time >= 1.0:
            new_time_value = next_time

            unit_index += 1
            new_time_unit = conversion_factor[unit_index][0]

        else:
            terminate = True

    return new_time_value, new_time_unit
