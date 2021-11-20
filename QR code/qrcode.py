import qrcode

data="https://google.com"
img= qrcode.make(data)

img.save("image.png")