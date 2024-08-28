import time
import os
import re
import sqlite3
import sys

# Koneksi ke database SQLite
conn = sqlite3.connect('learning_center.db')
cursor = conn.cursor()

# Membuat tabel pengguna jika belum ada
cursor.execute('''CREATE TABLE IF NOT EXISTS pengguna (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL)''')

# Membuat tabel anggota jika belum ada
cursor.execute('''CREATE TABLE IF NOT EXISTS anggota (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL UNIQUE,
                    umur INTEGER NOT NULL,
                    semester INTEGER NOT NULL,
                    jurusan TEXT NOT NULL)''')

# Membuat tabel pelajaran jika belum ada
cursor.execute('''CREATE TABLE IF NOT EXISTS pelajaran (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pelajaran TEXT NOT NULL,
                    guru TEXT NOT NULL,
                    UNIQUE (pelajaran, guru))''')

daftar_anggota = []
daftar_pelajaran = []
is_login = False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def tampilkan_splash_screen():
    clear_screen()
    print("=============================================")
    print("==       SELAMAT DATANG DI APLIKASI        ==")
    print("==            LEARNING CENTER              ==")
    print("=============================================")
    time.sleep(2)

def tampilkan_menu_utama():
    clear_screen()
    print("\n======== MENU APLIKASI LEARNING CENTER ========")
    print("1. Daftar Anggota")
    print("2. Daftar Pelajaran")
    print("3. Daftar Nama dan Pelajaran")
    print("4. Logout")
    print("5. Keluar")
    print("===============================================")

def tampilkan_menu_daftar_anggota():
    clear_screen()
    print("\n=== DAFTAR ANGGOTA ===")
    print("1. Tambah Anggota")
    print("2. Tampilkan Daftar Anggota")
    print("3. Edit Daftar Anggota")
    print("4. Kembali ke Menu Utama")

def tampilkan_menu_daftar_pelajaran():
    clear_screen()
    print("\n=== DAFTAR PELAJARAN ===")
    print("1. Tambah Pelajaran")
    print("2. Tampilkan Daftar Pelajaran")
    print("3. Edit Daftar Pelajaran")
    print("4. Kembali ke Menu Utama")

def tambah_anggota():
    while True:
        clear_screen()
        print("\n=== TAMBAH ANGGOTA ===")

        while True:
            nama = input("Masukkan nama anggota: ")
            if not re.match("^[A-Za-z\s]+$", nama):
                print("Nama hanya boleh berisi huruf. Silakan coba lagi.")
                time.sleep(2)
                clear_screen()
                continue

            # Cek apakah nama sudah ada di database
            cursor.execute("SELECT * FROM anggota WHERE nama=?", (nama,))
            if cursor.fetchone():
                print("Nama anggota sudah ada. Silakan coba nama lain.")
                time.sleep(2)
                clear_screen()
                continue
            break

        while True:
            umur = input("Masukkan umur anggota: ")
            if not umur.isdigit():
                print("Umur hanya boleh berisi angka. Silakan coba lagi.")
                time.sleep(2)
                clear_screen()
                continue
            break

        while True:
            semester = input("Masukkan semester anggota: ")
            if not semester.isdigit():
                print("Semester hanya boleh berisi angka. Silakan coba lagi.")
                time.sleep(2)
                clear_screen()
                continue
            break

        while True:
            jurusan = input("Masukkan jurusan anggota: ")
            if not re.match("^[A-Za-z\s]+$", jurusan):
                print("Jurusan hanya boleh berisi huruf. Silakan coba lagi.")
                time.sleep(2)
                clear_screen()
                continue
            break

        # Tambahkan anggota ke database
        cursor.execute("INSERT INTO anggota (nama, umur, semester, jurusan) VALUES (?, ?, ?, ?)",
                       (nama, umur, semester, jurusan))
        conn.commit()
        print("\nAnggota berhasil ditambahkan.")

        while True:
            tambah_lagi = input("Apakah ingin menambahkan anggota lagi? (Y/N): ").strip().upper()
            if tambah_lagi == 'Y':
                break
            elif tambah_lagi == 'N':
                clear_screen()
                return
            else:
                print("Pilihan tidak valid. Silakan pilih Y atau N.")
                time.sleep(2)
                clear_screen()

