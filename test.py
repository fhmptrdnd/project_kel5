import pandas as pd
import getpass
from tabulate import tabulate
import os

def logIn(username, password):
    sukses = False
    file = open("project_kel5/datauser.csv", "r")
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
        if username == 'Admin' and password == 'AdminProPlayer':
            os.system('cls')
            akses_admin()
        else:
            akses_pelanggan()
    else:
        input('\nUsername atau password salah atau tidak terdaftar.\nJika belum memiliki akun, silahkan Sign Up terlebih dahulu.\nLupa password? Pilih menu nomor 3.')
        awal()


def signUp(username, password, email):
    # bagian cek apa username sudah ada di datauser atau ngga
    file = open("project_kel5/datauser.csv", "r")
    for i in file:
        try:
            a, _, _ = i.split(',', 2)
            if a == username:
                input('\nUsername sudah ada. Silahkan pilih username lain.')
                file.close()
                awal()
                return
        except ValueError:
            continue
    file.close()

    # bagian nambahin data pengguna kalau belum ada
    file = open("project_kel5/datauser.csv", "a")
    file.write("\n" + username + "," + password + "," + email)
    file.close()
    input('Sign Up berhasil, silahkan masuk.')
    awal()

def lupa_password(username, email):
    sukses = False
    file = open("project_kel5/datauser.csv", "r")
    lines = file.readlines()  # Ini fungsi buat manipulasi csv per baris
    file.close()
    
    for i in lines:
        try:
            a, b, c = i.split(',', 2)
            c = c.strip()
            if a == username and c == email:
                sukses = True
                break
        except ValueError:
            continue  
    
    if sukses:
        new_password = input('Masukkan password baru: ').strip()
        file = open("project_kel5/datauser.csv", "w")
        for i in lines:
            try:
                a, b, c = i.split(',', 2)
                c = c.strip()
                if a == username and c == email:
                    file.write(f"{username},{new_password},{email}\n")
                else:
                    file.write(i)
            except ValueError:
                file.write(i)  # nulis ulang baris yang gk sesuai format
        file.close()
        input('Password berhasil diganti. Silahkan login dengan password baru.')
        awal()
    else:
        input('\nUsername atau email tidak terdaftar.')
        awal()

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
        print('\nTerima kasih sudah berkunjung!\n')

def akses_admin():
    while True:
        print('\nHalo Admin!\nMau ngapain hari ini?')
        print('='*50)
        print('1. Data Petani\n2. Data Pesanan\n3. Data Pengguna\n4. Keluar')
        print('='*50)
        try:
            opsi_admin = int(input('Silahkan pilih menu (1/2/3/4): '))
            if opsi_admin == 1:
                data_petani = pd.read_csv('percobaan_kel5/datapetaniTasya.csv')
                print(tabulate(data_petani, headers='keys', tablefmt='grid', showindex=False))
            elif opsi_admin == 2:
                print('Fitur Data Pesanan belum tersedia.') 
            elif opsi_admin == 3:
                data_pengguna = pd.read_csv('project_kel5/datauser.csv')
                data_pengguna = data_pengguna.drop(data_pengguna.columns[1], axis=1) # ini fungsinya ngehapus kolom kedua berdasarkan index
                print(tabulate(data_pengguna, headers='keys', tablefmt='grid', showindex=False))
            elif opsi_admin == 4:
                print('Kembali ke menu utama.')
                awal()
                break
            else:
                input('\nHarap pilih menu yang ada.')
        except ValueError:
            input('\nHarap pilih menu yang ada.')

def akses_pelanggan(opsi_pelanggan) :
    if opsi_pelanggan == 1 :
        data_petani = pd.read_csv('percobaan_kel5/datapetaniTasya.csv')
        print(tabulate(data_petani, headers='keys', tablefmt='grid', showindex=False))
        #aku bingung gimana caranya user milih jasa petaninya
        
def akses_pelanggan():
    print('\nLogin berhasil\n')
    print('Hai, mau ngapain hari ini?')
    print('='*50)
    print('1. Pilih Jasa Petani.\n2. Cek Saldo.\n3. Keluar')
    print('='*50)
    opsi_pelanggan= input('Silahkan pilih menu (1/2/3): ')
    if opsi_pelanggan.isdigit() and int(opsi_pelanggan) in [1,2] :
        opsi_pelanggan=int(opsi_pelanggan)
        akses_pelanggan(opsi_pelanggan)
    else :
        input('\nHarap pilih menu yang ada.')
        return
    
def awal():
    global opsi
    print('\nSelamat datang di Smart Farm!')
    print('='*50)
    print('1. Log In (Masuk ke akun yang sudah ada.)\n2. Sign Up (Untuk mendaftar akun baru.)\n3. Lupa Password\n4. Keluar')
    print('='*50)
    
    opsi = input('Silahkan pilih menu untuk masuk ke aplikasi (1/2/3/4): ')
    
    if opsi.isdigit() and int(opsi) in [1, 2, 3, 4]: # Ini meriksa kalau input itu angka dan termasuk di pilihan yang ada apa engga
        opsi = int(opsi)
        akses(opsi)
    else:
        input('\nHarap pilih menu yang ada.')
        awal()

awal()
