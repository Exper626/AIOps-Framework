import time
from contextlib import contextmanager


class Trace:
    """Records what each pipeline step received, returned and how long it took.

    Sent to the frontend as the "Pipeline trace" panel when DEBUG_TRACE is on.
    """

    def __init__(self):
        self.steps: list[dict] = []
        self._started = time.perf_counter()

    @contextmanager
    def step(self, name: str, model: str | None = None, input=None):
        entry: dict = {"name": name}

        if model:
            entry["model"] = model

        if input is not None:
            entry["input"] = input

        started = time.perf_counter()

        try:
            yield entry
        except Exception as error:
            entry.setdefault("error", str(error))
            raise
        finally:
            entry["ms"] = round((time.perf_counter() - started) * 1000)
            self.steps.append(entry)

    def to_dict(self) -> dict:
        return {
            "steps": self.steps,
            "total_ms": round((time.perf_counter() - self._started) * 1000),
        }

    def summary(self) -> str:
        """One line for the server logs, e.g. "planner=840ms answer=5230ms"."""
        return " ".join(f"{step['name']}={step['ms']}ms" for step in self.steps)
