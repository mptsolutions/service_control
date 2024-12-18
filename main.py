import log_handler
import logging
from pystemd.systemd1 import Manager, Unit
from nicegui import ui
from nicegui.events import ValueChangeEventArguments
from config import SERVICES

# Class for creating a service object
class system_service:
    def __init__(self, service):
        self.service = service
        with Unit(service.encode()) as sd_unit:
            self.name = sd_unit.Unit.Description.decode("utf-8")
            logging.info(f"Found new service: {self.name}")

    # Function to determine if service is enabled
    def is_enabled(self, service):
        with Manager() as manager:
            if manager.Manager.GetUnitFileState(service).decode("utf-8") == "enabled":
                logging.info(f"{self.name} is enabled")
                return True
        logging.info(f"{self.name} is disabled")
        return False

    # Function to determine if service is running
    def is_running(self, service):
        with Unit(service.encode()) as unit:
            if unit.Unit.SubState.decode("utf-8") == "running":
                logging.info(f"{self.name} is running")
                return True
        logging.info(f"{self.name} is stopped")
        return False

    # Function to enable or disable service
    def enable(self, event: ValueChangeEventArguments):
        with Manager() as manager:
            if event.value:
                manager.Manager.EnableUnitFiles(["f1_buzzer.service"], False, True)
                ui.notify(f'Enabled {self.name}')
                logging.info(f'Enabled {self.name}')
                return
            manager.Manager.DisableUnitFiles([self.service], False)
            ui.notify(f'Disabled {self.name}')
            logging.info(f'Disabled {self.name}')
    
    # Function to start or stop service
    def start(self, event: ValueChangeEventArguments):
        with Unit(self.service) as sd_unit:
            if event.value:
                sd_unit.Unit.Start(b'replace')
                ui.notify(f'Started {self.name}')
                return
            sd_unit.Unit.Stop(b'replace')
            ui.notify(f'Stopped {self.name}')

    # Function to build UI elements for service
    def build_ui(self):
        with ui.column().classes("w-full items-center"):
            self.label = ui.label(self.name).classes("title-box")
            with ui.row():
                self.enable_switch = ui.switch("Enabled", on_change=self.enable, value=self.is_enabled(self.service))
                self.start_switch = ui.switch("Started", on_change=self.start, value=self.is_running(self.service))

# Function to reboot system on button press
def reboot_click():
    ui.notify("Rebooting now...")
    with Manager() as manager:
        manager.Manager.Reboot()


# Start of module
if __name__ in {"__main__", "__mp_main__"}:
    title_style = "w-full bg-blue-500 p-1 text-center shadow-lg rounded-lg text-white text-2xl italic font-extrabold;"
    ui.add_head_html('<style type="text/tailwindcss"> @layer components { .title-box { @apply ' + title_style + '} } </style>')

    service_objs = []
    for service_filename in SERVICES:
        if not service_filename:
            logging.error("Service list not set up in config.py")
            exit(-1)
        cur_service = system_service(service_filename)
        cur_service.build_ui()
        service_objs.append(cur_service)
        
    with ui.column().classes("w-full items-center"):
        with ui.row(align_items="center"):
            ui.button("Reboot System", on_click=reboot_click)
    
    ui.page_title('Service Control')
    ui.run(dark=True)
    