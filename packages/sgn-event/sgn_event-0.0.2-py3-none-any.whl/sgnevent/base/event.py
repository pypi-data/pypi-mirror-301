from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any
import numpy

from sgn.base import Frame
from sgnts.base import TSSlice, TSSlices


def type_from_sqlite(col):
    if col["type"] == "INTEGER":
        return "i8"
    if col["type"] == "REAL":
        return "f8"
    if col["type"] == "TEXT":
        return "U%d" % col["size"]


def dtype_from_config(config):
    return numpy.dtype(
        [(col["name"], type_from_sqlite(col)) for col in config["columns"]]
    )


@dataclass
class EventBuffer:
    """Event buffer with associated metadata.

    Parameters
    ----------
    ts: int
        Start time of event buffer in ns
    te: int
        End time of event buffer in ns
    data: Any
        Data of the event
    """

    ts: int = None
    te: int = None
    data: Any = None

    def __post_init__(self):
        assert isinstance(self.ts, int) and isinstance(self.te, int)
        assert self.ts <= self.te

    def __repr__(self):
        with numpy.printoptions(threshold=3, edgeitems=1):
            return "EventBuffer(ts=%d, te=%d, data=%s)" % (
                self.ts,
                self.te,
                self.data,
            )

    def __bool__(self):
        return self.data is not None

    @property
    def slice(self):
        return TSSlice(self.ts, self.te)

    @property
    def duration(self):
        return self.te - self.ts

    @property
    def is_gap(self):
        if self.data is None:
            return True
        else:
            return False

    def __contains__(self, item):
        if isinstance(item, int):
            return self.ts <= item <= self.te
        else:
            return False

    def __lt__(self, item):
        if isinstance(item, int):
            return self.te < item
        elif isinstance(item, EventBuffer):
            return self.te < item.te

    def __le__(self, item):
        if isinstance(item, int):
            return self.te <= item
        elif isinstance(item, EventBuffer):
            return self.te <= item.te

    def __ge__(self, item):
        if isinstance(item, int):
            return self.ts >= item
        elif isinstance(item, EventBuffer):
            return self.te >= item.te

    def __gt__(self, item):
        if isinstance(item, int):
            return self.ts > item
        elif isinstance(item, EventBuffer):
            return self.te > item.te

    def pad_buffer(self, ts, te, data=None):
        assert ts < self.ts
        return EventBuffer(
            ts=ts,
            te=self.ts,
            data=data,
        )

    # FIXME HERE DOWN


#    def sub_buffer(self, slc, gap=False):
#            assert slc in self.slice
#            startsamples, stopsamples = Offset.tosamples(slc.start - self.offset, self.sample_rate), Offset.tosamples(slc.stop - self.offset, self.sample_rate)
#            gap = gap and self.data is not None
#            if not gap:
#                data = self.data[..., startsamples:stopsamples]
#            else:
#                data = None
#            return SeriesBuffer(
#                    offset=slc.start,
#                    sample_rate=self.sample_rate,
#                    data=data,
#                    shape=self.shape[:-1] + (stopsamples - startsamples,))
#
#    def split(self, boundaries, contiguous = False):
#        out = []
#        if isinstance(boundaries, int):
#            boundaries = TSSlices(self.slice.split(boundaries))
#        if not isinstance(boundaries, TSSlices):
#            raise NotImplementedError
#        for slc in boundaries.slices:
#            assert slc in self.slice
#            out.append(self.sub_buffer(slc))
#        if contiguous:
#            gap_boundaries = boundaries.invert(self.slice)
#            for slc in gap_boundaries.slices:
#                out.append(self.sub_buffer(slc, gap=True))
#        return sorted(out)


@dataclass
class EventFrame(Frame):
    """An sgn Frame object that holds a dictionary of events

    Parameters
    ----------
    events : dict
        Dictionary of EventBuffers

    """

    events: dict = None

    def __post_init__(self):
        super().__post_init__()
        assert len(self.events) > 0

    def __getitem__(self, item):
        return self.events[item]

    def __iter__(self):
        return iter(self.events)

    def __repr__(self):
        out = "%s ::" % self.metadata["__graph__"]
        for evt in self:
            out += "\n\t%s" % evt
        return out

    # FIXME HERE DOWN


#    @property
#    def offset(self):
#        return self.buffers[0].offset
#
#    @property
#    def end_offset(self):
#        return self.buffers[-1].end_offset
#
#    @property
#    def slice(self):
#        return TSSlice(self.offset, self.end_offset)
#
#    @property
#    def shape(self):
#        return self.buffers[0].shape[:-1] + (sum(b.samples for b in self.buffers),)
