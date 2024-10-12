from PIL import Image     

def pemotonganGambar(Input_path,Output_path,left,top,right,bottom):
    """Memotong gambar sesuai dengan koordinat yang ditentukan oleh pengguna dan menyimpannya.
    
    Args:
        Input_path (str): Jalur gambar dari folder.
        Output_path (str): Jalur gambar yang akan disimpan.
        left (int): Koordinat batas kiri gambar yang ingin dipotong (dalam piksel).
        top (int): Koordinat batas atas gambar yang ingin dipotong (dalam piksel).
        right (int): Koordinat batas kanan gambar yang ingin dipotong (dalam piksel).
        bottom (int): Koordinat batas bawah gambar yang ingin dipotong (dalam piksel).
    """
    try:
        # Membuka file gambar
        image = Image.open(Input_path)
        cropped_image = image.crop((left, top, right, bottom)) # Memotong gambar sesuai koordinat kiri atas dan kanan bawah sehingga terbentuk segii empat
        # Menyimpan hasil di jalur output
        cropped_image.save(Output_path)
        cropped_image.show() # Menunjukkan hasil gambar yang telah dipotong
        return f"Gambar berhasil dipotong dan disimpan di {Output_path}" # Akhir dari program
    except Exception as e:
        return f"Terjadi kesalahan: {e}"

# ukuran_gambar(
#               "C:\\Users\jpael\OneDrive\Pictures\Ignition Teaser.png", # Buat backslash (\) menjadi double backslash (\\) agar path gambar dapat terbaca
#               "C:\\Users\jpael\OneDrive\Pictures\Ignition Teaser14.png", # Buat backslash (\) menjadi double backslash (\\) agar path gambar dapat terbaca
#               0,0,2000,2000 # parameter untuk batasan pemotongan gambar
# )


