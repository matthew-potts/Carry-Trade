from pathlib import Path
import sqlite3

def main():
    base_dir = Path(__file__).parent.absolute()
    con = sqlite3.connect(f"{base_dir}/carry_trade.db")
    cur = con.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS price 
                (class, item, open, close, high, low, volume, timestamp,
                PRIMARY KEY (class, item, timestamp))
                """)

if __name__ == "__main__":
    main()
