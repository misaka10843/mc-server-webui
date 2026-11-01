from dataclasses import dataclass
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo


@dataclass(frozen=True, slots=True)
class IdlePolicy:
    day_timeout: timedelta = timedelta(minutes=90)
    night_timeout: timedelta = timedelta(minutes=30)
    night_start: time = time(23, 30)
    day_start: time = time(9, 0)
    timezone: str = "Asia/Hong_Kong"

    def __post_init__(self) -> None:
        if self.day_timeout <= timedelta(0) or self.night_timeout <= timedelta(0):
            raise ValueError("Idle timeouts must be positive")
        if self.night_start <= self.day_start:
            raise ValueError("Night interval must cross midnight")
        ZoneInfo(self.timezone)

    def threshold(self, now: datetime) -> timedelta:
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("now must be timezone-aware")
        local_time = now.astimezone(ZoneInfo(self.timezone)).time()
        if local_time >= self.night_start or local_time < self.day_start:
            return self.night_timeout
        return self.day_timeout

    def is_due(self, now: datetime, idle_seconds: float) -> bool:
        if idle_seconds < 0:
            raise ValueError("idle_seconds must be non-negative")
        return idle_seconds >= self.threshold(now).total_seconds()


@dataclass(slots=True)
class IdleTracker:
    ready: bool = False
    player_count: int = 0
    idle_since: float | None = None

    def update(self, *, ready: bool, player_count: int, monotonic_now: float) -> None:
        if player_count < 0:
            raise ValueError("player_count must be non-negative")
        if self.idle_since is not None and monotonic_now < self.idle_since:
            raise ValueError("monotonic time moved backwards")
        if not ready or player_count:
            self.idle_since = None
        elif not self.ready or self.player_count or self.idle_since is None:
            self.idle_since = monotonic_now
        self.ready = ready
        self.player_count = player_count

    def elapsed(self, monotonic_now: float) -> float | None:
        if self.idle_since is None:
            return None
        if monotonic_now < self.idle_since:
            raise ValueError("monotonic time moved backwards")
        return monotonic_now - self.idle_since
