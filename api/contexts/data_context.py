class AppContext:
    context = {
        "default_center": [52.28244, 104.298423],
        "selected_id": 0,
        "selected_ids": [],
        "roads_to_report": [],
        "current_road": 0,
        "current_road_name": "",
        "stop_thread": False,
        "selected_template": None,
        "form_variables": {},
    }

    @classmethod
    def get_context_from_db(cls) -> set[str]:
        """
        Возвращаем все переменные для генерации отчета
        которые будут заполняться из базы
        """
        return {
            "road_title",
            "road_length",
            "covers",
            "signs",
            "light",
            "barriers",
            "tubes",
            "cross",
            "scheme",
        }

    @classmethod
    def get_form_context(cls, variables: set[str]):
        """
        Отдаем переменные которые нужно заполнить через форму
        """
        cls.context["form_variables"] = {}
        for v in variables - cls.get_context_from_db():
            cls.context["form_variables"][v] = ""
        print(cls.context["form_variables"])
