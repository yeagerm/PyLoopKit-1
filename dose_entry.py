#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 09:57:26 2019

@author: annaquinlan

Github URL: https://github.com/tidepool-org/LoopKit/blob/
57a9f2ba65ae3765ef7baafe66b883e654e08391/LoopKit/InsulinKit/DoseEntry.swift
"""
from date import time_interval_since
from dose import DoseType


def net_basal_units(type_, value, start, end, scheduled_basal_rate):
    """ Find the units of insulin delivered, net of any scheduled basal rate
        (if dose is a temp basal)

    Arguments:
    type_ -- type of dose (basal, bolus, suspend, etc)
    value -- if bolus: amount given, if temp basal: temp rate (U/hr)
    start -- datetime object representing start of dose
    end -- datetime object representing end of dose
    scheduled_basal_rate -- the rate scheduled during the time the dose was
                            given (0 for boluses)

    Output:
    Bolus amount (if a bolus), or basal units given, net of whatever the
    schedule basal is
    """
    MINIMUM_MINIMED_INCREMENT = 20

    if type_ == DoseType.bolus:
        return value

    elif type_ == DoseType.basal:
        return 0

    hours_ = hours(end, start)

    if type_ == DoseType.suspend:
        units = -scheduled_basal_rate * hours_
    else:
        units = (value - scheduled_basal_rate) * hours_

    # round to the basal increments that the pump supports
    return round(units * MINIMUM_MINIMED_INCREMENT) / MINIMUM_MINIMED_INCREMENT


def total_units_given(type_, value, start, end):
    """ Find total units given for a dose """
    if type_ in [DoseType.bolus, DoseType.suspend]:
        return value

    return value * hours(end, start)


def hours(start_date, end_date):
    """ Find hours between two dates for the purposes of calculating basal
        delivery
    """
    return abs(time_interval_since(end_date, start_date))/3600  # secs -> hrs
