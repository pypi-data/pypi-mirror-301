"""各类建议工具"""

import logging
from typing import List, Dict, Any, Tuple
from vxutils.datamodel import VXDataModel
from vxutils.datamodel.dborm import VXDBSession, VXDataBase
from configparser import ConfigParser


class _config_option(VXDataModel):
    """配置项"""

    section: str
    option: str
    value: str


class VXDBConfigParser(ConfigParser):
    """数据库配置"""

    def read(self, db: VXDataBase, table_name: str = "settings") -> None:  # type: ignore[explicit-override, override]
        """读取配置"""

        with db.start_session() as session:
            try:
                items = session.find(table_name)
                for item in items:
                    if item["section"] not in self.sections():
                        self.add_section(item["section"])
                    self.set(item["section"], item["option"], item["value"])
            except Exception as e:
                logging.error("Read Config Failed. %s", e)
                return

    def write(self, db: VXDataBase, table_name: str = "settings") -> None:  # type: ignore[explicit-override, override]
        """写入配置"""
        db.create_table(
            table_name, ["section", "option"], _config_option, if_exists="replace"
        )
        with db.start_session() as session:
            for section in self.sections():
                for option in self.options(section):
                    session.save(
                        table_name,
                        _config_option(
                            section=section,
                            option=option,
                            value=self.get(section, option),
                        ),
                    )
