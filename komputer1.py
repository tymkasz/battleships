import socket
HOST = "127.0.0.1"
PORT = 5010
plansza = [0] * 100
for pole in range(44, 50):
    plansza[pole - 1] = 1
s = socket.socket()
s.bind((HOST, PORT))
s.listen()
print("oczekiwanie na polaczenie...")
conn, addr = s.accept()
print("polaczono")
while True:
    msg = conn.recv(1024).decode()
    print("klient:", msg)
    if msg == "exit":
        break
    dane = msg.split(";")
    pole = int(dane[1])
    wynik = plansza[pole - 1]
    conn.send(f"wynik:{wynik}".encode())
    print(f"wynik:{wynik}")
    msg = input("twoj strzal: ")
    conn.send(msg.encode())
    if msg == "exit":
        break
    wynik = conn.recv(1024).decode()
    print("klient wyslal", wynik)
conn.close()
s.close()