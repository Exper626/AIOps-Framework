import time
from contextlib import contextmanager

from pipeline.errors import StepFailed, describe_error


class Trace:
    def __init__(self):
        self.steps: list[dict] = []
        self._started = time.perf_counter()

    @contextmanager
    def step(self, name: str, model=None, input=None, fallback: bool = False):
        entry: dict = {"name": name}

        if model is not None:
            entry["model"] = model.id
            entry["source"] = model.source

        if input is not None:
            entry["input"] = input

        started = time.perf_counter()

        try:
            yield entry
        except Exception as error:
            entry["error"] = describe_error(error, name, model)

            if not fallback:
                raise StepFailed(entry["error"]) from error

            entry["fallback"] = True
            print(f"[{name}] {entry['error']} (falling back)")
        finally:
            entry["ms"] = round((time.perf_counter() - started) * 1000)
            self.steps.append(entry)

    def to_dict(self) -> dict:
        return {
            "steps": self.steps,
            "total_ms": round((time.perf_counter() - self._started) * 1000),
        }

    def summary(self) -> str:
        return " ".join(f"{step['name']}={step['ms']}ms" for step in self.steps)
