import json
import sqlite3
import decimal


class ConfigManager:
    """
    A class for managing configuration settings in a SQLite database.

    Args:
        db_file (str, optional): The filename of the SQLite database. Defaults to "config.db".

    Attributes:
        conn (sqlite3.Connection): A connection to the SQLite database.
        cursor (sqlite3.Cursor): A cursor for executing SQL statements.
    """

    def __init__(self, db_file="config.db"):
        """
        Initialize a new ConfigManager instance.
        """
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Create the "config" table in the database if it doesn't exist.
        """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT,
                data_type TEXT NOT NULL
            )
        """
        )
        self.conn.commit()

    def set(self, key, value):
        """
        Set the value of a configuration setting.

        Args:
            key (str): The key of the configuration setting.
            value (object): The value of the configuration setting.
        """
        data_type = self._get_data_type(value)
        if data_type == "json":
            value = json.dumps(value)
        self.cursor.execute(
            "INSERT OR REPLACE INTO config (key, value, data_type) VALUES (?, ?, ?)",
            (key, str(value), data_type),
        )
        self.conn.commit()

    def get(self, key, default=None):
        """
        Get the value of a configuration setting.

        Args:
            key (str): The key of the configuration setting.
            default (object, optional): The default value to return if the setting is not found.

        Returns:
            object: The value of the configuration setting, or the default value if not found.
        """
        self.cursor.execute("SELECT value, data_type FROM config WHERE key = ?", (key,))
        result = self.cursor.fetchone()
        if result:
            value, data_type = result
            if data_type == "json":
                value = json.loads(value)
            return self._convert_value(value, data_type)
        else:
            return default

    def delete(self, key):
        """
        Delete a configuration setting.

        Args:
            key (str): The key of the configuration setting.
        """
        self.cursor.execute("DELETE FROM config WHERE key = ?", (key,))
        self.conn.commit()

    def _get_data_type(self, value):
        """
        Get the data type of a value.

        Args:
            value (object): The value to get the data type of.

        Returns:
            str: The data type of the value.
        """
        if isinstance(value, bool):
            return "bool"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, str):
            return "str"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, decimal.Decimal):
            return "decimal"
        elif isinstance(value, dict) or isinstance(value, list):
            return "json"
        else:
            raise TypeError("Unsupported data type")

    def _convert_value(self, value, data_type):
        """
        Convert a value to its corresponding data type.

        Args:
            value (str): The value to convert.
            data_type (str): The data type of the value.

        Returns:
            object: The converted value.
        """
        if data_type == "bool":
            return True if value == "True" else False
        elif data_type == "int":
            return int(value)
        elif data_type == "str":
            return str(value)
        elif data_type == "float":
            return float(value)
        elif data_type == "decimal":
            return decimal.Decimal(value)
        elif data_type == "json":
            return value
        else:
            raise TypeError("Unsupported data type")

    def close(self):
        """
        Close the connection to the SQLite database.
        """
        self.conn.close()

    @staticmethod
    def test(debug=False):
        """
        Test the ConfigManager class.

        Args:
            debug (bool, optional): Whether to print debug information. Defaults to False.
        """
        config = ConfigManager()
        cases = {
            "enabled": True,
            "max_items": 10,
            "api_key": "your_api_key",
            "version": 1.23,
            "price": decimal.Decimal("19.99"),
            "login_count": 0,
            "level": -3,
            "auto_update": False,
            "stats": [3, 6, 9],
            "data": {"key1": "value1", "key2": [1, 2, 3]},
        }
        for key, value in cases.items():
            config.set(key, value)
            saved = config.get(key)
            if debug:
                print(value)
                print(saved)
                print('---------------------------------------------')
            assert saved == value
            config.delete(key)
            assert config.get(key) is None
            assert config.get(key, default=value) == value
        config.close()


if __name__ == "__main__":
    ConfigManager.test(debug=True)
