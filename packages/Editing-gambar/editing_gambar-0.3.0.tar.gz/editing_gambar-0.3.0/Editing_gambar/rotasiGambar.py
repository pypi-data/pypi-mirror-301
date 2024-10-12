from PIL import Image

def rotasiGambar(input_path,output_path,angle):
    """Melakukan rotasi gambar berdasarkan sudut yang ditentukan dan menyimpannya.
    
    Args:
        input_path (str): Jalur file gambar input yang akan dirotasi.
        output_path (str): Jalur file tempat gambar hasil rotasi akan disimpan.
        angle (float): Sudut rotasi dalam derajat (positif untuk rotasi searah jarum jam, negatif untuk berlawanan).
    """
    try:
        # Membuka gambar
        image = Image.open(input_path)
        # Melakukan rotasi
        rotated_image = image.rotate(angle, expand=True)
        # Menyimpan gambar hasil rotasi
        rotated_image.save(output_path)
        # Menunjukkan gambar yang telah di rotasi
        rotated_image.show(output_path)
    except Exception as e:
        return f"Terjadi kesalahan: {e}"

# rotate_image(
#     "C:\\Users\jpael\OneDrive\Pictures\Ignition Teaser.png", # Buat backslash (\) menjadi double backslash (\\) agar path gambar dapat terbaca
#     "C:\\Users\jpael\OneDrive\Pictures\Ignition Teaser14.png", # Buat backslash (\) menjadi double backslash (\\) agar path gambar dapat terbaca
#     90 # Masukkan angle rotasi dalam bentuk int atau float
# )
