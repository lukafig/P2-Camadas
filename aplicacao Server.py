from enlace import *
import time
import numpy as np

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
received = []

def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")

        # Sacrificio
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)

        contador = 1
        Recebendo = True

        while Recebendo:
            bufferLen = com1.rx.getBufferLen()
            rxBuffer, nRx = com1.getData(bufferLen)
            com1.rx.clearBuffer()
            time.sleep(1)
            if len(rxBuffer) != 0:
                print("recebeu {}".format(rxBuffer))
                if rxBuffer != start_byte and rxBuffer != end_byte:
                    received.append(rxBuffer)
                    contador+=1
            if rxBuffer  == end_byte:
                Recebendo = False

        print("recebidos{}\n\n".format(received))
        print("recebeu {} bytes".format(contador))


        com1.sendData(contador)
        print(f"enviou {contador} bytes")
            
    
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
