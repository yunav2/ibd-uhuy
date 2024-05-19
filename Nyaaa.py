import mysql.connector
from datetime import datetime

# Definisikan konstanta-konstanta
DATABASE_USERNAME = 'root'
DATABASE_PASSWORD = ''
DATABASE_HOST = '%'
DATABASE_NAME = 'testing'
DATABASE_PORT = '3306'

PASLON_OPTIONS = [
    "Anie Baswedan & Cak imin",
    "Prabowo & Gibran",
    "Ganjar Pranowo & Mahfud M.D"
]

# Buat koneksi ke database
cnx = mysql.connector.connect(
    user=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    database=DATABASE_NAME
)

# Buat kursor untuk eksekusi kueri
cursor = cnx.cursor()

# Buat tabel voter (pastikan kolom 'name' ada)
cursor.execute("""
CREATE TABLE IF NOT EXISTS voter (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    dob DATE NOT NULL,
    gender ENUM('M', 'F') NOT NULL,
    voter_id INT NOT NULL UNIQUE,
    choosen VARCHAR(50) NOT NULL,
    voting_time DATETIME NOT NULL
)
""")

# Komit perubahan
cnx.commit()

# Fungsi validasi nama
def is_valid_name(name):
    return name.isalpha() and len(name) >= 4  # Mengembalikan True jika hanya karakter alfabet dan panjangnya minimal 4 karakter

# Fungsi validasi ID
def is_valid_id(voter_id):
    return voter_id.isdigit() and len(voter_id) == 5  # Mengembalikan True jika hanya angka dan panjangnya tepat 5 karakter

# Mulai proses pemilihan
while True:
    name = input("Masukkan nama anda : ")
    if not is_valid_name(name):
        print("Nama hanya boleh terdiri dari karakter alfabet dan minimal 4 karakter.")
        continue

    dob = input("Masukkan tanggal lahir anda (format: yyyy-mm-dd) : ")
    gender = input("Masukkan jenis kelamin anda (M/F) : ")

    if not all([dob, gender]):
        print("Mohon isi semua field dengan benar.")
        continue

    try:
        dob = datetime.strptime(dob, "%Y-%m-%d").date()
    except ValueError:
        print("Format tanggal lahir tidak valid.")
        continue

    if gender not in ['M', 'F']:
        print("Jenis kelamin hanya boleh M atau F.")
        continue

    voter_id = input("Masukkan ID anda (harus terdiri dari 5 angka) : ")
    while not is_valid_id(voter_id):
        print("ID hanya boleh terdiri dari 5 angka.")
        voter_id = input("Masukkan ID anda (harus terdiri dari 5 angka) : ")

    print("Kamu adalah pemilih ")
    print("Untuk Memilih Paslon:")
    for i, paslon in enumerate(PASLON_OPTIONS, start=1):
        print(f"Tekan {i} untuk {paslon}")
    vote = int(input("Kamu Milih Paslon Berapa? : "))
    if 1 <= vote <= len(PASLON_OPTIONS):
        choosen = PASLON_OPTIONS[vote - 1]
        print("Terima kasih telah memilih!")
        # Masukkan data pemilih ke dalam tabel voter
        cursor.execute("INSERT INTO voter (name, dob, gender, voter_id, choosen, voting_time) VALUES (%s, %s, %s, %s, %s, NOW())", (name, dob, gender, voter_id, choosen))
        cnx.commit()
    else:
        print("Mohon pilih angka yang tersedia.")

    pilihan = input("Apakah Anda ingin melanjutkan memilih lagi, menghitung hasil, atau keluar dari program? (pilih 'y' untuk lanjut, 'h' untuk hitung, atau 'k' untuk keluar): ")
    if pilihan.lower() == 'k':
        break
    elif pilihan.lower() == 'h':
        # Buat koneksi baru untuk menghitung suara
        cnx = mysql.connector.connect(
            user=DATABASE_USERNAME,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            database=DATABASE_NAME
        )

        # Buat kursor untuk eksekusi kueri
        cursor = cnx.cursor()

        # Hitung suara untuk setiap kandidat
        cursor.execute("SELECT choosen, COUNT(choosen) AS votes FROM voter GROUP BY choosen")
        results = cursor.fetchall()

        for result in results:
            print(f"{result[0]} mendapatkan {result[1]} suara.")

        # Tentukan pemenangnya
        if results:
            winner = max(results, key=lambda x: x[1])
            print(f"{winner[0]} menang dengan {winner[1]} suara.")
        else:
            print("Tidak ada suara yang masuk.")

        # Tutup kursor dan koneksi
        cursor.close()
        cnx.close()
        break  # Keluar dari loop while utama

# Tutup kursor dan koneksi
cursor.close()
cnx.close()
