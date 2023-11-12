import sqlite3


def init_db():
    conn = sqlite3.connect("../microservicios.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customer_data (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE, 
            reg_date DATETIME
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS services_data (
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name,
            description TEXT,
            price INTEGER
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reservation_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            service_id INTEGER,
            payment_status BOOL,
            date DATE,
            FOREIGN KEY(customer_id) REFERENCES customer_data(customer_id),
            FOREIGN KEY(service_id) REFERENCES services_data(service_id)
        );
        """
    )

    conn.commit()
    conn.close()
