import logging
from sqlite3 import Error
from app.core.database import get_db_connection
from app.models.models import IPAddressDB
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def select(ip_address: str) -> Optional[IPAddressDB]:
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, ip_address FROM ip_addresses WHERE ip_address = ?",
            (ip_address,)
        )
        row = cursor.fetchone()
        if row:
            return IPAddressDB(id=row[0], ip_address=row[1])
        return None
    except Error as e:
        print(f"Database error in select: {e}")
        return None
    finally:
        conn.close()

def create_ip_address(ip_address: str) -> bool:
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ip_addresses (ip_address) VALUES (?)",
            (ip_address,)
        )
        conn.commit()
        return True
    except Error:
        return False
    finally:
        conn.close()


def get_all_ip_addresses() -> list[IPAddressDB]:
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, ip_address FROM ip_addresses")
        rows = cursor.fetchall()
        return [IPAddressDB(id=row[0], ip_address=row[1]) for row in rows]
    except Error as e:
        logger.error(f"Error fetching IP addresses: {e}")
        return []
    finally:
        if conn:
            conn.close()


def delete_ip_address(ip_address: str) -> bool:
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM ip_addresses WHERE ip_address = ?",
            (ip_address,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        logger.error(f"Error deleting IP address: {e}")
        return False
    finally:
        if conn:
            conn.close()


def import_from_file(file_path: str) -> bool:
    try:
        with open(file_path, 'r') as file:
            ip_addresses = [line.strip() for line in file if line.strip()]

        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ip_addresses")
            for ip in ip_addresses:
                cursor.execute(
                    "INSERT INTO ip_addresses (ip_address) VALUES (?)",
                    (ip,)
                )
            conn.commit()
            return True
        except Error as e:
            logger.error(f"Error importing IPs: {e}")
            return False
        finally:
            if conn:
                conn.close()
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return False


def export_to_file(file_path: str) -> bool:
    try:
        ip_addresses = get_all_ip_addresses()
        with open(file_path, 'w') as file:
            for ip in ip_addresses:
                file.write(f"{ip.ip_address}\n")
        return True
    except Exception as e:
        logger.error(f"Error exporting IPs: {e}")
        return False

def search_ip_addresses(search_term: str) -> list[IPAddressDB]:
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, ip_address FROM ip_addresses WHERE ip_address LIKE ?",
            (f"%{search_term}%",)
        )
        rows = cursor.fetchall()
        return [IPAddressDB(id=row[0], ip_address=row[1]) for row in rows]
    except Error as e:
        logger.error(f"Error searching IP addresses: {e}")
        return []
    finally:
        if conn:
            conn.close()


