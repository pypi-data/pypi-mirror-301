from typing import Iterable


class MySQLJoinOnCondition:
    def __init__(self, left_field_expression: str, right_field_expression: str):
        self.__left_field_expression = left_field_expression
        self.__right_field_expression = right_field_expression

    def __str__(self):
        return self.organize_to_sql()

    def organize_to_sql(self):
        return self.__left_field_expression + " = " + self.__right_field_expression

    @staticmethod
    def make_field_equal(left: Iterable[str], right: Iterable[str]):
        """
        Provide `left` and `right` each as
            1) a string for table name (alias);
        or  2) a tuple of two strings, for schema and table names (aliases).
        """
        left_field_expression = '`' + '`.`'.join(left) + '`'
        right_field_expression = '`' + '`.`'.join(right) + '`'

        return MySQLJoinOnCondition(
            left_field_expression=left_field_expression,
            right_field_expression=right_field_expression,
        )