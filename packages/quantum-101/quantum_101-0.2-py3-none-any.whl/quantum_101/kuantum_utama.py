modulKulit = __import__('Modul kulit')

def kuantumUtama(nomor_atom):
    konfigurasi = modulKulit.konfigurasi_elektron(nomor_atom)

    return konfigurasi[len(konfigurasi) - 3]