import socket
import pickle
import threading
import random

first_segment = 12
second_segment = 22
third_segment = 36
roulette_range_primary = 1
roulette_range_average = 2
roulette_range_final = 3
exit_answer = 0
twist_answer = 1
error_answer = 3
max_value = 36
min_value = 1
roulette = {1:'red',
            2:'black',
            3:'red',
            4:'black',
            5:'black',
            6:'red',
            7:'black',
            8:'red',
            9:'black',
            10:'red',
            11:'red',
            12:'black',
            13:'red',
            14:'black',
            15:'red',
            16:'black',
            17:'red',
            18:'black',
            19:'black',
            20:'red',
            21:'black',
            22:'red',
            23:'black',
            24:'red',
            25:'black',
            26:'red',
            27:'black',
            28:'red',
            29:'red',
            30:'black',
            31:'red',
            32:'black',
            33:'red',
            34:'black',
            35:'red',
            36:'black',
            }

def generate():
    result = random.randint(min_value, max_value)
    return result

def compare(color,range,result):
    if result <= first_segment:
        roulette_range  = roulette_range_primary
    elif result <= second_segment:
        roulette_range = roulette_range_average
    elif result <= third_segment:
        roulette_range = roulette_range_final
    if roulette_range == range and color == roulette[result]:
        return True
    else:
        return False

class ClientThread(threading.Thread):

    def __init__(self, channel, details):
        self.channel = channel
        self.details = details
        threading.Thread.__init__(self)

    def send_client(self,message):
        channel.send(pickle.dumps(message))

    def accept_client(self):
        accept_data = pickle.loads(channel.recv(1024))
        return accept_data

    def compare_result(self, color, range, result, send_color):
        if compare(color, range, result) == True:
            print(result, send_color)
            self.send_client(True)
            self.send_client(result)
            self.send_client(send_color)
        elif compare(color, range, result) == False:
            print(result, send_color)
            self.send_client(False)
            self.send_client(result)
            self.send_client(send_color)

    def run(self):
        while True:
            print(self.getName())
            if channel != None:
                print ('Принято подключение:', channel)
                comm = self.accept_client()
                print(comm)
                if comm[:3] == '-ex':
                    answer = exit_answer
                    self.send_client(answer)
                    break
                if comm[:3] == '-tw':
                    answer = twist_answer
                    print("Команду принял")
                    self.send_client(answer)
                    result = generate()
                    print(result)
                    send_color = roulette[result]
                    color = self.accept_client()
                    range = self.accept_client()
                    self.compare_result(color,range,result,send_color)
                else:
                    answer = error_answer
                    self.send_client(answer)
                    break

                channel.close()
                print('Закрыто подключение:', channel)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost',8000))
server.listen(6)


while True:
    channel, details = server.accept()
    ClientThread(channel, details).start()