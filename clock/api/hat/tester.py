import unicorn

led = unicorn.UnicornHat(32,16)

for i in range(16*32):
    x = i % 32
    y = i // 32
    led.set_pixel(x,y, 10, 200, 30)
    if i%2 == 0:
        led.show()