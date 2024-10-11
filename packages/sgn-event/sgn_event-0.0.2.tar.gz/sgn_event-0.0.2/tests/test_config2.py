#!/usr/bin/env python3

import sys
import numpy
import yaml
from sgnevent.base import dtype_from_config, EventBuffer

def test_config(config):
    #dtype = {n: dtype_from_config(config[n]) for n in ('filter', 'simulation', 'data', 'trigger', 'event')}
    dtype = dtype_from_config(config['trigger'])
    print (dtype)
    times = numpy.ones((2, 500))
    snrs = numpy.random.rand(2, 500)
    phases = numpy.random.rand(2, 500)

    #event_dict = {n: EventBuffer(0, 1_000_000_000, data=numpy.zeros(3, d)) for (n,d) in dtype.items()}
    #data = numpy.stack([times, snrs, phases], dtype=dtype)
    events = EventBuffer(0, 1_000_000_000, data=numpy.zeros((2, 500), dtype))
    print (events)
    events.data['time'] = times
    events.data['snr'] = snrs
    events.data['phase'] = phases
 
with open(sys.argv[1]) as f:
    config = yaml.safe_load(f)

test_config(config)