def tampilkan_daftar_anggota():
    clear_screen()
    print("\n=== DAFTAR ANGGOTA ===")
    cursor.execute("SELECT * FROM anggota")
    anggota_list = cursor.fetchall()
    for anggota in anggota_list:
        print("Nama: ", anggota[1])
        print("Umur: ", anggota[2])
        print("Semester: ", anggota[3])
        print("Jurusan: ", anggota[4])
        print()
    input("\nTekan Enter untuk kembali.")
    clear_screen()

def edit_anggota():
    clear_screen()
    print("\n=== DAFTAR ANGGOTA ===")
    cursor.execute("SELECT * FROM anggota")
    anggota_list = cursor.fetchall()
    
    if not anggota_list:
        print("Tidak ada anggota yang tersedia.")
        input("\nTekan Enter untuk kembali.")
        clear_screen()
        return

    for idx, anggota in enumerate(anggota_list, 1):
        print(f"{idx}. Nama: {anggota[1]}, Umur: {anggota[2]}, Semester: {anggota[3]}, Jurusan: {anggota[4]}")
    
    while True:
        try:
            nomor = int(input("\nPilih nomor anggota yang ingin diubah: "))
            if 1 <= nomor <= len(anggota_list):
                clear_screen()  # Bersihkan layar setelah memilih nomor anggota
                anggota = anggota_list[nomor - 1]
                nama = anggota[1]
                
                print(f"Anggota yang dipilih: Nama: {nama}, Umur: {anggota[2]}, Semester: {anggota[3]}, Jurusan: {anggota[4]}")
                print("\nPilih data yang ingin diubah:")
                print("1. Ubah nama")
                print("2. Ubah umur")
                print("3. Ubah semester")
                print("4. Ubah jurusan")
                pilihan = input("Pilih opsi: ")
                
                if pilihan == "1":
                    while True:
                        new_nama = input("Masukkan nama baru: ")
                        if not re.match("^[A-Za-z\s]+$", new_nama):
                            print("Nama hanya boleh berisi huruf. Silakan coba lagi.")
                            time.sleep(2)
                            clear_screen()
                            continue

                        # Cek apakah nama baru sudah ada di database
                        cursor.execute("SELECT * FROM anggota WHERE nama=?", (new_nama,))
                        if cursor.fetchone():
                            print("Nama anggota sudah ada. Silakan coba nama lain.")
                            time.sleep(2)
                            clear_screen()
                            continue
                        
                        cursor.execute("UPDATE anggota SET nama=? WHERE nama=?", (new_nama, nama))
                        conn.commit()
                        print("Nama berhasil diubah.")
                        break
                
                elif pilihan == "2":
                    while True:
                        new_umur = input("Masukkan umur baru: ")
                        if not new_umur.isdigit():
                            print("Umur hanya boleh berisi angka. Silakan coba lagi.")
                            time.sleep(2)
                            clear_screen()
                            continue
                        cursor.execute("UPDATE anggota SET umur=? WHERE nama=?", (new_umur, nama))
                        conn.commit()
                        print("Umur berhasil diubah.")
                        break
                
                elif pilihan == "3":
                    while True:
                        new_semester = input("Masukkan semester baru: ")
                        if not new_semester.isdigit():
                            print("Semester hanya boleh berisi angka. Silakan coba lagi.")
                            time.sleep(2)
                            clear_screen()
                            continue
                        cursor.execute("UPDATE anggota SET semester=? WHERE nama=?", (new_semester, nama))
                        conn.commit()
                        print("Semester berhasil diubah.")
                        break
                
                elif pilihan == "4":
                    while True:
                        new_jurusan = input("Masukkan jurusan baru: ")
                        if not re.match("^[A-Za-z\s]+$", new_jurusan):
                            print("Jurusan hanya boleh berisi huruf. Silakan coba lagi.")
                            time.sleep(2)
                            clear_screen()
                            continue
                        cursor.execute("UPDATE anggota SET jurusan=? WHERE nama=?", (new_jurusan, nama))
                        conn.commit()
                        print("Jurusan berhasil diubah.")
                        break
                
                else:
                    print("Pilihan tidak valid.")
                break
            
            else:
                print("Nomor tidak valid. Silakan pilih nomor yang benar.")
        except ValueError:
            print("Input tidak valid. Silakan masukkan nomor yang benar.")

    time.sleep(2)
    clear_screen()

