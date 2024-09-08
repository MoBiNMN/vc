#!/usr/bin/python3

import socket
import threading
import pyaudio
import socket
import threading
import pyaudio
import keyboard
import math
import struct
import flet as ft
from protocol import DataType, Protocol

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bufferSize = 4096
        self.connected = False
        self.name = "MoBiN"
        self.mic = True


        chunk_size = 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 14000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)

        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        threading.Thread(target=self.send_data_to_server).start()
        ft.app(self.main)
    
    def c3chnge(self,e):
        if self.c3.value == True:
            self.mic = False
        else:
            self.mic = True


    def dcon(self,e):
        self.connected = False
    def con(self,e):
        while 1:
            try:
                self.target_ip = '91.185.187.49'
                self.target_port = 42071
                self.server = (self.target_ip, self.target_port)
                print(self.connectToServer())
                break
            except ():
                print("Couldn't connect to server...")
    def main(self,page: ft.Page):
        page.window.max_height = 600
        page.window.min_width = 600
        page.window.max_width = 600
        page.window.min_height = 600
        page.window.height = 600
        page.window.width = 600
        Mtxt = ft.Text("MN RooM")
        page.theme_mode=ft.ThemeMode.DARK
        def c4chnge(e):
            if self.c4.value == True:
                self.c3.value = True
                self.c3.disabled = True
            else:
                self.c3.disabled = False
                self.c3.value=False
            
            page.update()


        def icchng(e):
            if page.theme_mode == ft.ThemeMode.DARK:
                page.theme_mode=ft.ThemeMode.LIGHT
                icbtn.icon=ft.icons.LIGHT_MODE
            else:
                page.theme_mode=ft.ThemeMode.DARK
                icbtn.icon=ft.icons.DARK_MODE
            page.update()
        icbtn = ft.IconButton(icon=ft.icons.DARK_MODE,on_click=icchng)
        page.appbar = ft.AppBar(
            title=Mtxt,
            actions=[
                ft.Container(content=icbtn,
                            margin=ft.Margin(right=20,left=0,top=0,bottom=0)),
            ]
        )
        
        def c1chnge(e):
            if self.c1.value==True:
                self.c2.value=False
                self.txtf1.disabled=False
            else:
                self.c2.value=True
                self.txtf1.disabled=True
            page.update()
        def c2chnge(e):
            if self.c2.value==True:
                self.c1.value=False
                self.txtf1.disabled=True
            else:
                self.c1.value=True
                self.txtf1.disabled=False
            page.update()

        self.c1 = ft.Checkbox(label="Push to Talk", value=True,on_change=c1chnge)
        self.c2 = ft.Checkbox(label="Voice Activation",on_change=c2chnge)
        self.c3 = ft.Checkbox(label="Mute Microphone",on_change=self.c3chnge)
        self.c4 = ft.Checkbox(label="Mute Sound",on_change=c4chnge)
        self.sw = ft.Switch(label="Push to talk")
        self.txt = ft.Text("Enter Name : ")
        self.txtf = ft.TextField(label="Name")
        self.txtf1 = ft.CupertinoTextField(placeholder_text="Key",max_length=1,width=50,placeholder_style=ft.TextStyle(size=15),input_filter=ft.TextOnlyInputFilter())
        rw = ft.Row(controls=[
                self.c1,
                
                self.txtf1,
        ],)
        btn1 = ft.ElevatedButton(content=ft.Text("Connect"),on_click=self.con)
        btn2 = ft.ElevatedButton(content=ft.Text("Disconnect"),on_click=self.dcon)
        rw2 = ft.Row(controls=[
            btn1,
            ft.Container(width=100),
            btn2
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.VerticalAlignment.CENTER
        )
        page.add(
            ft.Column(
                controls=[
                    self.txt,
                    ft.Container(content=self.txtf,width=200),
                    ft.Container(height=20),
                    rw,
                    self.c2,
                    ft.Container(height=20),
                    self.c3,
                    self.c4,
                    ft.Container(height=20),
                    rw2,
                    
                ],

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                
            )
        )

    def receive_server_data(self):
        while True:
            if self.connected:
                if self.c4.value==False:
                    try:
                        
                        data, addr = self.s.recvfrom(1025)
                        message = Protocol(datapacket=data)
                        print("Debug recv server")
                        if message.DataType == DataType.ClientData:
                            self.playing_stream.write(message.data)
                    except:
                        pass

    def connectToServer(self):
        if self.connected:
            return True

        message = Protocol(dataType=DataType.Handshake, data=self.name.encode(encoding='UTF-8'))
        self.s.sendto(message.out(), self.server)

        data, addr = self.s.recvfrom(1025)
        datapack = Protocol(datapacket=data)

        if (addr==self.server and datapack.DataType==DataType.Handshake and 
        datapack.data.decode('UTF-8')=='ok'):
            print('Connected to server successfully!')
            self.connected = True
        self.connected = True
        return self.connected

    def send_data_to_server(self):
        while True:
            if self.connected:
                if self.c3.value==False:
                    try:
                        # if keyboard.is_pressed("z"):
                        if self.c1.value==True:
                            if keyboard.is_pressed(self.txtf1.value):
                                data = self.recording_stream.read(512)
                                message = Protocol(dataType=DataType.ClientData, data=data)
                                print("Debug send push to talk server")
                                self.s.sendto(message.out(), self.server)
                        else:
                            data = self.recording_stream.read(512)
                            message = Protocol(dataType=DataType.ClientData, data=data)
                            print("Debug send voic active server")
                            self.s.sendto(message.out(), self.server)                     
                    except:
                        pass

client = Client()
