import subprocess
import os
import hashlib


def calculate_md5(file_path):
    """Dosyanın MD5 hash'ini hesapla"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        print(f"Hata: {file_path} dosyası bulunamadı")
        return None


def generate_md5sums(root_dir, output_file="DEBIAN/md5sums"):
    """Belirtilen dizindeki tüm dosyalar için md5sums dosyası oluştur"""
    md5_entries = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # DEBIAN dizinindeki dosyaları dahil etme
            if "DEBIAN" in os.path.relpath(file_path, root_dir):
                continue

            md5_hash = calculate_md5(file_path)
            if md5_hash:
                relative_path = os.path.relpath(file_path, root_dir)
                md5_entries.append(f"{md5_hash}  {relative_path}")

    md5sums_path = os.path.join(root_dir, output_file)
    os.makedirs(os.path.dirname(md5sums_path), exist_ok=True)

    with open(md5sums_path, "w") as f:
        for entry in sorted(md5_entries):
            f.write(entry + "\n")

    print(f"md5sums dosyası oluşturuldu: {md5sums_path}")


def extract_deb_package(deb_file, output_dir):
    subprocess.run(f"rm -rf {output_dir}", shell=True)  # Eski dizini temizle
    # Çıkarma işlemi için output_dir dizinini oluştur
    os.makedirs(output_dir, exist_ok=True)
    deb = f"{output_dir}/DEBIAN"
    os.makedirs(deb, exist_ok=True)

    # dpkg-deb komutunu çalıştır
    subprocess.run(["dpkg-deb", "-x", deb_file, output_dir], check=True)
    subprocess.run(["dpkg-deb", "-e", deb_file, deb], check=True)

    print(f"{deb_file} başarıyla {output_dir} dizinine çıkarıldı.")


def create_deb_package(output_dir, new_deb_file):
    # Yeni deb paketini oluştur
    generate_md5sums(output_dir, "DEBIAN/md5sums")
    subprocess.run(["dpkg-deb", "--build", output_dir, new_deb_file], check=True)
    print(f"{output_dir} dizininden {new_deb_file} başarıyla oluşturuldu.")



if __name__ == "__main__":


    deb_file = "base-files_12.4+pardus23.4.1_all.deb"  # Çıkarılacak deb dosyası
    output_dir = "base-files"  # Çıkarılan içerik için dizin
    new_deb_file = (
        "base-files_12.4+z-bismih25.1_all.deb"
    )
    
    # Deb paketini parçalara ayır
    # extract_deb_package(deb_file, output_dir)
    create_deb_package(output_dir, new_deb_file)
