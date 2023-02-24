#!/usr/bin/env python3

import sys
import os
from glob import glob
from subprocess import check_output, CalledProcessError
from cryptography.fernet import Fernet
import requests

uri = sys.argv[1]
print("URI:", uri)
id = uri.split("=")[1]


def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()

def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])
    return dict((os.path.basename(dev), dev) for dev in usb_devices)

def get_mount_points(devices=None):
    devices = devices or get_usb_devices()  # if devices are None: get_usb_devices
    output = check_output(['mount']).splitlines()
    output = [tmp.decode('UTF-8') for tmp in output]

    def is_usb(path):
        return any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.split()[0]))
    return [(info.split()[0], info.split()[2]) for info in usb_info]


if __name__ == '__main__':
    paths = get_mount_points()


    file_path = ""

    count = 0
    while file_path == "":

        if count == 50:
            response = requests.post("http://127.0.0.1:8000/physical-key-authentication/",data={'unique_id': id,'authentication':'fail'})
            break

        for path in paths:
            # Check whether the specified
            # path exists or not
            if path[1] == '/media/{user}/{usb drive name}':
                isExist = os.path.exists(path[1]+"/keys.txt")
                file_path = path[1]+"/keys.txt"
            else:
                isExist = os.path.exists(path[1]+"/keys.txt")

            if isExist == True:
                print("Key found, decrypting...")
                with open(file_path) as f:
                    data  = f.readlines()

                    key = data[0].split("\n")[0]

                    encrypted_data = data[1].split("\n")[0]

                    encrypted_data = bytes(encrypted_data,'utf-8')
                    
                    decrypted_data = decrypt_data(encrypted_data, key)

                    print(decrypted_data)

                    if decrypted_data == id:
                        print("logged in successfull")
                        response = requests.post("http://127.0.0.1:8000/physical-key-authentication/",data={'unique_id': id,'authentication':'success'})
                    else:
                        print("logged in fail")
                        response = requests.post("http://127.0.0.1:8000/physical-key-authentication/",data={'unique_id': id,'authentication':'fail'})
            else:
                print("Keys not found")

        count+= 1

    