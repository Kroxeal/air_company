import asyncpg


class Database:
    def __init__(self, user, password, database, host, port):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self.connection = None

    async def connect(self):
        """
            Establish a connection to the database.

            Raises:
                Exception: Raises an exception if the connection is already established.
        """
        self.connection = await asyncpg.connect(
            user=self.user,
            password=self.password,
            database=self.database,
            host=self.host,
            port=self.port,
        )

    async def disconnect(self):
        """
            Close the connection to the database.
        """
        await self.connection.close()

    async def execute(self, query, *args):
        """
            Execute an SQL query and return the result.

            Args:
                query (str): SQL query.
                *args: Query parameters.

            Returns:
                The result of executing the query.

            Raises:
                Exception: Raises an exception if the connection is not established.
        """
        if not self.connection:
            raise Exception("Connection is not established. Call connect() first.")
        return await self.connection.execute(query, *args)

    async def fetchrow(self, query, *args):
        """
            Execute an SQL query and return the first row of the result.

            Args:
                query (str): SQL query.
                *args: Query parameters.

            Returns:
                The first row of the query result.

            Raises:
                Exception: Raises an exception if the connection is not established.
        """
        if not self.connection:
            raise Exception("Connection is not established. Call connect() first.")

        result = await self.connection.fetchrow(query, *args)
        return result

    async def execute_in_transaction(self, *queries):
        """
            Execute multiple SQL queries within a single transaction.

            Args:
                *queries: List of SQL queries.

            Raises:
                Exception: Raises an exception if the connection is not established.
        """
        if not self.connection:
            raise Exception("Connection is not established. Call connect() first.")
        async with self.connection.transaction():
            for query in queries:
                await self.connection.execute(query)

    async def fetchall(self, query, *args):
        """
            Execute an SQL query and return all rows of the result.

            Args:
                query (str): SQL query.
                *args: Query parameters.

            Returns:
                List of all rows from the query result.

            Raises:
                Exception: Raises an exception if the connection is not established.
        """
        if not self.connection:
            raise Exception("Connection is not established. Call connect() first.")
        result = await self.connection.fetch(query, *args)
        return result

    async def fetchval(self, query, *args):
        """
            Execute an SQL query and return a single value from the result.

            Args:
                query (str): SQL query.
                *args: Query parameters.

            Returns:
                A single value from the query result.

            Raises:
                Exception: Raises an exception if the connection is not established.
        """
        if not self.connection:
            raise Exception("Connection is not established. Call connect() first.")
        result = await self.connection.fetchval(query, *args)
        return result