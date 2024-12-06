import pandas as pd
import getpass
from datetime import datetime, timedelta
from tabulate import tabulate
import os
import csv

def logIn(username, password):
    sukses = False
    file = open("datauser.csv", "r")
    for i in file:
        try:
            a, b, _ = i.split(',', 2)  # maxsplit 2 kolom
            b = b.strip()
            if a == username and b == password:
                sukses = True
                break
        except ValueError:
            continue  # baris yg ga sesuai format diskip aja
    file.close()
    if sukses:
        if username == 'Admin' and password == 'Admin123':
            os.system('cls')
            akses_admin()
        else:
            os.system('cls')
            akses_pelanggan()
    else:
        input('\nUsername atau password salah atau tidak terdaftar.\nJika belum memiliki akun, silahkan Sign Up terlebih dahulu.\n(Lupa password? Pilih menu nomor 3.)')
        os.system('cls')
        awal()


def signUp(username, password, email):
    if not username or not password or not email: 
        input('\nUsername, password, dan email tidak boleh kosong. Silahkan coba lagi.')
        return
    # bagian cek apa username sudah ada di datauser atau ngga
    file = open("datauser.csv", "r")
    for i in file:
        try:
            a, _, _ = i.split(',', 2)
            if a == username:
                input('\nUsername tidak tersedia. Silahkan gunakan username lain.')
                file.close()
                return
        except ValueError:
            continue
    file.close()
    nsaldo = "0"
    # bagian nambahin data pengguna kalau belum ada
    file = open("datauser.csv", "a")
    file.write(username + "," + password + "," + email + "," + nsaldo + "\n")
    file.close()
    input('Sign Up berhasil, silahkan masuk.')
    os.system('cls')

def lupa_password(username, email):
    sukses = False
    lines = []

    if not username or not email:
        input('\nUsername dan email tidak boleh kosong. Silahkan coba lagi.')
        return

    with open("datauser.csv", "r") as file:
        lines = file.readlines()

    for i in lines:
        try:
            a, b, c, d = i.strip().split(',')
            if a == username and c == email:
                sukses = True
                break
        except ValueError:
            continue
    
    if sukses:
        while True:
            new_password = input('Masukkan password baru: ').strip()
            if not new_password:
                input('\nPassword baru tidak boleh kosong. Silahkan coba lagi.')
            else:
                break
        
        updated_lines = []
        for i in lines:
            try:
                a, b, c, d = i.strip().split(',')
                if a == username and c == email:
                    updated_lines.append(f"{username},{new_password},{email},{d}\n")
                else:
                    updated_lines.append(f"{a},{b},{c},{d}\n")
            except ValueError:
                updated_lines.append(i)  # Menulis ulang baris yang tidak sesuai format

        with open("datauser.csv", "w", newline='') as file:
            file.writelines(updated_lines)
        
        input('\nPassword berhasil diganti.\nSilahkan login dengan password baru.')
        os.system('cls')
    else:
        input('\nUsername atau email tidak terdaftar.\nSilahkan coba lagi.')
        os.system('cls')

