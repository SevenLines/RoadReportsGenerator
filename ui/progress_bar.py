from nicegui import ui
from ui.context import context, change_stop_thread


class ReportProgressBar:
    def __init__(self):
        with ui.dialog() as self.dialog, ui.card().style(
            "width: 100%"
        ) as self.progress_bar_card:
            self.label = (
                ui.label("Текущий документ: ")
                .bind_text_from(
                    context, "current_road_name", lambda v: "Текущий документ: " + v
                )
                .style("font-weight: bold;")
            )
            with ui.row().style("width: 100%"):
                self.progress_bar = (
                    ui.linear_progress(show_value=True)
                    .bind_value_from(
                        context, "current_road", lambda v: f"{v * 100:.2f}%"
                    )
                    .props("rounded outlined dense")
                )
                self.decline_button = ui.button(
                    "Отменить", on_click=lambda: self.stop_report()
                )

    def stop_report(self):
        change_stop_thread()
        self.progress_bar.value = 0
        context["current_road"] = 0
        self.hide()

    def hide(self):
        self.dialog.close()

    def show(self):
        self.dialog.open()
