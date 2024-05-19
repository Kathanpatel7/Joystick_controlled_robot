import socket
import json
import time

def connectETController(ip, port=8055):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        return (True, sock)
    except Exception as e:
        sock.close()
        return (False,)

def disconnectETController(sock):
    if sock:
        sock.close()

def sendCMD(sock, cmd, params=None, id=1):
    if not params:
        params = []
    else:
        params = json.dumps(params)
    sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}\n".format(cmd, params, id)
    try:
        sock.sendall(bytes(sendStr, "utf-8"))
        ret = sock.recv(1024)
        jdata = json.loads(ret.decode("utf-8"))
        if "result" in jdata.keys():
            return (True, json.loads(jdata["result"]), jdata["id"])
        elif "error" in jdata.keys():
            return (False, jdata["error"], jdata["id"])
        else:
            return (False, None, None)
    except Exception as e:
        return (False, None, None)

def jog(sock, a, robot_speed):
    if a == 18:
        sendCMD(sock, "jog", {"index": 0, "speed": robot_speed})
    elif a == 19:
        sendCMD(sock, "jog", {"index": 1, "speed": robot_speed})
    elif a == 20:
        sendCMD(sock, "jog", {"index": 2, "speed": robot_speed})
    elif a == 21:
        sendCMD(sock, "jog", {"index": 3, "speed": robot_speed})
    elif a == 25:
        sendCMD(sock, "jog", {"index": 4, "speed": robot_speed})
    elif a == 24:
        sendCMD(sock, "jog", {"index": 5, "speed": robot_speed})
    elif a == 16:
        sendCMD(sock, "jog", {"index": 6, "speed": robot_speed})
    elif a == 17:
        sendCMD(sock, "jog", {"index": 7, "speed": robot_speed})
    elif a == 15:
        sendCMD(sock, "jog", {"index": 8, "speed": robot_speed})
    elif a == 14:
        sendCMD(sock, "jog", {"index": 9, "speed": robot_speed})
    elif a == 22:
        sendCMD(sock, "jog", {"index": 10, "speed": robot_speed})
    elif a == 23:
        sendCMD(sock, "jog", {"index": 11, "speed": robot_speed})

def main():
    global a
    global robot_speed 
    a = 0
    robot_speed = 10
    robot_ip = "192.168.1.201"
    
    conSuc, robot_sock = connectETController(robot_ip)
    if not conSuc:
        print("Failed to connect to the robot.")
        return
    
    sendCMD(robot_sock, "set_servo_status", {"status": 1})
    suc, result ,id=sendCMD(robot_sock, "setCurrentCoord", {"coord_mode":1})
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12349
    client_socket.connect((host, port))
    
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            a = int(data.decode('utf-8'))
            print(f"Received: {a}")
            
            if a == 5 and robot_speed > 0:
                if robot_speed > 10:# Decrease speed by 5% if button 5 is pressed
                    robot_speed -= 5
                else:
                    robot_speed -= 2
                print("Speed decreased to:", robot_speed)
            elif a == 6 and robot_speed < 100:  # Increase speed by 5% if button 6 is pressed
                robot_speed += 5
                print("Speed increased to:", robot_speed)
            else:
                jog(robot_sock, a, robot_speed)
                
            a = 0  # Clear the command after sending it
            
    except KeyboardInterrupt:
        print("Client stopped.")
    finally:
        client_socket.close()
        disconnectETController(robot_sock)

if __name__ == "__main__":
    main()
