class SchemaHelper:
    """
    A helper class for constructing schema URLs and retrieving schema version.

    Attributes:
        __schema_version__ (str): The version of the schema.
        __build_version__ (str): The build version.
        __Host__ (str): The host URL for the schema.

    Methods:
        construct_schema_url(path: str) -> str: Constructs a schema URL based on the provided path.
        get_schema_version() -> str: Retrieves the schema version.

    """

    __schema_version__ = "0.4.1"
    __build_version__ = "0.4.1-rc.4+b.37.sha.0ef25aa9"
    __Host__ = "https://bladednextgen.dnv.com"

    @staticmethod
    def construct_schema_url(path: str) -> str:
        """
        Constructs a schema URL based on the provided path.

        Args:
            path (str): The path to the schema.

        Returns:
            str: The constructed schema URL.

        """
        url = f"{SchemaHelper.__Host__}/schema/{SchemaHelper.__schema_version__}/{path}"
        return url
    
    @staticmethod
    def get_schema_version() -> str:
        """
        Retrieves the schema version.

        Returns:
            str: The schema version.

        """
        return SchemaHelper.__schema_version__