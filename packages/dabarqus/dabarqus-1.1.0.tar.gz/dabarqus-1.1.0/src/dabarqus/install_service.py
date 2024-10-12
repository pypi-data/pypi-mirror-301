import os
import platform
import subprocess
import sys
import requests
from tqdm import tqdm
import py7zr
import shutil
import zipfile
import site
import time

GITHUB_API_URL = "https://api.github.com/repos/electricpipelines/barq/releases/latest"

def check_cuda_support():
    try:
        # Try to run nvidia-smi
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        # nvidia-smi not found, CUDA is not available
        return False

def get_latest_release_info():
    try:
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        release_data = response.json()
        assets = release_data['assets']
        
        system = platform.system().lower()
        
        if system == 'darwin':
            metal_support = subprocess.run(["uname", "-m"], 
                                           capture_output=True, text=True).stdout
            use_metal = "arm64" in metal_support
            
            for asset in assets:
                if "macos" in asset['name'].lower() and ".zip" in asset['name'].lower():
                        return asset

                    # if use_metal and "metal" in asset['name'].lower():
                    #     return asset
                    # elif not use_metal and "metal" not in asset['name'].lower():
                    #     return asset
        elif system == 'windows' or system == 'linux':
            cuda_support = check_cuda_support()
            for asset in assets:
                if system in asset['name'].lower() and ".zip" in asset['name'].lower():
                    if cuda_support and "cublas" in asset['name'].lower():
                        return asset
                    elif not cuda_support and "cublas" not in asset['name'].lower():
                        return asset
        
        raise ValueError(f"No suitable release found for {system}")
    except requests.RequestException as e:
        print(f"Error fetching release information: {e}")
        sys.exit(1)
def format_size(size_bytes):
    """Convert size in bytes to a human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} GB"

def get_package_directory():
    # Get the site-packages directory
    if hasattr(sys, 'real_prefix') or sys.prefix != sys.base_prefix:  # We're in a virtualenv
        # Use sysconfig to get the correct scheme for virtual environments
        import sysconfig
        return sysconfig.get_path('purelib')
    else:
        return site.getsitepackages()[0]

def check_dabarqus_health():
    try:
        response = requests.get('http://localhost:6568/health', timeout=5)
        return response.json()
    except requests.RequestException:
        return None

def stop_dabarqus_service():
    system = platform.system().lower()
    if system == "windows":
        subprocess.run(["barq", "service", "stop"], check=True)
    else:
        subprocess.run(["barq", "service", "stop"], check=True)
    print("Waiting for Dabarqus service to stop...")
    time.sleep(5)  # Give some time for the service to stop

def download_and_extract_dabarqus():
    # system = platform.system().lower()
    # machine = platform.machine()

    asset_info = get_latest_release_info()
    url = asset_info['browser_download_url']
    size = asset_info['size']
    formatted_size = format_size(size)

    archive_filename = url.split("/")[-1]
    extract_dir = "dabarqus_extracted"

    print(f"Latest Dabarqus release found: {asset_info['name']}")
    print(f"File size: {formatted_size}")
    
    user_input = input("Do you want to download and install this version? (y/n): ")
    if user_input.lower() != 'y':
        print("Installation aborted.")
        sys.exit(0)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192

    with open(archive_filename, "wb") as file, tqdm(
        desc=archive_filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(block_size):
            size = file.write(data)
            progress_bar.update(size)

    print("Extracting archive...")
    if archive_filename.endswith(".zip"):
        with zipfile.ZipFile(archive_filename, 'r') as z:
            z.extractall(path=extract_dir)
    else:
        with py7zr.SevenZipFile(archive_filename, mode='r') as z:
            z.extractall(path=extract_dir)


    install_dir = os.path.join(get_package_directory(), 'dabarqus')

    print(f"Installing Dabarqus to {install_dir}...")
    
    if os.path.exists(install_dir):
        shutil.rmtree(install_dir)
    
    os.makedirs(install_dir, exist_ok=True)
    
    for item in os.listdir(extract_dir):
        s = os.path.join(extract_dir, item)
        d = os.path.join(install_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks=False, ignore=None)
        else:
            shutil.copy2(s, d)

    bin_dir = os.path.join(install_dir, "bin")
    if os.path.exists(bin_dir):
        for file in os.listdir(bin_dir):
            file_path = os.path.join(bin_dir, file)
            if os.path.isfile(file_path):
                os.chmod(file_path, 0o755)

    print(f"Dabarqus installed to {install_dir}")
    
    shutil.rmtree(extract_dir)
    os.remove(archive_filename)
    
    system = platform.system().lower()
    executable_name = "barq.exe" if system == "windows" else "barq"
    executable_path = os.path.join(install_dir, "bin", executable_name)
    if not os.path.exists(executable_path):
        executable_path = os.path.join(install_dir, executable_name)
    
    if not os.path.exists(executable_path):
        raise FileNotFoundError(f"Could not find {executable_name} in installed files")

    return executable_path

def install_service(executable_path):
    system = platform.system().lower()
    if system == "linux":
        # Linux service installation
        pass
    elif system == "darwin":
        # macOS service installation
        pass
    elif system == "windows":
        # Windows service installation
        subprocess.run([executable_path, "service", "uninstall"], check=True)
        subprocess.run([executable_path, "service", "install"], check=True)
    else:
        print(f"Unsupported operating system: {system}")
        sys.exit(1)

def main():
    health_status = check_dabarqus_health()
    
    if health_status and health_status.get('status') == 'ok':
        print("Dabarqus is currently running.")
        user_input = input("Do you want to stop Dabarqus and continue with the installation? (y/n): ")
        if user_input.lower() != 'y':
            print("Installation aborted.")
            return
        stop_dabarqus_service()
    
    executable_path = download_and_extract_dabarqus()
    install_service(executable_path)
    print("Dabarqus executable downloaded and service installed.")

if __name__ == "__main__":
    main()