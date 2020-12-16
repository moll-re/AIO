import unicorn

led = unicorn.UnicornHat(32,16)
r = 0
b = 0
for i in range(16*32):
    x = i % 32
    y = i // 32
    r += (x % 16 == 0)*5
    b+= (y % 16 == 0)*5
    led.set_pixel(x,y, r, 200, b)
    if i%2 == 0:
        led.show()