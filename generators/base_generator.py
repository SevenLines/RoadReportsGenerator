import io
import os
from statistics import mean

from PIL import Image
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chromium.webdriver import ChromiumDriver

from db import RoadsDB
from models import Road, High, Way
import folium


class BaseGenerator(object):
    template = ""
    tables_generators = {}

    def generate(self, road_id, save_folder="output", with_image=False):
        doc_template = DocxTemplate(os.path.join("templates", self.template))
        doc = doc_template.get_docx()

        tables_to_fill = []

        db = RoadsDB()
        with db.session() as s:
            road = s.query(Road).filter(Road.id == road_id).first()
            road_length = road.get_length(s)[1]
            high = s.query(High).join(Way, Way.id == High.way_id) \
                .filter(Way.road_id == road.id).first()

        for table in doc.tables:
            key = table.rows[0].cells[0].text[1:-1].strip()
            generator_class = self.tables_generators.get(key)
            if generator_class:
                tables_to_fill.append({
                    'table': table,
                    'generator': generator_class,
                })

        for table_info in tables_to_fill:
            table_info['generator'](high.id, db).fill(table_info['table'], doc)

        context = {
            'road_title': road.Name,
            'road_length': road_length,
        }

        if with_image:
            axe = road.get_main_axe_coordinates(s)

            points = [(i['lat'], i['lng']) for i in axe]
            map = folium.Map(
                location=(mean(i['lat'] for i in axe), mean(i['lng'] for i in axe)),
            )
            folium.PolyLine(
                points,
                color="#FF0000",
                weight=25,
                opacity=0.5,
            ).add_to(map)
            map.fit_bounds(points)
            map.show_in_browser()

            # options = Options()
            # options.add_argument('--headless=new')
            # img_data = map._to_png(driver=webdriver.Chrome(options), delay=1)
            # img = Image.open(io.BytesIO(img_data))
            # img.save('scheme.png')
            # context['scheme'] = InlineImage(doc_template, "scheme.png", width=Mm(173))

        doc_template.render(context)

        os.makedirs(save_folder, exist_ok=True)
        doc_template.save(os.path.join(save_folder, f"{road.Name}.docx"))
