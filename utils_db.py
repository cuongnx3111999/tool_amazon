import mysql.connector
from mysql.connector import Error
from typing import Optional, Dict, Tuple
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Hàm kết nối đến MySQLpip install mysql-connector-python
def create_connection():
  connection = None
  try:
      connection = mysql.connector.connect(
          host='MYSQL_HOST',
          database='MYSQL_DATABASE',
          user='MYSQL_USER',
          password='MYSQL_PASSWORD'
      )
      if connection.is_connected():
          logging.info("Kết nối MySQL thành công")
  except Error as e:
      logging.error(f"Lỗi khi kết nối MySQL: {e}")
  return connection

# Hàm lưu dữ liệu vào MySQL
def save_to_mysql(connection, msx_product: str, invoice: Dict[str, int]):
  try:
      cursor = connection.cursor()
      query = """INSERT INTO product_invoices 
                 (msx_product, items, shipping, total_before_tax, estimated_tax, order_total) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
      values = (msx_product,
                invoice.get('items', 0),
                invoice.get('shipping', 0),
                invoice.get('total_before_tax', 0),
                invoice.get('estimated_tax', 0),
                invoice.get('order_total', 0))
      cursor.execute(query, values)
      connection.commit()
      logging.info(f"Dữ liệu cho sản phẩm {msx_product} đã được lưu vào MySQL")
  except Error as e:
      logging.error(f"Lỗi khi lưu vào MySQL: {e}")

