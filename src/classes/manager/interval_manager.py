import threading
import time
from ..abstract.manager import Manager
from ...utils.error.error_handler import handle_error


class Interval:
    """
    JS의 setInterval/clearInterval에 해당하는 반복 실행 타이머
    """
    def __init__(self, callback, interval_ms):
        self.callback = callback
        self.interval = interval_ms / 1000  # 초 단위 변환
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        while not self._stop_event.is_set():
            try:
                self.callback()
            except Exception as e:
                print(f"[Interval] 오류 발생: {e}")
            time.sleep(self.interval)

    def start(self):
        self.thread.start()

    def stop(self):
        self._stop_event.set()


class IntervalManager(Manager):
    _instance = None

    def __init__(self):
        if IntervalManager._instance:
            return
        super().__init__()
        self.intervals = {}  # id -> type -> Interval 객체
        IntervalManager._instance = self

    @staticmethod
    def get_instance():
        if IntervalManager._instance is None:
            IntervalManager._instance = IntervalManager()
        return IntervalManager._instance

    def add(self, id, callback, interval, type='none'):
        if id not in self.intervals:
            self.intervals[id] = {}

        if type in self.intervals[id]:
            # 기존 타이머가 있으면 중복 실행 방지
            self.intervals[id][type].stop()

        timer = Interval(callback, interval)
        self.intervals[id][type] = timer
        timer.start()

    def remove(self, id, type=None):
        try:
            if id in self.intervals:
                current = self.intervals[id]

                if type is None:
                    for timer in current.values():
                        timer.stop()
                    del self.intervals[id]
                else:
                    if type in current:
                        current[type].stop()
                        del current[type]
                        if not current:
                            del self.intervals[id]
        except Exception as err:
            print(f"[IntervalManager] 에러: {err}")

    def clear_all(self):
        for id in list(self.intervals.keys()):
            self.remove(id)
