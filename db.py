import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="[Your_Password]",
  database="kasir"
)

cursor = db.cursor()
sql = """CREATE TABLE produk (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nama_barang VARCHAR(255),
  harga Int(255)
)
"""
cursor.execute(sql)

print("Tabel customers berhasil dibuat!")