def hapus_anggota():
    clear_screen()
    print("\n=== DAFTAR ANGGOTA ===")
    cursor.execute("SELECT * FROM anggota")
    anggota_list = cursor.fetchall()
    
    if not anggota_list:
        print("Tidak ada anggota yang tersedia.")
        input("\nTekan Enter untuk kembali.")
        clear_screen()
        return

    for idx, anggota in enumerate(anggota_list, 1):
        print(f"{idx}. Nama: {anggota[1]}, Umur: {anggota[2]}, Semester: {anggota[3]}, Jurusan: {anggota[4]}")
    
    while True:
        try:
            nomor = int(input("\nPilih nomor anggota yang ingin dihapus: "))
            if 1 <= nomor <= len(anggota_list):
                nama = anggota_list[nomor - 1][1]  # Ambil nama dari anggota yang dipilih
                konfirmasi = input(f"Apakah Anda yakin ingin menghapus anggota '{nama}'? (Y/N): ").strip().upper()
                if konfirmasi == 'Y':
                    cursor.execute("DELETE FROM anggota WHERE nama=?", (nama,))
                    conn.commit()
                    print("\nAnggota berhasil dihapus.")
                else:
                    print("\nPenghapusan dibatalkan.")
                break
            else:
                print("Nomor tidak valid. Silakan pilih nomor yang benar.")
        except ValueError:
            print("Input tidak valid. Silakan masukkan nomor yang benar.")

    time.sleep(2)
    clear_screen()

def tampilkan_menu_daftar_anggota():
    clear_screen()
    print("\n=== DAFTAR ANGGOTA ===")
    print("1. Tambah Anggota")
    print("2. Tampilkan Daftar Anggota")
    print("3. Edit Anggota")
    print("4. Hapus Anggota")
    print("5. Kembali ke Menu Utama")

def tambah_pelajaran():
    while True:
        clear_screen()
        print("\n=== TAMBAH PELAJARAN ===")

        while True:
            pelajaran = input("Masukkan nama pelajaran: ")
            if not re.match("^[A-Za-z\s]+$", pelajaran):
                print("Nama pelajaran hanya boleh berisi huruf. Silakan coba lagi.")
                time.sleep(2)
                clear_screen()
                continue
            break

        while True:
            guru = input("Masukkan nama guru: ")
            if not re.match("^[A-Za-z\s]+$", guru):
                print("Nama guru hanya boleh berisi huruf. Silakan coba lagi.")
                time.sleep(2)
                clear_screen()
                continue
            break

        # Cek apakah kombinasi pelajaran dan guru sudah ada di database
        cursor.execute("SELECT * FROM pelajaran WHERE pelajaran=? AND guru=?", (pelajaran, guru))
        if cursor.fetchone():
            print("Kombinasi nama pelajaran dan nama guru sudah ada. Silakan coba kombinasi lain.")
            time.sleep(2)
            clear_screen()
            continue

        # Tambahkan pelajaran ke database
        cursor.execute("INSERT INTO pelajaran (pelajaran, guru) VALUES (?, ?)", (pelajaran, guru))
        conn.commit()
        print("\nPelajaran berhasil ditambahkan.")

        while True:
            tambah_lagi = input("Apakah ingin menambahkan pelajaran lagi? (Y/N): ").strip().upper()
            if tambah_lagi == 'Y':
                break
            elif tambah_lagi == 'N':
                clear_screen()
                return
            else:
                print("Pilihan tidak valid. Silakan pilih Y atau N.")
                time.sleep(2)
                clear_screen()

