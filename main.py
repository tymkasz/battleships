from random import randint
import battleship_bot
def nowa_plansza():
    plansza = [[0] * 10 for _ in range(10)]
    statki = [4, 3, 2]
    wszystkie_pozycje = []

    for dlugosc in statki:
        postawiono = 0
        while postawiono == 0:
            pionowo = randint(0, 1)

            if pionowo == 0:
                statekx = randint(0, 10 - dlugosc)
                stateky = randint(0, 9)
            else:
                statekx = randint(0, 9)
                stateky = randint(0, 10 - dlugosc)
            kolizja = 0
            for i in range(dlugosc):
                cur_x = statekx + (i if pionowo == 0 else 0)
                cur_y = stateky + (i if pionowo == 1 else 0)

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx = cur_x + dx
                        ny = cur_y + dy
                        if 0 <= nx <= 9 and 0 <= ny <= 9:
                            if plansza[ny][nx] == 1:
                                kolizja = 1

            if kolizja == 0:
                statek_poz = []
                for i in range(dlugosc):
                    cur_x = statekx + (i if pionowo == 0 else 0)
                    cur_y = stateky + (i if pionowo == 1 else 0)

                    plansza[cur_y][cur_x] = 1
                    statek_poz += [cur_x, cur_y]

                wszystkie_pozycje.append(statek_poz)
                postawiono = 1

    return plansza, wszystkie_pozycje

def strzal(plansza, statki, x, y):
    if plansza[y][x] == 0:
        plansza[y][x] = -1
        return "pudło"

    elif plansza[y][x] == 1:
        plansza[y][x] = 2  # 2  trafiony segment
        for statek in statki:
            for i in range(0, len(statek), 2):
                if statek[i] == x and statek[i + 1] == y:
                    statek[i] = -1 # zatopione
                    statek[i + 1] = -1
            if all(c == -1 for c in statek):
                statki.remove(statek)
                return "zatopiony"

        return "trafiony"

    else:
        return "pudło"

def koniec_gry(statki):
    if len(statki) == 0:
        return True
    else:
        return False

# plansza, poz = nowa_plansza()
# for i in range(200):
#     # x = int(input("Podaj x"))-1
#     # y = int(input("Podaj y"))-1
#     for i in range(10):
#         for j in range(10):
#             print(strzal(plansza, poz, i, j))
#     if(koniec_gry(poz)):
#         print("koniec lol")
#         break

plansza_player, poz_player = nowa_plansza()
plansza_bot, poz_bot = nowa_plansza()
bot = battleship_bot.BotBattleships(10)

while 1:
    x = int(input("Podaj x"))-1
    y = int(input("Podaj y"))-1
    wynik = strzal(plansza_bot, poz_bot, x, y)

    c, r = randint(1,8)
    na_planszy = bot.on_board(c, r)

