def cari_nama_unsur(nomor_atom):
# Mencari nama dan golongan unsur kimia berdasarkan nomor atom
    if nomor_atom == 1:
        return "1A : Hidrogen (H)"
    elif nomor_atom == 3:
        return "1A : Litium (Li)"
    elif nomor_atom == 11:
        return "1A : Sodium (Na)"
    elif nomor_atom == 19:
        return "1A : Kalium (K)"
    elif nomor_atom == 37:
        return "1A : Rubidium (Rb)"
    elif nomor_atom == 55:
        return "1A : Scesium (Cs)"
    elif nomor_atom == 87:
        return "1A : Fransium (Fr)"
    elif nomor_atom == 4:
        return "2A : Berilium (Be)"
    elif nomor_atom == 12:
        return "2A : Magnesium (Mg)"
    elif nomor_atom == 20:
        return "2A : Kalsium (Ca)"
    elif nomor_atom == 38:
        return "2A : Stronsium (Sr)"
    elif nomor_atom == 56:
        return "2A : Barium (Ba)"
    elif nomor_atom == 88:
        return "2A : Radium (Ra)"
    elif nomor_atom == 5:
        return "3A : Boron (B)"
    elif nomor_atom == 13:
        return "3A : Aluminium (Al)"
    elif nomor_atom == 31:
        return "3A : Gallium (Ga)"
    elif nomor_atom == 49:
        return "3A : Indium (In)"
    elif nomor_atom == 81:
        return "3A : Thallium (Ti)"
    elif nomor_atom == 6:
        return "4A : Karbon (C)"
    elif nomor_atom == 14:
        return "4A : Silicon (Si)"
    elif nomor_atom == 32:
        return "4A : Germanium (Ge)"
    elif nomor_atom == 50:
        return "4A : Timah (Sn)"
    elif nomor_atom == 82:
        return "4A : Timbal (Pb)"
    elif nomor_atom == 7:
        return "5A : Nitrogen (N)"
    elif nomor_atom == 15:
        return "5A : Fosfor (P)"
    elif nomor_atom == 33:
        return "5A : Arsen (As)"
    elif nomor_atom == 51:
        return "5A : Antimon (Sb)"
    elif nomor_atom == 83:
        return "5A : Bismut (Bi)"
    elif nomor_atom == 8:
        return "6A : Oksigen (O)"
    elif nomor_atom == 16:
        return "6A : Sulfur (S)"
    elif nomor_atom == 34:
        return "6A : Selenium (Se)"
    elif nomor_atom == 52:
        return "6A : Tellurium (Te)"
    elif nomor_atom == 84:
        return "6A : Polonium (Po)"
    elif nomor_atom == 9:
        return "7A : Fluor (F)"
    elif nomor_atom == 17:
        return "7A : Klor (Cl)"
    elif nomor_atom == 35:
        return "7A : Brom (Br)"
    elif nomor_atom == 53:
        return "7A : Iodin (I)"
    elif nomor_atom == 85:
        return "7A : Astatin (At)"
    elif nomor_atom == 2:
        return "8A : Helium (He)"
    elif nomor_atom == 10:
        return "8A : Neon (Ne)"
    elif nomor_atom == 18:
        return "8A : Argon (Ar)"
    elif nomor_atom == 36:
        return "8A : Kripton (Kr)"
    elif nomor_atom == 54:
        return "8A : Xenon (Xe)"
    elif nomor_atom == 86:
        return "8A : Radon (Rn)"
    else:
        return "Nomor atom tidak ditemukan."

# Daftar nomor atom yang ingin dicari
nomor_atom_list = []

for nomor_atom in nomor_atom_list:
    nama_unsur = cari_nama_unsur(nomor_atom)