def tampilkan_daftar_pelajaran():
    clear_screen()
    print("\n=== DAFTAR PELAJARAN ===")
    cursor.execute("SELECT * FROM pelajaran")
    pelajaran_list = cursor.fetchall()
    for pelajaran in pelajaran_list:
        print("Nama Pelajaran: ", pelajaran[1])
        print("Nama Guru: ", pelajaran[2])
        print()
    input("\nTekan Enter untuk kembali.")
    clear_screen()

def edit_pelajaran():
    clear_screen()
    print("\n=== DAFTAR PELAJARAN ===")
    cursor.execute("SELECT * FROM pelajaran")
    pelajaran_list = cursor.fetchall()
    
    if not pelajaran_list:
        print("Tidak ada pelajaran yang tersedia.")
        input("\nTekan Enter untuk kembali.")
        clear_screen()
        return

    for idx, pelajaran in enumerate(pelajaran_list, 1):
        print(f"{idx}. Nama Pelajaran: {pelajaran[1]}, Nama Guru: {pelajaran[2]}")
    
    while True:
        try:
            nomor = int(input("\nPilih nomor pelajaran yang ingin diubah: "))
            if 1 <= nomor <= len(pelajaran_list):
                clear_screen()  # Bersihkan layar setelah memilih nomor pelajaran
                pelajaran = pelajaran_list[nomor - 1]
                nama_pelajaran = pelajaran[1]
                
                print(f"Pelajaran yang dipilih: Nama Pelajaran: {nama_pelajaran}, Nama Guru: {pelajaran[2]}")
                print("\nPilih data yang ingin diubah:")
                print("1. Ubah nama pelajaran")
                print("2. Ubah nama guru")
                pilihan = input("Pilih opsi: ")
                
                if pilihan == "1":
                    while True:
                        new_pelajaran = input("Masukkan nama pelajaran baru: ")
                        if not re.match("^[A-Za-z\s]+$", new_pelajaran):
                            print("Nama pelajaran hanya boleh berisi huruf. Silakan coba lagi.")
                            time.sleep(2)
                            clear_screen()
                            continue

                        # Cek apakah nama pelajaran baru sudah ada dengan guru yang sama
                        cursor.execute("SELECT * FROM pelajaran WHERE pelajaran=? AND guru=?", (new_pelajaran, pelajaran[2]))
                        if cursor.fetchone():
                            print("Nama pelajaran sudah ada dengan guru yang sama. Silakan coba nama pelajaran lain.")
                            time.sleep(2)
                            clear_screen()
                            continue
                        
                        # Cek apakah nama pelajaran baru sudah ada dengan guru yang berbeda
                        cursor.execute("SELECT * FROM pelajaran WHERE pelajaran=?", (new_pelajaran,))
                        if cursor.fetchone():
                            print("Nama pelajaran sudah ada dengan guru yang berbeda. Silakan coba nama pelajaran lain.")
                            time.sleep(2)
                            clear_screen()
                            continue
                        
                        cursor.execute("UPDATE pelajaran SET pelajaran=? WHERE pelajaran=? AND guru=?", (new_pelajaran, nama_pelajaran, pelajaran[2]))
                        conn.commit()
                        print("Nama pelajaran berhasil diubah.")
                        break
                
                elif pilihan == "2":
                    while True:
                        new_guru = input("Masukkan nama guru baru: ")
                        if not re.match("^[A-Za-z\s]+$", new_guru):
                            print("Nama guru hanya boleh berisi huruf. Silakan coba lagi.")
                            time.sleep(2)
                            clear_screen()
                            continue

                        # Cek apakah nama guru baru sudah ada dengan pelajaran yang sama
                        cursor.execute("SELECT * FROM pelajaran WHERE pelajaran=? AND guru=?", (pelajaran[1], new_guru))
                        if cursor.fetchone():
                            print("Nama guru sudah ada dengan pelajaran yang sama. Silakan coba nama guru lain.")
                            time.sleep(2)
                            clear_screen()
                            continue
                        
                        cursor.execute("UPDATE pelajaran SET guru=? WHERE pelajaran=? AND guru=?", (new_guru, pelajaran[1], pelajaran[2]))
                        conn.commit()
                        print("Nama guru berhasil diubah.")
                        break
                
                else:
                    print("Pilihan tidak valid.")
                break
            
            else:
                print("Nomor tidak valid. Silakan pilih nomor yang benar.")
        except ValueError:
            print("Input tidak valid. Silakan masukkan nomor yang benar.")

    time.sleep(2)
    clear_screen()

