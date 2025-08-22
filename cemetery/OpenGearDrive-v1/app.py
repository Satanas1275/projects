import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import asyncio
from bleak import BleakScanner, BleakClient
import threading
import time
import vgamepad as vg

class OpenGearDriveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenGear Drive - Contrôle")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        self.wheel_device = None
        self.pedals_device = None
        self.gear_port = None

        self.wheel_position = tk.StringVar(value="Position: 0")
        self.accel_value = tk.StringVar(value="Accel: 0%")
        self.brake_value = tk.StringVar(value="Break: 0%")
        self.gear_x = tk.StringVar(value="X: 0")
        self.gear_y = tk.StringVar(value="Y: 0")

        self.running = False
        self.gamepad = vg.VX360Gamepad()
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="OpenGear Drive", font=("Arial", 20, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        frame = ttk.Frame(self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(frame, text="Volant:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, pady=5, sticky="w")
        self.wheel_status = tk.Label(frame, text="Non connecté", fg="red", bg="#f0f0f0")
        self.wheel_status.grid(row=0, column=1, pady=5)
        tk.Label(frame, textvariable=self.wheel_position, font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=2, pady=5)

        tk.Label(frame, text="Pédales:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, pady=5, sticky="w")
        self.pedals_status = tk.Label(frame, text="Non connecté", fg="red", bg="#f0f0f0")
        self.pedals_status.grid(row=1, column=1, pady=5)
        tk.Label(frame, textvariable=self.accel_value, font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=2, pady=5)
        tk.Label(frame, textvariable=self.brake_value, font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=2, pady=5)

        tk.Label(frame, text="Boîte de vitesses:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, pady=5, sticky="w")
        self.gear_status = tk.Label(frame, text="Non connecté", fg="red", bg="#f0f0f0")
        self.gear_status.grid(row=3, column=1, pady=5)
        tk.Label(frame, textvariable=self.gear_x, font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=2, pady=5)
        tk.Label(frame, textvariable=self.gear_y, font=("Arial", 12), bg="#f0f0f0").grid(row=4, column=2, pady=5)

        ttk.Button(self.root, text="Connecter", command=self.connect_all).pack(pady=10)
        ttk.Button(self.root, text="Déconnecter", command=self.disconnect_all).pack(pady=10)

    async def scan_bluetooth(self, target_name):
        print(f"Recherche de {target_name}...")
        devices = await BleakScanner.discover(timeout=10.0)
        for device in devices:
            print(f"Appareil détecté: {device.name} ({device.address})")
            if device.name == target_name:
                return device
        print(f"{target_name} non trouvé")
        return None

    def connect_all(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.connect_device, args=("OGD Wheel", self.connect_wheel), daemon=True).start()
            threading.Thread(target=self.connect_device, args=("OGD Pedals", self.connect_pedals), daemon=True).start()
            threading.Thread(target=self.connect_gear, daemon=True).start()

    def disconnect_all(self):
        self.running = False
        self.wheel_status.config(text="Non connecté", fg="red")
        self.pedals_status.config(text="Non connecté", fg="red")
        self.gear_status.config(text="Non connecté", fg="red")
        self.gamepad.reset()
        self.gamepad.update()

    def connect_device(self, target_name, callback):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        device = loop.run_until_complete(self.scan_bluetooth(target_name))
        self.root.after(0, lambda: callback(device))
        loop.close()

    def connect_wheel(self, device):
        if device and self.running:
            self.wheel_device = device
            self.wheel_status.config(text=f"Connecté ({device.address})", fg="green")
            threading.Thread(target=self.read_ble_data, args=(device, self.wheel_notification_handler), daemon=True).start()
        else:
            self.wheel_status.config(text="Non connecté", fg="red")

    def connect_pedals(self, device):
        if device and self.running:
            self.pedals_device = device
            self.pedals_status.config(text=f"Connecté ({device.address})", fg="green")
            threading.Thread(target=self.read_ble_data, args=(device, self.pedals_notification_handler), daemon=True).start()
        else:
            self.pedals_status.config(text="Non connecté", fg="red")

    def connect_gear(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            print(f"Port détecté: {port.device} - {port.description}")
            if "USB Serial Device" in port.description:
                try:
                    self.gear_port = port.device
                    self.gear_status.config(text=f"Connecté ({self.gear_port})", fg="green")
                    self.read_gear_data()
                    return
                except serial.SerialException:
                    continue
        self.gear_status.config(text="Non connecté", fg="red")

    def wheel_notification_handler(self, sender, data):
        try:
            position = int(data.decode('utf-8').strip())
            # Normaliser pour joystick gauche X (-1.0 à 1.0), ajuste selon la plage réelle
            wheel_value = max(-1.0, min(1.0, position / 50.0))  # Si plage -50 à 50, sinon ajuste
            self.wheel_position.set(f"Position: {position}")
            self.gamepad.left_joystick_float(x_value_float=wheel_value, y_value_float=0.0)
            print(f"Volant envoyé: {wheel_value}")
            self.gamepad.update()
        except (UnicodeDecodeError, ValueError):
            print("Erreur décodage volant")

    def pedals_notification_handler(self, sender, data):
        try:
            accel_float = 0.0  # Valeur par défaut
            brake_float = 0.0  # Valeur par défaut
            lines = data.decode('utf-8').strip().split("\n")
            for line in lines:
                if "accel :" in line:
                    value = float(line.split("accel :")[1].strip())
                    self.accel_value.set(f"Accel: {value}%")
                    accel_float = value / 100.0
                    self.gamepad.right_trigger_float(accel_float)
                elif "break :" in line:
                    value = float(line.split("break :")[1].strip())
                    self.brake_value.set(f"Break: {value}%")
                    brake_float = value / 100.0
                    self.gamepad.left_trigger_float(brake_float)
            print(f"Pédales envoyées - Accel: {accel_float}, Break: {brake_float}")
            self.gamepad.update()
        except (UnicodeDecodeError, ValueError) as e:
            print(f"Erreur décodage pédales: {e}")

    def read_ble_data(self, device, handler):
        async def ble_loop():
            client = BleakClient(device.address)
            try:
                await client.connect()
                print(f"Connecté à {device.name} ({device.address})")
                await client.start_notify("6E400003-B5A3-F393-E0A9-E50E24DCCA9E", handler)
                while self.running:
                    await asyncio.sleep(0.1)
                await client.stop_notify("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
            except Exception as e:
                print(f"Erreur {device.name}: {e}")
            finally:
                if client.is_connected:
                    await client.disconnect()
                    print(f"Déconnecté de {device.name}")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(ble_loop())
        loop.close()

    def read_gear_data(self):
        try:
            ser = serial.Serial(self.gear_port, 9600, timeout=1)
            while self.running and self.gear_port:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    parts = line.split(",")
                    gear_x_value = 0.0  # Valeur par défaut
                    gear_y_value = 0.0  # Valeur par défaut
                    for part in parts:
                        if "X:" in part:
                            value = int(part.split("X:")[1].strip())
                            self.gear_x.set(f"X: {value}")
                            gear_x_value = max(-1.0, min(1.0, (value - 512) / 512.0))
                        elif "Y:" in part:
                            value = int(part.split("Y:")[1].strip())
                            self.gear_y.set(f"Y: {value}")
                            gear_y_value = max(-1.0, min(1.0, (value - 512) / 512.0))
                    self.gamepad.right_joystick_float(x_value_float=gear_x_value, y_value_float=gear_y_value)
                    print(f"Boîte envoyée - X: {gear_x_value}, Y: {gear_y_value}")
                    self.gamepad.update()
                time.sleep(0.1)
            ser.close()
        except serial.SerialException as e:
            print(f"Erreur boîte: {e}")

def main():
    root = tk.Tk()
    app = OpenGearDriveApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()