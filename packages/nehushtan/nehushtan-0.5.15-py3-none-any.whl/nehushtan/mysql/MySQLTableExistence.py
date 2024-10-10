#  Copyright (c) 2020. Sinri Edogawa

from abc import abstractmethod, ABC

from nehushtan.mysql.MySQLKit import MySQLKit
from nehushtan.mysql.MySQLSelectionMixin import MySQLSelectionTarget


class MySQLTableExistence(MySQLSelectionTarget, ABC):

    def __init__(self):
        """
        Since 0.2.17 Remove `self._mysql_kit`, it is not defined here anymore
        """
        super().__init__()

    @abstractmethod
    def get_mysql_kit(self) -> MySQLKit:
        pass

    @abstractmethod
    def mapping_table_name(self) -> str:
        pass

    @abstractmethod
    def mapping_schema_name(self) -> str:
        pass

    def get_table_expression(self) -> str:
        e = ''
        if self.mapping_schema_name() != '':
            e += f'`{self.mapping_schema_name()}`.'
        e += f'`{self.mapping_table_name()}`'
        return e

    def as_selection_target(self) -> str:
        """
        Since 0.5.8
        """
        return self.get_table_expression()