def hapus_pelajaran():
    clear_screen()
    print("\n=== DAFTAR PELAJARAN ===")
    cursor.execute("SELECT * FROM pelajaran")
    pelajaran_list = cursor.fetchall()
    
    if not pelajaran_list:
        print("Tidak ada pelajaran yang tersedia.")
        input("\nTekan Enter untuk kembali.")
        clear_screen()
        return

    for idx, pelajaran in enumerate(pelajaran_list, 1):
        print(f"{idx}. Nama Pelajaran: {pelajaran[1]}, Nama Guru: {pelajaran[2]}")
    
    while True:
        try:
            nomor = int(input("\nPilih nomor pelajaran yang ingin dihapus: "))
            if 1 <= nomor <= len(pelajaran_list):
                nama_pelajaran = pelajaran_list[nomor - 1][1]  # Ambil nama pelajaran dari pelajaran yang dipilih
                konfirmasi = input(f"Apakah Anda yakin ingin menghapus pelajaran '{nama_pelajaran}'? (Y/N): ").strip().upper()
                if konfirmasi == 'Y':
                    cursor.execute("DELETE FROM pelajaran WHERE pelajaran=?", (nama_pelajaran,))
                    conn.commit()
                    print("\nPelajaran berhasil dihapus.")
                else:
                    print("\nPenghapusan dibatalkan.")
                break
            else:
                print("Nomor tidak valid. Silakan pilih nomor yang benar.")
        except ValueError:
            print("Input tidak valid. Silakan masukkan nomor yang benar.")

    time.sleep(2)
    clear_screen()

def tampilkan_menu_daftar_pelajaran():
    clear_screen()
    print("\n=== DAFTAR PELAJARAN ===")
    print("1. Tambah Pelajaran")
    print("2. Tampilkan Daftar Pelajaran")
    print("3. Edit Pelajaran")
    print("4. Hapus Pelajaran")
    print("5. Kembali ke Menu Utama")

def tampilkan_daftar_nama_dan_pelajaran():
    clear_screen()
    print("\n=== DAFTAR NAMA DAN PELAJARAN ===")

    # Tampilkan daftar nama anggota dengan nomor urut
    print("Daftar Nama Anggota:")
    cursor.execute("SELECT * FROM anggota")
    anggota_list = cursor.fetchall()
    if anggota_list:
        for idx, anggota in enumerate(anggota_list, 1):
            print(f"{idx}. Nama: {anggota[1]}")
            print(f"   Umur: {anggota[2]}")
            print(f"   Semester: {anggota[3]}")
            print(f"   Jurusan: {anggota[4]}")
            print()
    else:
        print("Tidak ada anggota yang tersedia.")
    
    # Tampilkan daftar pelajaran dengan nomor urut
    print("Daftar Pelajaran:")
    cursor.execute("SELECT * FROM pelajaran")
    pelajaran_list = cursor.fetchall()
    if pelajaran_list:
        for idx, pelajaran in enumerate(pelajaran_list, 1):
            print(f"{idx}. Nama Pelajaran: {pelajaran[1]}")
            print(f"   Nama Guru: {pelajaran[2]}")
            print()
    else:
        print("Tidak ada pelajaran yang tersedia.")

    input("\nTekan Enter untuk kembali.")
    clear_screen()

