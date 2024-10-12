import pandas as pd

def hitung_statistik_dasar(data, kolom):
    """Hitung statistik dasar untuk sebuah kolom"""
    n = len(data[kolom])
    mean = data[kolom].mean()
    std_dev = data[kolom].std()

def hitung_skewness(data, kolom, n, mean, std_dev):
    """Hitung skewness untuk sebuah kolom"""
    skewness = (1/n) * sum(((data[kolom] - mean) / std_dev) ** 3)
    return skewness

def hitung_kurtosis(data, kolom, n, mean, std_dev):
    """Hitung kurtosis untuk sebuah kolom"""
    kurtosis = (1/n) * sum(((data[kolom] - mean) / std_dev) ** 4) - 3
    return kurtosis

def hitung_skewness_kurtosis(data, kolom):
    """Hitung skewness dan kurtosis untuk sebuah kolom"""
    n, mean, std_dev = hitung_statistik_dasar(data, kolom)
    skewness = hitung_skewness(data, kolom, mean, std_dev)
    kurtosis = hitung_kurtosis(data, kolom, mean, std_dev)
    return skewness, kurtosis

# Membaca data dari file excel
file_path = 'src\SAMPEL NILAI PROJEK ALGORITMA.xlsx'  # Ganti dengan path ke file Anda
data = pd.read_excel(file_path)

# Ganti 'nama_kolom' dengan nama kolom yang ingin dianalisis
kolom_anda = 'Biologi'  # Ganti dengan nama kolom yang sesuai

skewness, kurtosis = hitung_skewness_kurtosis(data, kolom_anda)

print(f'Skewness dari {kolom_anda}: {skewness}')
print(f'Kurtosis dari {kolom_anda}: {kurtosis}')