import sqlite3

def ensure_schema(connection):
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Incomes ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "empl REAL, "
        "savings REAL, "
        "bonus REAL"
        ")"
    )
    cursor.execute("PRAGMA table_info(Incomes)")
    columns = {row[1] for row in cursor.fetchall()}
    if "bonus" not in columns:
        cursor.execute("ALTER TABLE Incomes ADD COLUMN bonus REAL")
    connection.commit()

def addIncomes(user, empl, savings, bonus):
    connection = sqlite3.connect("taxcalculator.db")
    ensure_schema(connection)
    cursor = connection.cursor()
    query = "INSERT INTO Incomes (empl, savings, bonus) VALUES (?, ?, ?)"
    cursor.execute(query, (empl, savings, bonus))
    connection.commit()
    print("Saved")

def retrieveIncomes():
    connection = sqlite3.connect("taxcalculator.db")
    ensure_schema(connection)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Incomes")    
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return rows


if __name__ == "__main__":
    addIncomes(1, 30000, 1250, 2000)
    retrieveIncomes()