def login():
    clear_screen()
    username = input("Username: ")
    password = input("Password: ")

    cursor.execute("SELECT * FROM pengguna WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    if user:
        global is_login
        is_login = True
        print("\nLogin berhasil.")
    else:
        print("\nUsername atau password salah. Silakan coba lagi.")
    time.sleep(2)
    clear_screen()

def registrasi():
    clear_screen()
    while True:
        username = input("Buat username baru: ")
        if not re.match("^[A-Za-z]+$", username):
            print("Username hanya boleh berisi huruf. Silakan coba lagi.")
            time.sleep(2)
            clear_screen()
            continue

        cursor.execute("SELECT * FROM pengguna WHERE username=?", (username,))
        if cursor.fetchone():
            print("Username sudah ada. Silakan coba username lain.")
            time.sleep(2)
            clear_screen()
            continue
        break

    while True:
        password = input("Buat password baru: ")
        if not re.match("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$", password):
            print("Password harus minimal 8 karakter, mengandung huruf dan angka. Simbol opsional.")
            time.sleep(2)
            clear_screen()
            continue
        break

    cursor.execute("INSERT INTO pengguna (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    print("\nRegistrasi berhasil. Silakan login dengan akun baru.")
    time.sleep(2)
    clear_screen()

def main():
    global is_login  # Mengakses variabel global
    tampilkan_splash_screen()
    
    while True:
        if not is_login:
            clear_screen()
            print("=== SELAMAT DATANG ===")
            print("Silakan login atau registrasi.")
            print("1. Login")
            print("2. Registrasi")
            print("3. Keluar")
            choice = input("Pilihan: ")

            if choice == "1":
                login()
            elif choice == "2":
                registrasi()
            elif choice == "3":
                break
            else:
                print("Pilihan tidak valid.")
                time.sleep(2)
                clear_screen()

        else:
            while True:
                tampilkan_menu_utama()
                pilihan = input("Pilihan opsi: ")

                if pilihan == "1":
                    while True:
                        tampilkan_menu_daftar_anggota()
                        sub_pilihan = input("Pilihan opsi: ")

                        if sub_pilihan == "1":
                            tambah_anggota()
                        elif sub_pilihan == "2":
                            tampilkan_daftar_anggota()
                        elif sub_pilihan == "3":
                            edit_anggota()
                        elif sub_pilihan == "4":
                            hapus_anggota()
                        elif sub_pilihan == "5":
                            clear_screen()
                            break
                        else:
                            print("Pilihan tidak valid.")
                            time.sleep(2)
                            clear_screen()

                elif pilihan == "2":
                    while True:
                        tampilkan_menu_daftar_pelajaran()
                        sub_pilihan = input("Pilihan opsi: ")

                        if sub_pilihan == "1":
                            tambah_pelajaran()
                        elif sub_pilihan == "2":
                            tampilkan_daftar_pelajaran()
                        elif sub_pilihan == "3":
                            edit_pelajaran()
                        elif sub_pilihan == "4":
                            hapus_pelajaran()
                        elif sub_pilihan == "5":
                            clear_screen()
                            break
                        else:
                            print("Pilihan tidak valid.")
                            time.sleep(2)
                            clear_screen()

                elif pilihan == "3":
                    tampilkan_daftar_nama_dan_pelajaran()

                elif pilihan == "4":
                    # Logout
                    is_login = False
                    clear_screen()
                    print("Anda telah logout.")
                    time.sleep(2)
                    break

                elif pilihan == "5":
                    sys.exit()

                else:
                    print("Pilihan tidak valid.")
                    time.sleep(2)
                    clear_screen()

# Menutup koneksi database ketika program selesai
if __name__ == "__main__":
    main()
    conn.close()
