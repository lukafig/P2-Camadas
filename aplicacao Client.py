from enlace import *
import time
import numpy as np
from random import randint, choice

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM8"                  # Windows(variacao de)

start_byte = b'\x12'
end_byte = b'\x13'

n = randint(10,30)
comandos = [b'\x00\x00\x00\x00',
            b'\x00\x00\xFF\x00',
            b'\xFF\x00\x00',
            b'\x00\xFF\x00',
            b'\x00\x00\xFF',
            b'\x00\xFF',
            b'\xFF\x00',
            b'\x00',
            b'\xFF']

""" comandos = [bytes.fromhex("00 00 00 00"),
            bytes.fromhex("00 00 FF 00"),
            bytes.fromhex("FF 00 00"),
            bytes.fromhex("00 FF 00"),
            bytes.fromhex("00 00 FF"),
            bytes.fromhex("00 FF"),
            bytes.fromhex("FF 00"),
            bytes.fromhex("00"),
            bytes.fromhex("FF")] """



def main():

    try:
        contador = 0
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")

        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
       


        txBuffer = []     
        len_escolhido = []

        for i in range(n):
            escolhido = choice(comandos)
            txBuffer.append(escolhido)
            len_escolhido.append(len(escolhido))

        txLen = len(txBuffer)
            

        #txBuffer = b'\x12\x13\xAA'  #isso é um array de bytes
        print("{} comandos vão ser enviados" .format(n))
        msg = bytearray([])
        for i in txBuffer:
            msg += i
            msg += b'\x14'
        print("")
        print("Meu array de bytes tem tamanho {}" .format(len(msg)+2))


        com1.sendData(np.asarray(start_byte)) 
             
    
        com1.sendData(np.asarray(msg))
        print(msg)

        com1.sendData(np.asarray(end_byte))
        #print("enviou o end_byte")
        print("")
        print("Enviando os comandos")
        print("")

        """"""""""""""""""""""""""""""""""""""""""""""""
        while com1.tx.getIsBussy():
            pass

        
        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))
        ''''''''''''''''''''''''''''''''''''''''''''
        TimeOut_Status = False
        timeout = time.time()
        print('Esperando resposta do server...')
        print('')
        while (time.time() - timeout < 5) and not TimeOut_Status:
            if com1.rx.getBufferLen() > 0:
                TimeOut_Status = True
                rxBuffer, nRx = com1.getData(1)
                msg += rxBuffer

        
        if TimeOut_Status == False:
            print("ERRO: TIMEOUT")
        else:
            recebidos = int.from_bytes(msg, byteorder='little')

            print(f"O servidor informou que recebeu {recebidos} comandos")
            if recebidos != len(msg)+2:
                print(f"ERRO: Foram enviados {len(msg)+2} e recebidos {recebidos}")
            if recebidos == len(msg)+2:
                print("SUCESSO")
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
