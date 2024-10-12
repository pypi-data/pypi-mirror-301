def Kuantum_Magnetik(nomor_atom): 
    sub_kulit = [
        ('1s', 2), ('2s', 2), ('2p', 6), 
        ('3s', 2), ('3p', 6), ('4s', 2), 
        ('3d', 10), ('4p', 6), ('5s', 2), 
        ('4d', 10), ('5p', 6), ('6s', 2), 
        ('4f', 14), ('5d', 10), ('6p', 6), 
        ('7s', 2), ('5f', 14), ('6d', 10), 
        ('7p', 6)
    ]
    konfigurasi = []
    sisa_elektron = nomor_atom
    subkulit_terakhir = None
    elektron_terakhir = 0
    for sub, kapasitas in sub_kulit:
        if sisa_elektron > 0:
            elektron_diisi = min(sisa_elektron, kapasitas)
            konfigurasi.append(f'{sub}{elektron_diisi}')
            sisa_elektron -= elektron_diisi 
            if sisa_elektron == 0:
                subkulit_terakhir = sub 
                elektron_terakhir = elektron_diisi  
                break  
        else:
            break  
    if subkulit_terakhir:
        subkulit_terakhir =  subkulit_terakhir[1:]    
        if subkulit_terakhir == 's':
            jumlah_orbital = 1
        elif subkulit_terakhir == 'p': 
            jumlah_orbital = 3
        elif subkulit_terakhir == 'd':
            jumlah_orbital = 5
        elif subkulit_terakhir == 'f': 
            jumlah_orbital = 7
        orbital = [[0, 0] for _ in range(jumlah_orbital)]  
        posisi_terakhir = None
        spin_terakhir = None
        for i in range(elektron_terakhir):  
            for pengisian in range(jumlah_orbital):
                if orbital[pengisian][0] == 0: 
                    orbital[pengisian][0] = 1  
                    posisi_terakhir = pengisian  
                    spin_terakhir = "+1/2" 
                    break
            else:
                for pengisian in range(jumlah_orbital):
                    if orbital[pengisian][1] == 0:  
                        orbital[pengisian][1] = 1   
                        posisi_terakhir = pengisian  
                        spin_terakhir = "-1/2"  
                        break
        print(f"Nilai Kuantum Spin = {spin_terakhir}")
Kuantum_Magnetik(10) # contoh nomor atom
