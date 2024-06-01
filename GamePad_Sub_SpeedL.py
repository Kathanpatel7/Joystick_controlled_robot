#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 02:38:10 2024

@author: kathanpatel
"""

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
        
def set_v(sock, a, current_pose,robot_speed,omega):

        # Set the system V variable value
        
        #print (suc, result )
        if a == 18:
            current_pose[0] = robot_speed
            print("this is current_pose = ",current_pose)
        elif a == 19:
            current_pose[0] = -robot_speed
            print("this is current_pose = ",current_pose)
        elif a == 20:
            current_pose[1] = robot_speed
            print("this is current_pose = ",current_pose)
        elif a == 21:
            current_pose[1] = -robot_speed
            print("this is current_pose = ",current_pose)
        elif a == 24:
            current_pose[2] = robot_speed
            print("this is current_pose = ",current_pose)
        elif a == 25:
            current_pose[2] = -robot_speed
            print("this is current_pose = ",current_pose)
        elif a == 16:
            current_pose[3] = robot_speed
            print("this is current_pose = ",current_pose)
        elif a == 17:
            current_pose[3] = -robot_speed
            print("this is current_pose = ",current_pose)
        elif a == 15:
            current_pose[4] = robot_speed
            print("this is current_pose = ",current_pose)
        elif a == 14:
            current_pose[4] = -robot_speed
            print("this is current_pose = ",current_pose)
        elif a == 22:
            current_pose[5] = robot_speed
            print("this is current_pose = ",current_pose)
        elif a == 23:
            current_pose[5] = -robot_speed
            
            print("this is current_pose = ",current_pose)
        return current_pose

def main():
    global a
    global robot_speed 
    global omega
    global current_pose
    a = 0
    omega = 0.02 
    robot_speed = 10
    current_pose = [0,0,0,0,0,0]
    robot_ip = "192.168.1.200"
    
    conSuc, robot_sock = connectETController(robot_ip)
    if not conSuc:
        print("Failed to connect to the robot.")
        return
    
    sendCMD(robot_sock, "set_servo_status", {"status": 1})
    #Set the loop mode to single loop
    suc , resultt , id = sendCMD(robot_sock, "setCycleMode",{"cycle_mode":2})
    suc, result ,id=sendCMD(robot_sock, "setCurrentCoord", {"coord_mode":1})
    
    if conSuc:
        suc, result_pose, id = sendCMD(robot_sock, "get_tcp_pose", {"coordinate_num": 2, "tool_num": 4})
        print(result_pose)
        #current_pose = result_pose
        suc, result , id = sendCMD(robot_sock, "setSysVarV", {"addr": 1,"pose": current_pose})
        
    #suc, result , id = sendCMD(robot_sock, "run")
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12334
    client_socket.connect((host, port))
    
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            a = int(data.decode('utf-8'))
            print(f"Received: {a}")
            
            if a != 0:
                suc, check_1 ,id=sendCMD(robot_sock,"getSysVarI",{"addr":10})
                #suc, run , id = sendCMD(robot_sock, "run")
            
                if a == 5 and robot_speed > 0 and omega > -3.14:
                    if robot_speed > 10:# Decrease speed by 5% if button 5 is pressed
                        robot_speed -= 0.05
                        omega -= 0.02
                        
                    else:
                        robot_speed -= 0.05
                        omega -= 0.2
                    print("Speed decreased to:", robot_speed)
                    
                    
                elif a == 6 and robot_speed < 100 and omega < 3.14:  # Increase speed by 5% if button 6 is pressed
                    robot_speed += 2
                    omega += 0.02
                    print("Speed increased to:", robot_speed)
                    
                
              
                else:
                    #jog(robot_sock, a, robot_speed)
                    print(a)
                    current_pose = set_v(robot_sock, a, current_pose,robot_speed,omega)
                    print("this is current pose =",current_pose)
                    suc, result, id = sendCMD(robot_sock, "moveBySpeedl", {"v": current_pose, "acc": 50, "arot": 10, "t": 0.1})
                    #time.sleep(0.5)
                    print(suc, result, id)
                    print("running !!!")
                    
                
            
            elif a == 0:
                suc, result ,id=sendCMD(robot_sock,"stopl",{"acc":120})
                current_pose = [0,0,0,0,0,0]
            #suc, current_pose, id = sendCMD(robot_sock, "get_tcp_pose", {"coordinate_num": 2, "tool_num": 4})
            #suc, result , id = sendCMD(robot_sock, "setSysVarV", {"addr": 1,"pose": current_pose})
              
                    
                    
                    
            a = 0  # Clear the command after sending it
            #suc, result , id = sendCMD(robot_sock, "pause")

            
    except KeyboardInterrupt:
        print("Client stopped.")
    finally:
        client_socket.close()
        disconnectETController(robot_sock)

if __name__ == "__main__":
    main()
