import socket
HOST = "127.0.0.1"
PORT = 5010
plansza = [0] * 100
for pole in range(44, 50):
    plansza[pole - 1] = 1
s = socket.socket()
s.connect((HOST, PORT))
print("polaczono")
while True:
    msg = input("twoj strzal: ")
    s.send(msg.encode())
    if msg == "exit":
        break
    wynik = s.recv(1024).decode()
    print(wynik)
    msg = s.recv(1024).decode()
    print("serwer:", msg)
    if msg == "exit":
        break
    dane = msg.split(";")
    pole = int(dane[1])
    wynik = plansza[pole - 1]
    s.send(f"wynik:{wynik}".encode())
    print(f"wynik:{wynik}")
s.close()