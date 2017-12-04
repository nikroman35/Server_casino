import pickle
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8000))

while True:
    ques = input("Введите ключ")
    client.send(pickle.dumps(ques))
    answer = pickle.loads(client.recv(1024))
    if answer == 0:
        print("Выход")
        break
    if answer == 1:
        color = input("Выберите цвет")
        client.send(pickle.dumps(color))
        print("Выберите промежуток "
              "1 если от 1 до 12" ','
              "2 если от 13 до 22" ','
              "3 если от 23 до 36")
        range = int(input("Промежуток = "))
        client.send(pickle.dumps(range))
        print("Крутим бабабан")
    if answer == 3:
        print("Ошибка ввода ключа")
        continue

    receive_result = pickle.loads(client.recv(1024))
    receive_number = pickle.loads(client.recv(1024))
    receive_color = pickle.loads(client.recv(1024))

    if receive_result == True:
        print('Выпало число ',receive_number)
        print('Цвет', receive_color)
        print('Победа')
        break
    elif receive_result == False:
        print('Выпало число ', receive_number)
        print('Цвет', receive_color)
        print('Неудача')
        break
client.close()
