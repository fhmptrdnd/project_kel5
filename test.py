import pandas as pd
import getpass
from tabulate import tabulate
import os

def logIn(username, password, email):
    sukses = False
    file = open("datauser.csv", "r")
    for i in file:
        a, b = i.split(',')
        b = b.strip()
        if a == username and b == password:
            sukses = True
            break
    file.close()
    if sukses:
        if username == 'Admin' and password == 'AdminProPlayer':
            os.system('cls')
            akses_admin()
        else:
            akses_pelanggan()
    else:
        input('\nUsername atau password salah atau tidak terdaftar.\nJika belum memiliki akun, silahkan Sign Up terlebih dahulu.')
        awal()

def signUp(username, password, email):
    file = open("datauser.csv", "a")
    file.write("\n" + username + "," + password + "," + email)
    file.close()

def akses(opsi):
    global username, email
    if opsi == 1:
        username = input('\nMasukkan Username: ').strip()
        password = getpass.getpass(('Masukkan Password: '))
        logIn(username, password)
    elif opsi == 2:
        username = input('\nMasukkan Username Baru: ').strip()
        password = input('Masukkan Password Baru: ')
        email = input('Masukkan alamat email: ').strip()
        signUp(username, password, email)
        input('Sign Up berhasil, silahkan masuk.')
        awal()
    elif opsi == 3:
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
                print('Fitur Data Petani belum tersedia.') #nama petani, alamat petani, skill (5)
            elif opsi_admin == 2:
                print('Fitur Data Pesanan belum tersedia.') #
            elif opsi_admin == 3:
                data_pengguna = pd.read_csv('datauser.csv')
                print(tabulate(data_pengguna, headers='keys', tablefmt='grid', showindex=False))
            elif opsi_admin == 4:
                print('Kembali ke menu utama.')
                awal()
                break
            else:
                input('\nHarap pilih menu yang ada.')
        except ValueError:
            input('\nHarap pilih menu yang ada.')

def akses_pelanggan():
    print('\nLogin berhasil\n')
    
def awal():
    global opsi
    print('\nSelamat datang di Smart Farm!')
    print('='*50)
    print('1. Log In (Masuk ke akun yang sudah ada.)\n2. Sign Up (Untuk mendaftar akun baru.)\n3. Keluar')
    print('='*50)
    try:
        opsi = int(input('Silahkan pilih menu untuk masuk ke aplikasi (1/2/3): '))
        if opsi in [1, 2, 3]:
            akses(opsi)
        else:
            input('\nHarap pilih menu yang ada.')
            awal()
    except ValueError:
        input('\nHarap pilih menu yang ada.')
        awal()

awal()
