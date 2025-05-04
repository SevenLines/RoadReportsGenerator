from ui.main import main_page
from nicegui import ui
from models import SQLiteBase
from api.db import SQLiteDB

SQLiteBase.metadata.create_all(SQLiteDB().engine)


main_page()
ui.run(native=True, title="Дороги")
