from PIL import Image

def hitam_putih(input_path,output_path):
    """Mengubah gambar menjadi hitam putih.
    
    Args:
        input_path (str): Jalur gambar dari folder.
        output_path (str): Jalur gambar yang akan disimpan.
    """
    
    # Buka gambar
    try:
        image = Image.open(input_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return
    
    # Ubah gambar ke grayscale
    grayscale_image = image.convert('L')

    # Simpan gambar grayscale
    grayscale_image.save(output_path)
    print(f"Gambar grayscale telah disimpan di: {output_path}")

    # Menunjukkan hasil gambar
    grayscale_image.show()

# convert_image_to_grayscale(
#     "C:\\Users\jpael\OneDrive\Pictures\Ignition Teaser.png", # Buat backslash (\) menjadi double backslash (\\) agar path gambar dapat terbaca
#     "C:\\Users\jpael\OneDrive\Pictures\Ignition Teaser14.png" # Buat backslash (\) menjadi double backslash (\\) agar path gambar dapat terbaca
# )
