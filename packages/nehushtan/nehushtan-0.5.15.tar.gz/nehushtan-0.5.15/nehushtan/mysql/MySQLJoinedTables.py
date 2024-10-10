from typing import Optional, Union, List

from nehushtan.mysql.MySQLJoinOnCondition import MySQLJoinOnCondition
from nehushtan.mysql.MySQLKit import MySQLKit
from nehushtan.mysql.MySQLSelectionMixin import MySQLSelectionTarget, MySQLSelectionMixin
from nehushtan.mysql.MySQLTableExistence import MySQLTableExistence
from nehushtan.mysql.MySQLTableSelection import MySQLTableSelection


class MySQLJoinedTables(MySQLSelectionTarget):
    def __init__(self):
        super().__init__()
        self.__join_target_list = []
        self.__db: Optional[MySQLKit] = None

    def add_join_target(self,
                        join_type: str,
                        target: Union[MySQLSelectionMixin, MySQLTableExistence],
                        alias: Optional[str] = None,
                        on_conditions: Optional[List[MySQLJoinOnCondition]] = None,
                        index_hint: Optional[str] = None,
                        ):
        db = target.get_mysql_kit()
        if db is not None:
            self.__db = db

        x = join_type + " "
        if isinstance(target, MySQLTableExistence):
            x += target.get_table_expression()
        elif isinstance(target, MySQLSelectionMixin):
            x += target.generate_sql()
        else:
            raise TypeError(
                'target for nehushtan.mysql.MySQLJoinSelection.MySQLJoinSelection.add_join_target should not be this')

        if alias is not None:
            x += ' as `' + alias + '`'

        if index_hint is not None:
            x += ' ' + index_hint

        if on_conditions is not None and len(on_conditions) > 0:
            a = []
            for condition in on_conditions:
                a.append(condition.organize_to_sql())
            x += ' on ' + ' and '.join(a)

        self.__join_target_list.append(x)
        return self

    def based_on(self,
                 target: Union[MySQLSelectionMixin, MySQLTableExistence],
                 alias: Optional[str] = None,
                 index_hint: Optional[str] = None,
                 ):
        return self.add_join_target(join_type='',
                                    target=target, alias=alias,
                                    on_conditions=None,
                                    index_hint=index_hint)

    def left_join(self,
                  target: Union[MySQLSelectionMixin, MySQLTableExistence],
                  alias: Optional[str] = None,
                  index_hint: Optional[str] = None,
                  on_conditions: Optional[List[MySQLJoinOnCondition]] = None,
                  ):
        return self.add_join_target(join_type='LEFT JOIN',
                                    target=target, alias=alias,
                                    on_conditions=on_conditions,
                                    index_hint=index_hint)

    def inner_join(self,
                   target: Union[MySQLSelectionMixin, MySQLTableExistence],
                   alias: Optional[str] = None,
                   index_hint: Optional[str] = None,
                   on_conditions: Optional[List[MySQLJoinOnCondition]] = None,
                   ):
        return self.add_join_target(join_type='INNER JOIN',
                                    target=target, alias=alias,
                                    on_conditions=on_conditions,
                                    index_hint=index_hint)

    def get_mysql_kit(self) -> MySQLKit:
        return self.__db

    def as_selection_target(self) -> str:
        return ' '.join(self.__join_target_list)

    def select_in_joined_tables(self):
        return MySQLTableSelection(target=self, )