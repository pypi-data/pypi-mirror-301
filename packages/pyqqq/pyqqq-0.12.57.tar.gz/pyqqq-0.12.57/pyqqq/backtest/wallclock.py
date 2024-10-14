import asyncio
import datetime as dtm
from typing import Optional


class WallClock:

    def __init__(self, live_mode: bool = True, start_time: Optional[dtm.datetime] = None, end_time: Optional[dtm.datetime] = None, tzinfo: Optional[dtm.tzinfo] = None):
        self.live_mode = live_mode
        self.tzinfo = tzinfo

        if not live_mode:
            self.current_time = start_time
            self.end_time = end_time if end_time is not None else dtm.datetime.now()

            if self.tzinfo is not None:
                self.current_time = self.current_time.astimezone(self.tzinfo)
                self.end_time = self.end_time.astimezone(self.tzinfo)

        self.on_time_change = None
        self.on_before_time_change = None

    def now(self) -> dtm.datetime:
        if self.live_mode:
            return dtm.datetime.now(self.tzinfo)
        else:
            if self.current_time > dtm.datetime.now(self.tzinfo):
                raise ValueError("backtesting time is must be less than current time")

            return self.current_time

    def today(self) -> dtm.date:
        return self.now().date()

    def is_alive(self) -> bool:
        if self.live_mode:
            return True
        else:
            return self.current_time <= self.end_time

    async def sleep(self, seconds: float):
        if self.live_mode:
            await asyncio.sleep(seconds)
        else:
            before = self.current_time
            after = before + dtm.timedelta(seconds=seconds)

            if self.on_before_time_change:
                self.on_before_time_change(before, after)

            self.current_time = after

            if self.on_time_change:
                self.on_time_change(self.current_time, before)
