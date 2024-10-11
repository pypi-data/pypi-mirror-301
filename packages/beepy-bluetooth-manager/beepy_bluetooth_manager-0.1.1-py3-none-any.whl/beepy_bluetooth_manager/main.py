import asyncio
import time
import subprocess
from textual.binding import Binding
from textual.app import App, ComposeResult
from textual.widgets import (
    Footer,
    Label,
    ListItem,
    ListView,
    Rule,
    LoadingIndicator,
    Checkbox,
    Static,
    Header,
)
from textual.reactive import reactive


def is_bluetooth_enabled() -> bool:
    return (
        subprocess.run(
            'bluetoothctl show | grep "Powered: yes"',
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        == 0
    )


def toggle_bluetooth() -> None:
    if not is_bluetooth_enabled():
        subprocess.run(
            "rfkill unblock bluetooth && bluetoothctl power on",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.run(
            "bluetoothctl power off",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


class BluetoothStatusCheckbox(Static):
    def compose(self) -> ComposeResult:
        yield Checkbox("Bluetooth enabled?", is_bluetooth_enabled(), id="initial_focus")

    def on_checkbox_changed(_, __):
        toggle_bluetooth()


class BluetoothDevicesList(Static):
    BINDINGS = [
        Binding("k", "cursor_up", "Up", show=True),
        Binding("j", "cursor_down", "Down", show=True),
        Binding("space", "select_cursor", "Select", show=True),
    ]

    async def on_key(self, event) -> None:
        """Handle key events directly for Enter key."""
        if event.key == "enter":
            await self.action_select_cursor()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lv = ListView()

    def action_cursor_up(self):
        self.lv.action_cursor_up()

    def action_cursor_down(self):
        self.lv.action_cursor_down()

    async def connect(self, device_id: str):
        self.lv.disabled = True
        subprocess.run(
            f"bluetoothctl connect {device_id}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.lv.disabled = False

    async def action_select_cursor(self):
        self.notify(f"Connecting to {self.devices[self.lv.index][1]}", title="")
        asyncio.create_task(self.connect(self.devices[self.lv.index][0]))

    async def get_bluetooth_devices(self):
        subprocess.run(
            "bluetoothctl --timeout 10 scan on",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        output = subprocess.run(
            "bluetoothctl devices",
            shell=True,
            capture_output=True,
            text=True,
        ).stdout

        self.devices = [
            (d.split(" ")[1], " ".join(d.split(" ")[2:]))
            for d in output.split("\n")
            if d
        ]

        self.lv.clear()
        self.lv.extend([ListItem(Label(device[1])) for device in self.devices])
        self.lv.refresh()

    def compose(self) -> ComposeResult:
        yield Label("Device List")
        yield self.lv
        # yield LoadingIndicator()

    def on_mount(self) -> None:
        asyncio.create_task(self.get_bluetooth_devices())


class BluetoothManagerApp(App):
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield BluetoothStatusCheckbox()
        yield Rule()
        yield BluetoothDevicesList()
        yield Footer()

    def on_mount(self):
        self.query_one("#initial_focus", Checkbox).focus()


def main():
    BluetoothManagerApp().run()


if __name__ == "__main__":
    main()
