from PIL import Image, ImageDraw, ImageFont

def penambahanTeks(input_path,output_path,teks,left,top,nama_font,font_size,warna_font):
    """Menambahkan teks ke gambar pada koordinat yang ditentukan dan menyimpannya.
    
    Args:
        Input_path (str): Jalur file gambar input.
        output_path (str): Jalur file untuk menyimpan gambar dengan teks yang ditambahkan.
        teks (str): Teks yang akan ditambahkan pada gambar.
        left (int): Posisi horizontal (kiri) teks dalam piksel.
        top (int): Posisi vertikal (atas) teks dalam piksel.
        nama_font (str): Nama file font (TrueType) yang akan digunakan untuk teks.
        font_size (int): Ukuran font teks.
        warna_font (str): Warna teks yang akan ditambahkan dalam format heksadesimal atau nama warna yang didukung.
    """
    # Membuka file gambar
    input_path = Image.open(input_path)
    # Menentukan posisi teks
    posisi = (left, top)
    # Mengolah gambar
    gambar = ImageDraw.Draw(input_path)
    # Mengolah nama font dan ukuran teks
    font = ImageFont.truetype(nama_font, font_size)
    # Menempatkan posisi dan warna teks
    gambar.text(posisi, teks, fill=warna_font, font=font)
    input_path.save(output_path) # Menyimpan hasil di output
    input_path.show(output_path) # Menunjukkan hasil gambar yang telah ditambahkan teks

# tambahkan_teks(
#     "C:\\Users\jpael\OneDrive\Pictures\Ignition Teaser.png", # Buat backslash (\) menjadi double backslash (\\) agar path gambar dapat terbaca
#     "C:\\Users\jpael\OneDrive\Pictures\Ignition Teaser14.png", # Buat backslash (\) menjadi double backslash (\\) agar path gambar dapat terbaca
#     "Jean Patra Paeloran", #Tambahkan teks string
#     3000,1500, # Masukkan koordinat teks
#     "times.ttf", # font yang tersedia: "arial.ttf", "ALGER.TTF", "calibri.ttf", "cambriab.ttf", "times.ttf"
#     500, # Masukkan ukuran font
#     "red" # Masukkan warna font dalam bahasa inggris
# )
