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
                konfigurasi.append(f'{sub}{sisa_elektron}')
                sisa_elektron = 0
    return ' '.join(konfigurasi)

print(konfigurasi_elektron(20))