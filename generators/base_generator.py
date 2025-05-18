import datetime
import io
import os
from statistics import mean
from time import sleep

from PIL import Image
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chromium.webdriver import ChromiumDriver

from api.managers.sqlite import TemplateVariablesManager
from api.managers.road_factory import RoadManagerFactory
from generators.utils import RangeCustom, Range
from models import Road, High, Way, Attribute
import folium

from table_generators.base import TableGeneratorBase
from table_generators.generators import (
    CoverTypeTableAggregateGenerator,
    SignAggregateGenerator,
    CommunicationsAggregateGenerator,
    LightAggregateGenerator,
    BarriersAggregateGenerator,
    TubesAggregateGenerator,
    CrossAggregateGenerator,
)
from api.contexts.data_context import AppContext


class BaseGenerator(object):
    template = ""
    tables_generators = {}

    def test_generator(self, road_id, table_generator: type[TableGeneratorBase]):
        manager = RoadManagerFactory()
        with manager.db().session() as s:
            road = s.query(Road).filter(Road.id == road_id).first()
            high = (
                s.query(High)
                .join(Way, Way.id == High.way_id)
                .filter(Way.road_id == road.id)
                .first()
            )
        return table_generator(high.id, road, db)._get_raw_data()

    def generate(self, road_id, template_path:str, save_folder="output", with_image=False):
        # doc_template = DocxTemplate(os.path.join("templates", self.template))
        doc_template = DocxTemplate(template_path)
        doc = doc_template.get_docx()

        tables_to_fill = []

        manager = RoadManagerFactory()
        db = manager.db()
        with db.session() as s:
            road = s.query(Road).filter(Road.id == road_id).first()
            road_length = road.get_length(s)[1]
            high = (
                s.query(High)
                .join(Way, Way.id == High.way_id)
                .filter(Way.road_id == road.id)
                .first()
            )

        for table in doc.tables:
            key = table.rows[0].cells[0].text[1:-1].strip()
            generator_class = self.tables_generators.get(key)
            if generator_class:
                tables_to_fill.append(
                    {
                        "table": table,
                        "generator": generator_class,
                    }
                )

        for table_info in tables_to_fill:
            table_info["generator"](high.id, road, db).fill(table_info["table"], doc)

        covers = CoverTypeTableAggregateGenerator(high.id, road, db)._get_raw_data()
        covers["rest"] = road_length - covers["total"]

        context_from_db = {
            "road_title": road.Name,
            "road_length": road_length,
            # 'year': datetime.datetime.now().year,
            "covers": covers,
            "signs": SignAggregateGenerator(high.id, road, db)._get_raw_data(),
            "light": LightAggregateGenerator(high.id, road, db)._get_raw_data()[
                "length"
            ],
            "barriers": BarriersAggregateGenerator(high.id, road, db)._get_raw_data()[
                "length"
            ],
            "tubes": TubesAggregateGenerator(high.id, road, db)._get_raw_data(),
            "cross": CrossAggregateGenerator(high.id, road, db)._get_raw_data(),
        }

        if with_image:
            axe = road.get_main_axe_coordinates(s)
            points = [(i["lat"], i["lng"]) for i in axe]
            lng = mean(i["lng"] for i in axe)
            lat = mean(i["lat"] for i in axe)
            map = folium.Map(
                location=(lat, lng)
                # location=(mean(i['lng'] for i in axe), mean(i['lat'] for i in axe)),
            )
            # folium.PolyLine(
            #     points,
            #     color="#FF0000",
            #     weight=25,
            #     opacity=0.5,
            # ).add_to(map)
            map.fit_bounds(points)
            # map.show_in_browser()

            options = Options()
            options.add_argument("--headless=new")
            img_data = map._to_png(driver=webdriver.Chrome(options), delay=2)
            img = Image.open(io.BytesIO(img_data))
            img.save("scheme.png")
            context_from_db["scheme"] = InlineImage(
                doc_template, "scheme.png", width=Mm(173)
            )
            print(TemplateVariablesManager().get_objects())
            context = context_from_db | TemplateVariablesManager().get_objects()
            print(context)
        doc_template.render(context)

        os.makedirs(save_folder, exist_ok=True)
        doc_template.save(os.path.join(save_folder, f"{road.Name}.docx"))
