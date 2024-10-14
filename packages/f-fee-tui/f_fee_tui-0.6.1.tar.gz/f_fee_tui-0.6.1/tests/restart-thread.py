import random
import threading
import time
from queue import Queue

from textual.app import App
from textual.app import ComposeResult
from textual.binding import Binding
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Footer
from textual.widgets import Header


class RuntimeErrorCaught(Message):
    def __init__(self, message: str, exc: Exception):
        super().__init__()
        self.msg = message
        self.exc = exc


class ThreadCrashed(Message):
    def __init__(self, message: str, exc: Exception):
        super().__init__()
        self.msg = message
        self.exc = exc


class Command(threading.Thread):
    def __init__(self, app: App, command_q: Queue):
        super().__init__()
        self._app = app
        self._command_q = command_q
        self._canceled = threading.Event()

    def run(self):
        self._app.log("Command thread started ...")

        while True:
            if self._canceled.is_set():
                break

            try:
                if random.random() < 0.1:
                    raise RuntimeError("A fake runtime error.")
            except RuntimeError as exc:
                self._app.get_screen("master").post_message(
                    ThreadCrashed("master: We got a RuntimeError in the Command thread ...", exc)
                )
                self._app.post_message(
                    RuntimeErrorCaught("app: We got a RuntimeError in the Command thread ...", exc)
                )

                if self.sleep_or_break():
                    break

                self._app.notify("Re-activating Command Thread after 5.0s")

    def sleep_or_break(self) -> bool:
        for _ in range(100):
            if self._canceled.is_set():
                is_cancelled = True
                break
            time.sleep(0.1)
        else:
            is_cancelled = False

        return True if is_cancelled else False

    def cancel(self) -> None:
        self._canceled.set()


class MasterScreen(Screen):

    def __init__(self):
        super().__init__()
        self._command_q = Queue()
        self._commanding_thread = Command(self.app, self._command_q)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self._commanding_thread.start()

    def on_unmount(self) -> None:
        self._commanding_thread.cancel()

        if self._commanding_thread.is_alive():
            self._commanding_thread.join()

    def on_thread_crashed(self, message: ThreadCrashed):
        self.log(f"{message.msg}: {message.exc}")


class ThreadApp(App):
    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    SCREENS = {"master": MasterScreen}

    def on_mount(self):
        self.push_screen("master")

    def on_runtime_error_caught(self, message: RuntimeErrorCaught):
        self.log(f"{message.msg}: {message.exc}")


if __name__ == '__main__':

    app = ThreadApp()
    app.run()
