from src.db.settings import database


async def create_tables():

    await database.connect()

    await database.execute("""
    CREATE TABLE IF NOT EXISTS Aircrafts (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(100) NOT NULL,
        model VARCHAR(255) NOT NULL,
        year_manufacture INT,
        seating_capacity INT,
        max_range INT,
        engine_type VARCHAR(35),
        status VARCHAR(35),
        last_service DATE,
        manufacture VARCHAR(100)
    )
    """)

    await database.execute("""
    CREATE TABLE IF NOT EXISTS Flights (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        flight_number VARCHAR(30),
        departure_datetime TIMESTAMP NOT NULL,
        arrival_datetime TIMESTAMP NOT NULL,
        departure_airport VARCHAR(100) NOT NULL,
        arrival_airport VARCHAR(100) NOT NULL,
        available_seats INT,
        ticket_price NUMERIC(10, 2),
        aircraft_id UUID NOT NULL REFERENCES Aircrafts(id) ON DELETE CASCADE
    )
    """)

    await database.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        username VARCHAR(100) NOT NULL,
        name VARCHAR(100),
        surname VARCHAR(100),
        phone_number VARCHAR(20),
        email VARCHAR(255),
        password VARCHAR(255) NOT NULL,
        role VARCHAR(30) CHECK (new_column_name IN ('user', 'admin', 'employee'))
    )
    """)

    await database.execute("""
        CREATE TABLE IF NOT EXISTS Passports (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            passport_number VARCHAR(20) NOT NULL,
            nationality VARCHAR(20) NOT NULL,
            sex VARCHAR(7) NOT NULL,
            address VARCHAR(100) NOT NULL,
            date_of_birth DATE NOT NULL,
            date_of_issue DATE NOT NULL,
            date_of_expire DATE NOT NULL,
            photo varchar(150),
            user_id UUID NOT NULL REFERENCES Users(id) ON DELETE CASCADE
        )
        """)

    await database.execute("""
    CREATE TABLE IF NOT EXISTS Tickets (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        flight_id UUID NOT NULL REFERENCES Flights(id) ON DELETE CASCADE,
        user_id UUID NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
        service_class VARCHAR(20) NOT NULL,
        price NUMERIC(10, 2) NOT NULL,
        status VARCHAR(20) NOT NULL,
        booking_date TIMESTAMP NOT NULL
    )
    """)

    await database.execute("""
        CREATE TABLE IF NOT EXISTS Departments (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR(100) NOT NULL,
            description VARCHAR(150) NOT NULL
        )
        """)

    await database.execute("""
    CREATE TABLE IF NOT EXISTS Employees (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        position VARCHAR(100) NOT NULL,
        salary NUMERIC(10, 2) NOT NULL,
        status VARCHAR(20) NOT NULL,
        department_id UUID NOT NULL REFERENCES Departments(id) ON DELETE CASCADE,
        user_id UUID NOT NULL REFERENCES Users(id) ON DELETE CASCADE
    )
    """)

    await database.disconnect()


if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tables())
