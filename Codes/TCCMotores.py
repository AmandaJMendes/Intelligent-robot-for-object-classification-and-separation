import machine
import time
import json
import ustruct
uart = machine.UART(2, baudrate=9600, rx=13,tx=12,timeout=10)

dir1 = machine.Pin(23, machine.Pin.OUT)
step1 = machine.Pin(22, machine.Pin.OUT)
dir2 = machine.Pin(21, machine.Pin.OUT)
step2 = machine.Pin(19, machine.Pin.OUT)
angInicial = 0
angFinal = 0
angDesejado = 0
passos = 0
pulsos = 20  # micro segundos
timer = 90 # mili segundos
msg = ""

def controle(motor,angIn,angFi):
  print(motor,angIn,angFi)  
  angDesejado = (angFi - angIn)
  passos = round((200*angDesejado)/360)  
  if (motor == 1):
    if (angFi>angIn):
      angDesejado = (angFi - angIn)
      passos = round((200*angDesejado)/360)
      print(passos)
      dir1.value(0)
      n = 0
      while n <= passos:
        step1.value(1)
        time.sleep_us(pulsos)
        step1.value(0)
        n += 1
        time.sleep_ms(timer)
      return (angIn + passos*1.8)
        
      
    
    elif (angIn>angFi):
      angDesejado = (angIn - angFi)
      passos = round((200*angDesejado)/360)
      dir1.value(1)
      n= 0
      while n <= passos:
        step1.value(1)
        time.sleep_us(pulsos)
        step1.value(0)
        n += 1
        time.sleep_ms(timer)
      return (angIn - passos*1.8)
    else:
        return (angIn + passos*1.8)

  elif (motor == 2):
    if (angFi>angIn):
      angDesejado = (angFi - angIn)
      passos = round((200*angDesejado)/360)
      print(passos)
      dir2.value(0)
      n = 0
      while n <= passos:
        step2.value(1)
        time.sleep_us(pulsos)
        step2.value(0)
        n += 1
        time.sleep_ms(timer)
      return (angIn + passos*1.8)
        
      
    
    elif (angIn>angFi):
      angDesejado = (angIn - angFi)
      passos = round((200*angDesejado)/360)
      dir2.value(1)
      n= 0
      while n <= passos:
        step2.value(1)
        time.sleep_us(pulsos)
        step2.value(0)
        n += 1
        time.sleep_ms(timer)
      return (angIn - passos*1.8)
    else:
        return (angIn + passos*1.8)

while True:
    if uart.any():
        bin_data = uart.readline()
        
        msg = json.loads(bin_data)
        m1 = controle(1, msg["initial"][1], msg["final"][1])
        m2 = controle(2, msg["initial"][2], msg["final"][2])
        envia = (json.dumps({"estimated": [msg["final"][0], m1, m2, msg["final"][3]]})+"\n").encode("utf-8")
        uart.write(envia)
        passos = 0
        
        

        