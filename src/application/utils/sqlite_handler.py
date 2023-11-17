import sqlite3
from typing import Any, Dict


class SQLiteHandler:

    @staticmethod
    def create_table(
            db_name: str,
            table_name: str
    ):
        """
        Create the table for the events project
        :param db_name: the db where the tables at
        :param table_name: the tables name
        :return:
        """
        conn = sqlite3.connect(db_name)
        curs = conn.cursor()
        curs.execute(
                    f"""
                                CREATE TABLE "{table_name}" (
            event_id               TEXT    PRIMARY KEY
                                           NOT NULL,
            event_time             TEXT    NOT NULL,
            title                  TEXT    NOT NULL,
            location               TEXT    NOT NULL,
            venue                  TEXT    NOT NULL,
            number_of_participants INTEGER NOT NULL,
            creation_time          TEXT    NOT NULL,
            modify_time            TEXT    NOT NULL
        );
        ;"""
        )
        conn.commit()
        conn.close()

    @staticmethod
    def check_if_table_exists(
            db_name: str,
            table_name: str,
    ):
        """
        Check if the table is in the db
        :param db_name: the db where the tables at
        :param table_name: the tables name
        :return:
        """
        conn = sqlite3.connect(db_name)
        curs = conn.cursor()
        curs.execute(
            f"""
                    SELECT name FROM sqlite_master 
                WHERE type='table' and name = '{table_name}';"""
        )
        res = curs.fetchall()
        conn.close()
        return res != []

    @staticmethod
    def read_all_table(db_name: str, table_name: str):
        """
        Read the entire data from the table
        :param db_name: the db where the tables at
        :param table_name: the tables name
        :return:
        """
        conn = sqlite3.connect(db_name)
        curs = conn.cursor()
        curs.execute(
                f""" SELECT * FROM {table_name}; """
            )
        res = curs.fetchall()
        conn.close()
        return res

    @staticmethod
    def read_with_conditions(
        db_name: str,
        table_name: str,
        filter_key: str,
        searched_value: str | int,
    ):
        """
        Read data from the table that stands in the conditions
        :param db_name: the db where the tables at
        :param table_name: the tables name
        :param filter_key: the key that the filter is on
        :param searched_value: the searched value
        :return: the rows that are stands in the condition
        """
        conn = sqlite3.connect(db_name)
        curs = conn.cursor()
        curs.execute(
                f"""
                SELECT * FROM {table_name}
                WHERE {filter_key} = "{searched_value}";
                """
            )
        res = curs.fetchall()
        conn.close()
        return res

    @staticmethod
    def insert(db_name: str, table_name: str, item: Dict[str, Any]):
        """
        insert the item to the db
        :param db_name: the db where the tables at
        :param table_name: the tables name
        :param item: the item to insert {column_name: value}
        :return:
        """
        converted_item = SQLiteHandler.convert_dict_to_query_strings(item)
        conn = sqlite3.connect(db_name)
        curs = conn.cursor()
        curs.execute(
                f"""
                INSERT INTO {table_name}({converted_item["columns"]})
                VALUES({converted_item["values"]});
                """, item
            )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(db_name: str, table_name: str, id_column: str, obj_id: str):
        """
        delete an object from the table
        :param db_name: the db where the tables at
        :param table_name: the tables name
        :param id_column: the id column name
        :param obj_id: the id of the object to delete
        :return:
        """
        conn = sqlite3.connect(db_name)
        curs = conn.cursor()
        curs.execute(
                f"""
                DELETE FROM {table_name}
                WHERE {id_column} = "{obj_id}";
                """
            )
        conn.commit()
        conn.close()

    @staticmethod
    def update(
        db_name: str,
        table_name: str,
        id_column: str,
        obj_id: str,
        new_item: dict,
    ):
        """
        delete an object from the table
        :param db_name: the db where the tables at
        :param table_name: the tables name
        :param id_column: the id column name
        :param obj_id: the id of the object to delete
        :param new_item: the fields to update
        :return:
        """
        update_str = ""
        for column in new_item.keys():
            update_str += f"{column} = :{column},"
        conn = sqlite3.connect(db_name)
        curs = conn.cursor()
        curs.execute(
                f"""
                UPDATE {table_name}
                SET {update_str[:-1]}
                WHERE {id_column} = "{obj_id}";
                """, new_item
            )
        conn.commit()
        conn.close()

    @staticmethod
    def convert_dict_to_query_strings(dictionary: Dict[str, str | int]):
        """
        Gets dictionary and separate it to a string of the columns and
        string of the values
        :param dictionary: the dict to convert
        :return: a converted dict
        {columns: string of columns, values: string of values}
        """
        columns = ""
        values = ""
        for column in dictionary.keys():
            columns += f',{column}'
            values += f', :{column}'
        return {"columns": columns[1:], "values": values[1:]}
