from datetime import datetime, timedelta
from typing import Tuple, List
from collections import namedtuple

Interval = Tuple[timedelta, int]
AntiSpamInterval = namedtuple("AntiSpamInterval", ["period", "frequency"])


class AntiSpam:
    """
    Custom class which is more flexible than using discord.py's
    :func:`discord.ext.commands.cooldown`.

    Can be intialized with a custom set of intervals
    These should be provided as a list of tuples in the form
    (timedelta, quantity)

    Where quantity represents the maximum amount of times
    something should be allowed in an interval.
    """

    # TODO : Decorator interface for command check using `spammy`
    # with insertion of the antispam element into context
    # for manual stamping on successful command completion

    default_intervals = [
        (timedelta(seconds=5), 3),
        (timedelta(minutes=1), 5),
        (timedelta(hours=1), 10),
        (timedelta(days=1), 24),
    ]

    def __init__(self, intervals: List[Interval]):
        self.__event_timestamps = []
        _itvs = intervals if intervals else self.default_intervals
        self.__intervals = [AntiSpamInterval(*x) for x in _itvs]
        self.__discard_after = max([x.period for x in self.__intervals])

    def __interval_check(self, interval: AntiSpamInterval):
        return (
            len([t for t in self.__event_timestamps if (t + interval.period) > datetime.utcnow()])
            >= interval.frequency
        )

    @property
    def spammy(self):
        """
        Used to check if any intervals are active. Intervals are marked
        from the stamp function.

        This function takes no arguments.

        Returns
        -------
        bool
            Whether an antispam interval has been met.
        """
        return any(self.__interval_check(x) for x in self.__intervals)

    def stamp(self):
        """
        Used to mark an event that counts against the intervals.

        It will increment the interval's quantity, and will escalate to
        the next interval if that quantity is exceeded.

        This function takes no arguments.
        """
        self.__event_timestamps.append(datetime.utcnow())
        self.__event_timestamps = [
            t for t in self.__event_timestamps if t + self.__discard_after > datetime.utcnow()
        ]
