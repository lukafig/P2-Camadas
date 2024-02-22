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
        n = randint(10,30)
        comandos = [("00 00 00 00"),
                    ("00 00 FF 00"),
                    ("FF 00 00"),
                    ("00 FF 00"),
                    ("00 00 FF"),
                    ("00 FF"),
                    ("FF 00"),
                    ("00"),
                    ("FF")]
        
        len_escolhido = []

        for i in range(n):
            escolhido = choice(comandos)
            txBuffer.append(escolhido)
            len_escolhido.append(len(escolhido))

        txLen = len(txBuffer)
            

        #txBuffer = b'\x12\x13\xAA'  #isso é um array de bytes

        print("meu array de bytes tem tamanho {}" .format(txLen))

        com1.sendData(np.asarray(start_byte))

        com1.sendData(np.asarray(txBuffer))

        com1.sendData(np.asarray(end_byte))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
        
        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))

        TimeOut_Status = False
        timeout = time.time() + 5
        while time.time()<timeout:
            if com1.rx.getBufferLen()>0:
                rxBuffer, nRx = com1.getData(txLen)


                if rxBuffer == n:
                    print(f"recebeu {rxBuffer}, acabou a transmissão")
                    TimeOut_Status = True
                    break
                else:
                    if rxBuffer != n:
                        print("ERRO: NAO RECEBEU O QUE ESPERAVA")
                        print(f"esperava {n} e recebeu {rxBuffer}")
                        TimeOut_Status = True

        
        if TimeOut_Status == False:
            print("ERRO: TIMEOUT")
            print("Passou dos 5 segundos e não recebeu o que esperava")
            print(f"esperava {n} e recebeu {rxBuffer}")
    
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
