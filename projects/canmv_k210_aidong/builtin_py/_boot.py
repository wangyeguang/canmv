import os, sys, time

sys.path.append('')
sys.path.append('.')

# chdir to "/sd" or "/flash"
devices = os.listdir("/")
if "sd" in devices:
    # os.chdir("/sd")
    sys.path.append('/sd')
# else:
#     os.chdir("/flash")
sys.path.append('/flash')
os.chdir("/flash")
del devices

print("[CanMV] init end") # for IDE
for i in range(200):
    time.sleep_ms(1) # wait for key interrupt(for canmv ide)
del i

# check IDE mode
ide_mode_conf = "/flash/ide_mode.conf"
ide = True
try:
    f = open(ide_mode_conf)
    f.close()
    del f
except Exception:
    ide = False

if ide:
    os.remove(ide_mode_conf)
    from machine import UART
    import lcd
    lcd.init(color=lcd.PINK)
    repl = UART.repl_uart()
    repl.init(1500000, 8, None, 1, read_buf_len=2048, ide=True, from_ide=False)
    sys.exit()
del ide, ide_mode_conf

# detect boot.py
main_py = '''
try:
    import gc, lcd, image
    gc.collect()
    lcd.init()
    loading = image.Image(size=(lcd.width(), lcd.height()))
    loading.draw_rectangle((0, 0, lcd.width(), lcd.height()), fill=True, color=(0, 81, 137))
    info = "Aidong FaceModule"
    loading.draw_string(int(lcd.width()//2 - len(info) * 5), (lcd.height())//4, info, color=(255, 255, 255), scale=2, mono_space=0)
    v = sys.implementation.version
    vers = 'V{}.{}.{} : aidong.ai'.format(v[0],v[1],v[2])
    loading.draw_string(int(lcd.width()//2 - len(info) * 6), (lcd.height())//3 + 20, vers, color=(255, 255, 255), scale=1, mono_space=1)
    lcd.display(loading)
    del loading, v, info, vers
    gc.collect()
finally:
    gc.collect()
'''

flash_ls = os.listdir()
if not "main.py" in flash_ls:
    f = open("main.py", "wb")
    f.write(main_py)
    f.close()
    del f
del main_py

flash_ls = os.listdir("/flash")
try:
    sd_ls = os.listdir("/sd")
except Exception:
    sd_ls = []
if "cover.boot.py" in sd_ls:
    code0 = ""
    if "boot.py" in flash_ls:
        with open("/flash/boot.py") as f:
            code0 = f.read()
    with open("/sd/cover.boot.py") as f:
        code=f.read()
    if code0 != code:
        with open("/flash/boot.py", "w") as f:
            f.write(code)
        import machine
        machine.reset()

if "cover.main.py" in sd_ls:
    code0 = ""
    if "main.py" in flash_ls:
        with open("/flash/main.py") as f:
            code0 = f.read()
    with open("/sd/cover.main.py") as f:
        code = f.read()
    if code0 != code:
        with open("/flash/main.py", "w") as f:
            f.write(code)
        import machine
        machine.reset()

try:
    del flash_ls
    del sd_ls
    del code0
    del code
except Exception:
    pass

import json

config = {
"type": "dock",
  "board_info": {
      'BOOT_KEY': 16,
      'LED_W': 19,
      'LED_R': 20,
      'WIFI_TX': 6,
      'WIFI_RX': 7,
      'WIFI_EN': 8,
      'SPK_CTRL': 18,
      'I2S_WS': 22,
      'I2S_DA': 21,
      'I2S_BCK': 23,
      "LCD_RST":37,
      "SPI0_MISO": 26,
      "SPI0_CLK":  27,
      "SPI0_MOSI": 28,
      "SPI0_CS0":  29,
      "RFID_TX": 24,
      "RFID_RX": 25,
      "PC_RX": 30,
      "PC_TX":31,
      "I2C2_SCL": 33,
      "I2C2_SDA": 34,
      "SPI1_SCLK": 10,
      "SPI1_MOSI": 11,
      "SPI1_MISO": 12,
      "SPI1_CS0": 13,
      "I2C1_SCL": 14,
      "I2C1_SDA": 15,
  },
  "sensor":{
  "cmos_pclk":47,
  "cmos_xclk":46,
  "cmos_href":45,
  "cmos_pwdn":44,
  "cmos_vsync":43,
  "reg_width":8,
  "i2c_num":2,
  "cmos_rst":17,
  "pin_clk":41,
  "pin_sda":42
  }
}

cfg = json.dumps(config)
print(cfg)

try:
    with open('/flash/config.json', 'rb') as f:
        tmp = json.loads(f.read())
    # print(tmp)
    if tmp["type"] != config["type"]:
        raise Exception('config.json no exist')
except Exception as e:
    with open('/flash/config.json', "w") as f:
        f.write(cfg)
    import machine
    machine.reset()
