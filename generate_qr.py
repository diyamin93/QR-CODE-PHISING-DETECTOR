import qrcode


safe_url = "https://www.google.com"
phishing_url = "http://verify-bank-login-secure.com"

# Safe QR

safe_img = qrcode.make(safe_url)
safe_img.save("test_qr_codes/safe_qr.png")

# Phishing QR

phishing_img = qrcode.make(phishing_url)
phishing_img.save("test_qr_codes/phishing_qr.png")

print("QR Codes Generated Successfully")