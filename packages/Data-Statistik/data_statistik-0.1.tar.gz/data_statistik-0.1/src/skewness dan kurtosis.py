def hitung_skewness_kurtosis(data, nama_kolom):
    try:
        # Menghitung statistik dasar
        n = len(self.get_data(nama_kolom))
        mean = self.mean(nama_kolom)
        std_dev = self.simpangan_baku(nama_kolom)

        # Menghitung skewness
        skewness = (1/n) * sum(((data[kolom] - mean) / std_dev) ** 3)

        # Menghitung kurtosis
        kurtosis = (1/n) * sum(((data[kolom] - mean) / std_dev) ** 4) - 3

        return skewness, kurtosis
    except:
        print("Kolom atau nilai tidak valid!")

# Membaca data dari file excel
file_path = 'src\SAMPEL NILAI PROJEK ALGORITMA.xlsx'  # Ganti dengan path ke file Anda
data = pd.read_excel(file_path)

# Ganti 'nama_kolom' dengan nama kolom yang ingin dianalisis
kolom_anda = 'Biologi'  # Ganti dengan nama kolom yang sesuai

skewness, kurtosis = hitung_skewness_kurtosis(data, kolom_anda)

print(f'Skewness dari {kolom_anda}: {skewness}')
print(f'Kurtosis dari {kolom_anda}: {kurtosis}')