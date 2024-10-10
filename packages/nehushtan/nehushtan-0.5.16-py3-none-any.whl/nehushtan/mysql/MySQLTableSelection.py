#  Copyright (c) 2020. Sinri Edogawa
from typing import Iterable, Optional, Union, List

from nehushtan.mysql.MySQLCondition import MySQLCondition
from nehushtan.mysql.MySQLKit import MySQLKit
from nehushtan.mysql.MySQLSelectionMixin import MySQLSelectionMixin, MySQLSelectionTarget
from nehushtan.mysql.MySQLTableExistence import MySQLTableExistence





class MySQLTableSelection(MySQLSelectionMixin):
    """
    As of version 0.3.6, move some features to MySQLSelectionMixin
    """

    def __init__(self,
                 target: MySQLSelectionTarget,
                 # model: MySQLTableExistence, alias: Optional[str] = None,
                 ):
        super().__init__()
        # self._model = model
        # self._alias = alias
        self._target = target
        self._select_fields = []
        # self._join_metas = []
        self._conditions = []
        self._group_by_fields = []
        self._sort_expression = ''
        self._limit = 0
        self._offset = 0
        self._use_indices = []
        self._force_indices = []
        self._ignore_indices = []
        self._for_update = False

    def get_mysql_kit(self) -> MySQLKit:
        return self._target.get_mysql_kit()

    def get_limit(self) -> int:
        return self._limit

    def set_limit(self, limit: int):
        self._limit = limit
        return self

    def get_offset(self) -> int:
        return self._offset

    def set_offset(self, offset: int):
        self._offset = offset
        return self

    def get_sort_expression(self):
        return self._sort_expression

    def set_sort_expression(self, sort_expression: str):
        self._sort_expression = sort_expression
        return self

    def add_select_field(self, field_expression: str, alias: str = ''):
        s = field_expression
        if len(alias) > 0:
            s += f' as {alias}'
        self._select_fields.append(s)
        return self

    def add_select_field_name_list(self, field_name_array: Iterable[str]):
        """

        :param field_name_array: ["F1","F2", ...] or ("F1","F2", ...)
        :return:
        """
        for item in field_name_array:
            self._select_fields.append(item)
        return self

    # def add_left_join_table(self, table_name: str, schema_name: Optional[str] = None,
    #                         alias: Optional[str] = None,
    #                         on_conditions: Optional[Iterable[MySQLJoinOnCondition]] = None, ):
    #     return self._add_join_table(join_type="LEFT JOIN", table_name=table_name, schema_name=schema_name, alias=alias,
    #                                 on_conditions=on_conditions)
    #
    # def add_inner_join_table(self, table_name: str, schema_name: Optional[str] = None,
    #                          alias: Optional[str] = None,
    #                          on_conditions: Optional[Iterable[MySQLJoinOnCondition]] = None, ):
    #     return self._add_join_table(join_type="INNER JOIN", table_name=table_name, schema_name=schema_name, alias=alias,
    #                                 on_conditions=on_conditions)

    # def _add_join_table(self, join_type: str, table_name: str, schema_name: Optional[str] = None,
    #                     alias: Optional[str] = None, on_conditions: Optional[Iterable[MySQLJoinOnCondition]] = None, ):
    #     e = f'`{table_name}`'
    #     if schema_name is not None:
    #         e = f'`{schema_name}`.{e}'
    #     if alias is not None:
    #         e = f'{e} as `{alias}`'
    #     c = ''
    #     if on_conditions is not None:
    #         c_array = []
    #         for condition in on_conditions:
    #             c_array.append(f'({condition.organize_to_sql()})')
    #         c_c = ' AND '.join(c_array)
    #         c = f' ON {c_c}'
    #
    #     j = f'{join_type} {e}{c}'
    #
    #     self._join_metas.append(j)
    #     return self

    # def add_left_join_sub_query(self, selection: MySQLSelectionMixin, alias: str,
    #                             on_conditions: Optional[Iterable[MySQLJoinOnCondition]] = None, ):
    #     return self._add_join_sub_query("LEFT JOIN", selection=selection, alias=alias, on_conditions=on_conditions)
    #
    # def add_inner_join_sub_query(self, selection: MySQLSelectionMixin, alias: str,
    #                              on_conditions: Optional[Iterable[MySQLJoinOnCondition]] = None, ):
    #     return self._add_join_sub_query("INNER JOIN", selection=selection, alias=alias, on_conditions=on_conditions)
    #
    # def _add_join_sub_query(self, join_type: str, selection: MySQLSelectionMixin, alias: str,
    #                         on_conditions: Optional[Iterable[MySQLJoinOnCondition]] = None, ):
    #     c = ''
    #     if on_conditions is not None:
    #         c_array = []
    #         for condition in on_conditions:
    #             c_array.append(f'({condition.organize_to_sql()})')
    #         c_c = ' AND '.join(c_array)
    #         c = f' ON {c_c}'
    #     j = f'{join_type} ({selection.generate_sql()}) as `{alias}`{c}'
    #     self._join_metas.append(j)
    #     return self

    def add_condition(self, condition: MySQLCondition):
        self._conditions.append(condition)
        return self

    def add_conditions(self, conditions: Iterable[MySQLCondition]):
        """

        :param conditions: array of MySQLCondition
        :return:
        """
        for condition in conditions:
            if isinstance(condition, MySQLCondition):
                self._conditions.append(condition)
            # else just ignore
        return self

    def add_simple_conditions(self, equal_dict: dict):
        """

        :param equal_dict: {FIELD:VALUE,FIELD:VALUE_ARRAY}
        :return:
        """
        for k, v in equal_dict.items():
            if isinstance(v, (tuple, list)):
                self.add_condition(MySQLCondition.make_in_array(k, v))
            else:
                self.add_condition(MySQLCondition.make_equal(k, v))
        return self

    def set_group_by_fields(self, group_by_fields: list):
        self._group_by_fields = group_by_fields
        return self

    def use_index(self, index: str):
        self._use_indices.append(index)
        return self

    def force_index(self, index: str):
        self._force_indices.append(index)
        return self

    def ignore_index(self, index: str):
        self._ignore_indices.append(index)
        return self

    def set_for_update(self, value: bool):
        self._for_update = value

    def generate_sql(self) -> str:
        # table = self._model.get_table_expression()
        #
        # if self._alias is not None:
        #     table += f' AS `{self._alias}` '

        target = self._target.as_selection_target()

        fields = "*"
        if len(self._select_fields) > 0:
            fields = ",".join(self._select_fields)

        condition_sql = MySQLCondition.build_sql_component(self._conditions)

        if isinstance(self._target, MySQLTableExistence):
            indices = ''
            if len(self._use_indices) > 0:
                indices += " USE INDEX (" + ",".join(self._use_indices) + ") "
            if len(self._force_indices) > 0:
                indices += " FORCE INDEX (" + ",".join(self._force_indices) + ") "
            if len(self._ignore_indices) > 0:
                indices += " IGNORE INDEX (" + ",".join(self._force_indices) + ") "
            target += indices

        # joins = ' '.join(self._join_metas)

        # sql = f"SELECT {fields} FROM {table} {indices} {joins} WHERE {condition_sql} "

        sql = f"SELECT {fields} FROM {target} WHERE {condition_sql} "

        if len(self._group_by_fields) > 0:
            sql += "GROUP BY " + ",".join(self._group_by_fields) + " "

        if self._sort_expression.strip() != '':
            sql += "ORDER BY " + self._sort_expression + " "

        if self._limit > 0:
            sql += f"LIMIT {self._limit} "
            if self._offset > 0:
                sql += f"OFFSET {self._offset} "

        if self._for_update:
            sql += " FOR UPDATE "

        return sql