def ganti_username(username, password, email):
    sukses = False
    data = []

    if not username or not password or not email:
        input('\nUsername, password, dan email tidak boleh kosong. Silahkan coba lagi.')
        return

    with open("datauser.csv", "r", newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3:
                user, pwd, mail = row[0].strip(), row[1].strip(), row[2].strip()
                if user == username and pwd == password and mail == email:
                    sukses = True
                    print("\nUsername, password, dan email ditemukan.")
                data.append(row)

    if sukses:
        while True:
            new_username = input('Masukkan username baru: ').strip()
            if not new_username:
                input('\nUsername baru tidak boleh kosong. Silahkan coba lagi.')
            else:
                break

        for row in data:
            user, pwd, mail = row[0].strip(), row[1].strip(), row[2].strip()
            if user == username and pwd == password and mail == email:
                row[0] = new_username
        
        with open("datauser.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        input('\nUsername berhasil diganti.\nSilahkan login dengan username baru.')
        os.system('cls')
    else:
        input('\nUsername, password, atau email tidak terdaftar.\nSilahkan coba lagi.')
        os.system('cls')

def akses(opsi):
    global username, email
    if opsi == 1:
        username = input('\nMasukkan Username: ').strip()
        password = getpass.getpass('Masukkan Password: ')
        logIn(username, password)
    elif opsi == 2:
        username = input('\nMasukkan Username Baru: ').strip()
        password = input('Masukkan Password Baru: ')
        email = input('Masukkan alamat email: ').strip()
        signUp(username, password, email)
    elif opsi == 3:
        username = input('\nMasukkan Username: ').strip()
        email = input('Masukkan alamat email: ').strip()
        lupa_password(username, email)
    elif opsi == 4:
        username = input('\nMasukkan Username: ').strip()
        password = input('Masukkan Password: ')
        email = input('Masukkan alamat email: ').strip()
        ganti_username(username, password, email)
    elif opsi == 5:
        print('\nTerima kasih sudah berkunjung!\n')
        return True
    return False

def cek_username_terdaftar(username):
    # Membaca file datauser.csv
    with open("datauser.csv", "r") as file:
        for i in file:
            try:
                a = i.split(',')[0]  # Ambil elemen pertama aja
                if a == username:
                    return True  # Username ditemukan
            except IndexError:
                continue  # Skip baris kosong atau gk valid
    return False  # Username tidak ditemukan

def tambah_saldo_admin(username, jumlah_tambah):
    data = []

    with open("datauser.csv", "r", newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 4:  # pastiin ada 4 kolom (Username, Password, Email, Saldo)
                user, pwd, mail, saldo = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip()
                if user == username:
                    try:
                        new_saldo = float(saldo) + jumlah_tambah if saldo else jumlah_tambah
                    except ValueError:
                        new_saldo = jumlah_tambah  # Jika saldo saat ini kosong atau tidak valid, set saldo baru
                    row[3] = str(new_saldo)
                    print(f"Saldo untuk {username} berhasil ditambahkan sebesar {jumlah_tambah}.")
                data.append(row)
            else:
                data.append(row)

    # Menulis ulang file CSV dengan data yang sudah di-update
    with open("datauser.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def cek_saldo(username):
    try:
        data_saldo = pd.read_csv('datauser.csv')
        user_saldo = data_saldo.loc[data_saldo['Username'] == username, 'Saldo']
        if not user_saldo.empty:
            return user_saldo.values[0]
    except FileNotFoundError:
        print("File saldo tidak ditemukan.")
    return None

def update_saldo(username, new_saldo):
    data_pengguna = pd.read_csv('datauser.csv')
    for i, row in data_pengguna.iterrows():
        if row['Username'] == username:
            data_pengguna.at[i, 'Saldo'] = new_saldo
            data_pengguna.to_csv('datauser.csv', index=False)
            return True
    return False

def simpan_riwayat_pembelian(username, nama_petani, skill_petani, lama_sewa, biaya_sewa, tanggal_mulai, tanggal_selesai):
    try:
        riwayat_data = {
            'Username': username,
            'Nama Petani': nama_petani,
            'Keahlian Jasa': skill_petani,
            'Lama Sewa': lama_sewa,
            'Biaya Sewa': biaya_sewa,
            'Tanggal Mulai': tanggal_mulai.strftime('%d-%m-%Y'),
            'Tanggal Selesai': tanggal_selesai.strftime('%d-%m-%Y')
        }

        # cek misal file riwayat pembelian udah ada
        if os.path.isfile('riwayat_pembelian.csv'):
            existing_data = pd.read_csv('riwayat_pembelian.csv')
            updated_data = existing_data._append(riwayat_data, ignore_index=True)
            updated_data.to_csv('riwayat_pembelian.csv', index=False)
        else:
            riwayat_df = pd.DataFrame([riwayat_data])
            riwayat_df.to_csv('riwayat_pembelian.csv', index=False)
    except FileNotFoundError:
        riwayat_df = pd.DataFrame([riwayat_data])
        riwayat_df.to_csv('riwayat_pembelian.csv', index=False)

def cetak_nota(username, nama_petani, skill_petani, lama_sewa, biaya_sewa, tanggal_mulai, tanggal_selesai):
    nota = f"""
    ==============================
             Nota Pembelian
    ==============================
    Username: {username}
    Nama Petani: {nama_petani}
    Keahlian Jasa: {skill_petani}
    Lama Sewa: {lama_sewa} hari
    Biaya Sewa: Rp.{biaya_sewa:,.2f}
    Tanggal Mulai: {tanggal_mulai.strftime('%d-%m-%Y')}
    Tanggal Selesai: {tanggal_selesai.strftime('%d-%m-%Y')}
    ==============================
    Terima kasih atas pembelian Anda!
    """
    print(nota)

def checkout_sewa_petani(username):
    data_petani = pd.read_csv('datapetani.csv')
    print("\n" + tabulate(data_petani, headers='keys', tablefmt='grid', showindex=range(1, len(data_petani)+1)))

    try:
        pilihan = int(input('Silahkan pilih nomor petani yang ingin Anda sewa (Enter untuk keluar): '))
        if pilihan < 1 or pilihan > len(data_petani):
            input('\nHarap pilih nomor petani yang ada.')
            return

        status_petani = data_petani.at[pilihan - 1, 'Status']
        if status_petani.lower() != 'tersedia':
            input('\nPetani tidak tersedia untuk disewa.')
            return

        saldo_anda = cek_saldo(username)
        print("="*80 + f"\nSisa saldo Anda: {saldo_anda:,.2f}" + "\n" + "="*80)
        lama_sewa = int(input('Masukkan lama sewa (minimal 7 hari kerja): '))
        if lama_sewa < 7:
            input('\nLama sewa minimal adalah 7 hari kerja.')
            return

        biaya_sewa = lama_sewa * 35000

        if saldo_anda is not None and saldo_anda >= biaya_sewa:
            new_saldo = saldo_anda - biaya_sewa
            update_saldo(username, new_saldo)

            nama_petani = data_petani.at[pilihan - 1, 'Nama']
            skill_petani = data_petani.at[pilihan - 1, 'Skill']

            tanggal_mulai = datetime.now().date()
            tanggal_selesai = tanggal_mulai + timedelta(days=lama_sewa)

            cetak_nota(username, nama_petani, skill_petani, lama_sewa, biaya_sewa, tanggal_mulai, tanggal_selesai)
            simpan_riwayat_pembelian(username, nama_petani, skill_petani, lama_sewa, biaya_sewa, tanggal_mulai, tanggal_selesai)

            data_petani.at[pilihan - 1, 'Status'] = 'Tidak Tersedia'
            data_petani.to_csv('datapetani.csv', index=False)

            print(f"\nCheckout berhasil. Anda telah menyewa petani selama {lama_sewa} hari kerja dengan biaya Rp.{biaya_sewa:,.2f}")
            input(f"Sisa saldo Anda: Rp.{new_saldo:,.2f}")
        else:
            input('\nSaldo tidak mencukupi untuk melakukan sewa.')
    except ValueError:
        print('\nHarap masukkan nomor yang valid.')
    os.system('cls')

def lihat_riwayat_pembelian_pelanggan_admin():
    try:
        data_riwayat = pd.read_csv('riwayat_pembelian.csv')
        if not data_riwayat.empty:
            input("\n" + tabulate(data_riwayat, headers='keys', tablefmt='grid', showindex=range(1, len(data_riwayat)+1)))
        else:
            input("\nTidak ada riwayat pembelian yang ditemukan.")
    except FileNotFoundError:
        input("\nTidak ada riwayat pembelian yang ditemukan.")

def lihat_riwayat_pembelian(username):
    try:
        data_riwayat = pd.read_csv('riwayat_pembelian.csv')
        riwayat_user = data_riwayat[data_riwayat['Username'] == username]
        if not riwayat_user.empty:
            input("\n" + tabulate(riwayat_user, headers='keys', tablefmt='grid', showindex=range(1, len(riwayat_user)+1)))
        else:
            input("\nTidak ada riwayat pembelian untuk user ini.")
    except FileNotFoundError:
        input("\nTidak ada riwayat pembelian yang ditemukan.")

def akses_pelanggan():
    while True:
        print(f'\nHai {username}, mau ngapain hari ini?')
        print('='*50)
        print('1. Pilih Jasa Petani.\n2. Cek Saldo.\n3. Lihat Riwayat Pembelian\n4. Keluar')
        print('='*50)
        try:
            opsi_pelanggan = int(input('Silahkan pilih menu (1/2/3/4): '))
            if opsi_pelanggan == 1:
                checkout_sewa_petani(username)
            elif opsi_pelanggan == 2:
                saldo = cek_saldo(username)
                if saldo is not None:
                    print(f"\nSaldo Anda saat ini: Rp.{saldo:,.2f}")
                    input('Ingin melakukan top-up saldo? Silahkan menghubungi nomor di bawah:\n+6281359749043')
                else:
                    input("\nUsername tidak ditemukan.")
            elif opsi_pelanggan == 3:
                lihat_riwayat_pembelian(username)
            elif opsi_pelanggan == 4:
                os.system('cls')
                break
            else:
                input('\nHarap pilih menu yang ada.')
                os.system('cls')
        except ValueError:
            input('\nHarap pilih menu yang ada.')
            os.system('cls')

def akses_admin():
    while True:
        print('\nHalo Admin!\nMau ngapain hari ini?')
        print('='*50)
        print('1. Data Petani\n2. Data Pesanan\n3. Data Pengguna\n4. Tambah saldo user\n5. Tambah Data Petani\n6. Hapus Data Petani\n7. Hapus Riwayat Pembelian\n8. Keluar')
        print('='*50)
        try:
            opsi_admin = int(input('Silahkan pilih menu (1/2/3/4/5/6/7/8): '))
            if opsi_admin == 1:
                data_petani = pd.read_csv('datapetani.csv')
                input(tabulate(data_petani, headers='keys', tablefmt='grid', showindex=range(1, len(data_petani)+1)))
                try:
                    petani_index = int(input('Silahkan pilih nomor petani yang ingin diubah statusnya: '))
                    if petani_index == 0:
                        input('Tidak ada perubahan status yang dilakukan.')
                    elif petani_index < 1 or petani_index > len(data_petani):
                        input('\nHarap pilih nomor petani yang ada.')
                    else:
                        status_sekarang = data_petani.at[petani_index - 1, 'Status']
                        status_baru = 'Tidak Tersedia' if status_sekarang == 'Tersedia' else 'Tersedia'
                        data_petani.at[petani_index - 1, 'Status'] = status_baru
                        print('\nStatus berhasil diubah.')
                        input(tabulate(data_petani, headers='keys', tablefmt='grid', showindex=range(1, len(data_petani)+1)))
                        data_petani.to_csv('datapetani.csv', index=False)
                except ValueError:
                    input('\nHarap masukkan nomor yang valid.')
            elif opsi_admin == 2:
                lihat_riwayat_pembelian_pelanggan_admin()
                os.system('cls')
            elif opsi_admin == 3:
                data_pengguna = pd.read_csv('datauser.csv')
                data_pengguna = data_pengguna.drop(data_pengguna.columns[1], axis=1) # ini fungsinya ngehapus kolom kedua berdasarkan index
                input(tabulate(data_pengguna, headers='keys', tablefmt='grid', showindex=range(1, len(data_pengguna)+1)))
            elif opsi_admin == 4:
                username = input("\nMasukkan Username Pengguna yang akan diisi saldo: ").strip()
                if cek_username_terdaftar(username):
                    try:
                        jumlah_tambah = float(input("Masukkan jumlah saldo yang ingin ditambahkan: "))
                        tambah_saldo_admin(username, jumlah_tambah)
                    except ValueError:
                        input('Harap masukkan nominal yang benar.')
                else:
                    print("\nUsername tidak terdaftar. Saldo tidak dapat ditambahkan.")
            elif opsi_admin == 5:
                nama_petani = input("\nMasukkan Nama Petani: ").strip()
                skill_petani = input("Masukkan Skill Petani: ").strip()
                alamat_petani = input("Masukkan Alamat Petani: ").strip()
                if not nama_petani or not skill_petani or not alamat_petani:
                    input('\nUsername dan email tidak boleh kosong. Silahkan coba lagi.')
                    akses_admin()
                else:
                    break
                data_petani = pd.read_csv('datapetani.csv')
                data_petani = data_petani._append({'Nama': nama_petani, 'Skill': skill_petani, 'Alamat': alamat_petani, 'Status': 'Tersedia'}, ignore_index=True)
                data_petani.to_csv('datapetani.csv', index=False)
                print("\nData petani berhasil ditambahkan.")
            elif opsi_admin == 6:
                data_petani = pd.read_csv('datapetani.csv')
                print("\n" + tabulate(data_petani, headers='keys', tablefmt='grid', showindex=range(1, len(data_petani)+1)))
                try:
                    petani_index = int(input('Silahkan pilih nomor petani yang ingin dihapus: '))
                    if petani_index < 1 or petani_index > len(data_petani):
                        input('\nHarap pilih nomor petani yang ada.')
                    else:
                        data_petani = data_petani.drop(petani_index - 1)
                        data_petani.to_csv('datapetani.csv', index=False)
                        print('\nData petani berhasil dihapus.')
                except ValueError:
                    input('\nHarap masukkan nomor yang valid.')
            elif opsi_admin == 7:
                data_riwayat = pd.read_csv('riwayat_pembelian.csv')
                print("\n" + tabulate(data_riwayat, headers='keys', tablefmt='grid', showindex=range(1, len(data_riwayat)+1)))
                try:
                    riwayat_index = int(input('Silahkan pilih nomor riwayat pembelian yang ingin dihapus: '))
                    if riwayat_index < 1 or riwayat_index > len(data_riwayat):
                        input('\nHarap pilih nomor riwayat pembelian yang ada.')
                    else:
                        data_riwayat = data_riwayat.drop(riwayat_index - 1)
                        data_riwayat.to_csv('riwayat_pembelian.csv', index=False)
                        print('\nRiwayat pembelian berhasil dihapus.')
                except ValueError:
                    input('\nHarap masukkan nomor yang valid.')
            elif opsi_admin == 8:
                os.system('cls')
                break
            else:
                input('\nHarap pilih menu yang ada.')
        except ValueError:
            input('\nHarap pilih menu yang ada.')
        os.system('cls')    
        
def akses(opsi):
    global username, email
    if opsi == 1:
        username = input('\nMasukkan Username: ').strip()
        password = getpass.getpass('Masukkan Password: ')
        logIn(username, password)
    elif opsi == 2:
        username = input('\nMasukkan Username Baru: ').strip()
        password = input('Masukkan Password Baru: ')
        email = input('Masukkan alamat email: ').strip()
        signUp(username, password, email)
    elif opsi == 3:
        username = input('\nMasukkan Username: ').strip()
        email = input('Masukkan alamat email: ').strip()
        lupa_password(username, email)
    elif opsi == 4:
        username = input('\nMasukkan Username: ').strip()
        password = input('Masukkan Password: ')
        email = input('Masukkan alamat email: ').strip()
        ganti_username(username, password, email)
    elif opsi == 5:
        print('\nTerima kasih sudah berkunjung!\n')
        return True
    return False

def awal():
    while True:
        global opsi
        print('\nSelamat datang di Smart Farm!')
        print('='*50)
        print('1. Log In (Masuk ke akun yang sudah ada.)\n2. Sign Up (Untuk mendaftar akun baru.)\n3. Lupa/Ganti Password\n4. Ganti Username\n5. Keluar')
        print('='*50)
        
        opsi = input('Silahkan pilih menu untuk masuk ke aplikasi (1/2/3/4/5): ')
        
        if opsi.isdigit() and int(opsi) in [1, 2, 3, 4, 5]:
            opsi = int(opsi)
            os.system('cls')
            if akses(opsi):
                break
        else:
            input('\nHarap pilih menu yang ada.')
            os.system('cls')

awal()