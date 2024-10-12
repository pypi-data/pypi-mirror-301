from PIL import Image, ImageOps

def pencerminanGambar(image_path,output_path,direction="horizontal"):
    """Memantulkan gambar baik secara horizontal atau vertikal.
    
    Args:
        image_path (str): Jalur gambar dari folder.
        output_path (str): Jalur gambar yang akan disimpan.
        direction (str): pencerminan yang diinginkan (antara horizontal atau vertikal).
    """
    
    try:
        # Buka gambar
        image = Image.open(image_path)

        # Pemantulan gambar sesuai arah
        if direction == 'horizontal':
            flipped_image = ImageOps.mirror(image)
        elif direction == 'vertikal':
            flipped_image = ImageOps.flip(image)
        else:
            raise ValueError("Arah yang dimasukkan harus 'horizontal' atau 'vertikal'.")

        # Simpan gambar yang dipantulkan
        flipped_image.save(output_path)
        flipped_image.show()
    except Exception as e:
        return f"Terjadi kesalahan: {e}"
    
# flip_image(
#     "C:\\Users\jpael\OneDrive\Pictures\Ignition Teaser.png", # Buat backslash (\) menjadi double backslash (\\) agar path gambar dapat terbaca
#     "C:\\Users\jpael\OneDrive\Pictures\Ignition Teaser14.png", # Buat backslash (\) menjadi double backslash (\\) agar path gambar dapat terbaca
#     "Horizontal" 
# )
