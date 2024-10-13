def konfigurasi_elektron(nomor_atom):
    sub_kulit = {
        '1s': 2,
        '2s': 2,
        '2p': 6,
        '3s': 2,
        '3p': 6,
        '4s': 2,
        '3d': 10,
        '4p': 6,
        '5s': 2,
        '4d': 10,
        '5p': 6,
        '6s': 2,
        '4f': 14,
        '5d': 10,
        '6p': 6,
        '7s': 2,
        '5f': 14,
        '6d': 10,
        '7p': 6
    }

    konfigurasi = []
    sisa_elektron = nomor_atom

    for sub, kapasitas in sub_kulit.items():
        if sisa_elektron > 0:
            if sisa_elektron >= kapasitas:
                konfigurasi.append(f'{sub}{kapasitas}')
                sisa_elektron -= kapasitas
            else:
                konfigurasi.append(f'{sub}{kapasitas}')
                sisa_elektron = 0
    return ' '.join(konfigurasi)

def mengambil_konfigurasi_terakhir(konfigurasi) :
    subkulit_terakhir = konfigurasi.split() [-1]
    for subkulit in subkulit_terakhir:
        if subkulit.isalpha():
            return subkulit

def bilangan_kuantum_azimut(konfigurasi):
    nilai_kulit = {
        's': 0,
        'p': 1,
        'd': 2,
        'f': 3
    }
    konfigurasi_terakhir = mengambil_konfigurasi_terakhir(konfigurasi)
    return nilai_kulit.get(konfigurasi_terakhir)

__init__ = '__main__' 
