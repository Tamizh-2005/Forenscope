from generate_report import verify_image_hash
image_path = "/home/pi/forenscope/usb/session_20240711/device_image.img"
hash_file = "/home/pi/forenscope/usb/session_20240711/hash.txt"

result = verify_image_hash(image_path, hash_file)
print(result)
