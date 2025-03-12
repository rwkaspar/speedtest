import tkinter as tk
from tkinter import ttk
import threading
import speedtest
import time
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

OUTPUT_FILE = "speedtest_results.csv"
header = ['Timestamp', 'Download Speed (Mbit/s)', 'Upload Speed (Mbit/s)', 'Ping (ms)']

def run_speedtest():
    try:
        if not os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                print(f"{OUTPUT_FILE} wurde erstellt.")
        else:
            print(f"{OUTPUT_FILE} existiert bereits.")
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1e6  # Mbit/s
        return round(download_speed, 2)
    except speedtest.ConfigRetrievalError:
        return -1  # Mark as timeout in the graph

def update_chart():
    ax.clear()
    ax.plot(range(len(speed_results)), speed_results, label="Download Geschwindigkeit (Mbit/s)")
    ax.axhline(y=paid_speed.get(), color='r', linestyle='--', label="Ziel-Geschwindigkeit (Mbit/s)")
    ax.axhline(y=16, color='g', linestyle='--', label="Nötiges Minimum (16 Mbit/s)")
    ax.set_xlabel("Anzahl Testläufe [-]")
    ax.set_ylabel("Geschwindigkeit [Mbit/s]")
    ax.legend()
    canvas.draw()

def start_speedtest():
    interval = int(interval_entry.get())
    def test_loop():
        while running:
            start_time = time.time()
            speed = run_speedtest()
            elapsed_time = time.time() - start_time
            speed_results.append(speed)
            result_label.config(text=f"Aktuelle Geschwindigkeit: {speed} Mbit/s")
            update_chart()
            sleep_time = max(0, interval - elapsed_time)
            time.sleep(sleep_time)
    
    global thread
    thread = threading.Thread(target=test_loop, daemon=True)
    thread.start()

def stop_speedtest():
    global running
    running = False
    if thread.is_alive():
        thread.join()

root = tk.Tk()
root.title("Speedtest GUI")
root.geometry("600x500")

frame = ttk.Frame(root, padding=10)
frame.pack(fill='both', expand=True)

# Intervall-Eingabe
interval_label = ttk.Label(frame, text="Messintervall (Sekunden):")
interval_label.pack()
interval_entry = ttk.Entry(frame)
interval_entry.insert(0, "10")
interval_entry.pack()

# Eingabe für bezahlte Geschwindigkeit
paid_label = ttk.Label(frame, text="Bezahlte Geschwindigkeit (Mbit/s):")
paid_label.pack()
paid_speed = tk.DoubleVar(value=100)
paid_entry = ttk.Entry(frame, textvariable=paid_speed)
paid_entry.pack()

# Start-/Stop-Buttons
start_button = ttk.Button(frame, text="Speedtest starten", command=lambda: start_speedtest())
start_button.pack()
stop_button = ttk.Button(frame, text="Speedtest stoppen", command=stop_speedtest)
stop_button.pack()

# Ergebnisanzeige
result_label = ttk.Label(frame, text="Noch keine Messung durchgeführt.")
result_label.pack()

# Matplotlib Diagramm
fig, ax = plt.subplots()
plt.xlabel('Anzahl Testläufe [-]')
speed_results = []
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

running = True
thread = None
root.mainloop()
