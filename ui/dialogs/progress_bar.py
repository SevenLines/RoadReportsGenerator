from nicegui import ui
from api.contexts.data_context import AppContext


class ReportProgressBar:
    def __init__(self):
        with ui.dialog() as self.dialog, ui.card().style(
            "width: 100%"
        ) as self.progress_bar_card:
            with ui.row().style("width:100%"):
                self.label = (
                    ui.label("Текущий документ: ")
                    .bind_text_from(
                        AppContext.context,
                        "current_road_name",
                        lambda v: "Текущий документ: " + v,
                    )
                    .style("font-weight: bold;")
                )
                ui.spinner(size="1rem")
            with ui.row().style("width:100%"):
                self.progress_bar = (
                    ui.linear_progress(show_value=True)
                    .bind_value_from(
                        AppContext.context,
                        "current_road",
                        lambda v: f"{v * 100:.2f}%",
                    )
                    .props("rounded")
                )
                self.decline_button = ui.button(
                    "Отменить", on_click=lambda: self.stop_report()
                )
        self.dialog.bind_visibility_from(
            AppContext.context, "stop_thread", lambda v: not v
        )

    def stop_report(self):
        AppContext.context["stop_thread"] = True
        AppContext.context["current_road"] = 0
        self.progress_bar.value = 0
        self.hide()

    def hide(self):
        self.dialog.close()

    def show(self):
        self.dialog.open()
