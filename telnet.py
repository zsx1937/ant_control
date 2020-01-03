# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: lovesatomi.xyz

import sys
import telnetlib
import time
import json


###############################################################
# Function define
###############################################################
def init_telnet(host_, port_):
    tn = telnetlib.Telnet(host_, int(port_))
    return tn


def close_telnet(tn):
    tn.close()


def read_files(path):
    f = open(path, 'r', encoding='utf-8')
    if f:
        print("Read files success")
    else:
        print("Read files fail")
    content = f.read()
    commands = content.split('\n')
    f.close()
    return commands


def write_files(path, results):
    f = open(path, 'w', encoding='utf-8')
    for result in results:
        f.write(str(result) + '\n')
    f.close()
    print("Write files success")


# process single command,for example, RS 1 1
def process_command(tn, command):
    tn.write(bytes(command, encoding='utf8'))
    result = str()
    a = []
    # get result
    while True:
        b, c, d = tn.expect(a, timeout=0.05)
        # print (d)
        result += d.decode()
        if b == 0:
            # print ('There are more data!!')
            tn.write(r' ')
        else:
            break
    # print ('Get result success.')
    return result


# 254 -> 0 1 1 1 1 1 1 1,   2 -> 0 1 0 0 0 0 0 0
def dec2bin(num):
    results = []
    for i in range(8):
        results.append(num % 2)
        num = int(num / 2)
    return results


def set_port(tn, port, state):
    command = "SS " + str(port) + " " + str(state) + '\n'
    result = process_command(tn, command)
    if (result == " Fail"):
        return 0
    l = result.split(':')
    if len(l) < 2:
        return 0
    elif (l[0][-1] == str(port) and l[1][0] == str(state)):
        return 1
    else:
        return 0


def set_all_ports(tn, ports_states):
    for i in range(8):
        if set_port(tn, i + 1, 2 - ports_states[i]) == 0:
            print("Set fail")
            return 0
    print("Set success")
    return 1


def query_port(tn, port):
    command = "RS " + str(port) + '\n'
    result = process_command(tn, command)
    if (result == " Fail"):
        return -1
    l = result.split(':')
    return 2 - int(l[1][0])


def query_all_ports(tn):
    l = []
    res = 0
    for i in range(8):
        resq = query_port(tn, i + 1)
        if resq > -1:
            l.append(resq)
        else:
            print("Query fail")
            return -1
    # calculate status
    for i in range(8):
        res = res * 2 + l[7 - i]
    print("Query result : " + str(res))
    return res


def process_advance(tn, commands):
    results = []
    for command in commands:
        l = len(command)
        #print (command)
        #print(l)
        if l == 0:
            continue
        # set one port, for example, o 1 1
        elif (l >= 5 and command[0].lower() == 'o'):
            command = "SS" + command[1:] + '\n'
            result = process_command(tn, command)
            if (result == " Fail"):
                print("Set fail")
            else:
                print("Set success")
        # pause for n seconds, for example, P 3
        elif (l >= 3 and command[0].lower() == 'p'):
            t = int(command[2:])
            print("Sleep " + str(t) + 's')
            time.sleep(t)
        # set all ports, for example, S 127(01111111)
        elif (l >= 3 and command[0].lower() == 's'):
            num = int(command[2:])
            states = dec2bin(num)
            if (set_all_ports(tn, states) == 0):
                print("Set fail")
            else:
                results.append(num)
        # query all ports, for example, Q
        elif (l >= 1 and command[0].lower() == 'q'):
            resq = query_all_ports(tn)
            if resq > -1:
                results.append(resq)
            else:
                print("Query all fail")
        # others
        else:
            print("Command not exist")
    return results


def main(readfile_path, writefile_path, host, port):
    tn = init_telnet(host, port)
    commands = read_files(readfile_path)
    results = process_advance(tn, commands)
    write_files(writefile_path, results)
    close_telnet(tn)
    print("Finished!")


if __name__ == '__main__':
    argv = sys.argv[1:]
    print(sys.argv[0])
    
    if len(argv) == 4:
        main(argv[0], argv[1], argv[2], argv[3])
    else:
        config_json = open("telnet_config.json")
        try:
            config = json.load(config_json)
        except Exception:
            print("Read config error!")
            exit()
        finally:
            config_json.close()

        commands_path = config['commands_path']
        results_path = config['results_path']
        host_ip = config['host_ip']
        host_port = config['host_port']
        main(commands_path, results_path, host_ip, host_port)
