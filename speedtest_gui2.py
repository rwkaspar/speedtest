import tkinter as tk
from tkinter import ttk
import threading
import speedtest
import time
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# CSV-Datei vorbereiten
csv_file = "speedtest_results.csv"
def init_csv():
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Test Number", "Download Speed (Mbit/s)", "Upload Speed (Mbit/s)", "Server"])

def save_to_csv(test_number, download_speed, upload_speed, server):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([test_number, download_speed, upload_speed, server])

# Speedtest durchführen
def run_speedtest():
    try:
        st = speedtest.Speedtest()
        server = st.get_best_server()['host']
        download_speed = st.download() / 1e6  # Mbit/s
        upload_speed = st.upload() / 1e6      # Mbit/s
        return round(download_speed, 2), round(upload_speed, 2), server
    except speedtest.ConfigRetrievalError:
        return -1, -1, -1  # Mark as timeout in the graph

# Diagramm aktualisieren
def update_chart():
    ax.clear()
    ax.axhline(y=0, color='black')
    ax.plot(range(len(download_results)), download_results, label="Download Speed (Mbit/s)")
    ax.plot(range(len(upload_results)), upload_results, label="Upload Speed (Mbit/s)")
    ax.axhline(y=paid_speed.get(), color='r', linestyle='--', label="Paid Speed (Mbit/s)")
    ax.axhline(y=16, color='g', linestyle='--', label="Minimum Guaranteed (16 Mbit/s)")
    ax.set_title("Speedtest Results")
    ax.set_xlabel("Anzahl Tests [-]")
    ax.set_ylabel("Speed [Mbit/s]")
    ax.legend()
    canvas.draw()

# Starten des Speedtests
def start_speedtest():
    interval = int(interval_entry.get())
    def test_loop():
        test_number = 1
        while running:
            start_time = time.time()
            download_speed, upload_speed, server = run_speedtest()
            elapsed_time = time.time() - start_time
            download_results.append(download_speed)
            upload_results.append(upload_speed)
            save_to_csv(test_number, download_speed, upload_speed, server)  # Speichern in CSV
            result_label.config(text=f"Download: {download_speed} Mbit/s, Upload: {upload_speed} Mbit/s")
            update_chart()
            sleep_time = max(0, interval - elapsed_time)
            time.sleep(sleep_time)
            test_number += 1
        # Nach dem Testlauf Diagramm als PNG speichern
        save_chart_as_image()

    global thread
    thread = threading.Thread(target=test_loop, daemon=True)
    thread.start()

# Stoppen des Speedtests
def stop_speedtest():
    global running
    running = False
    if thread.is_alive():
        thread.join()

# Diagramm als Bild speichern
def save_chart_as_image():
    fig.savefig("speedtest_results.png")

# GUI-Setup
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
plt.xlabel('Anzahl Tests [-]')
plt.ylabel('Speed [Mbit/s]')
download_results = []
upload_results = []
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# CSV initialisieren
init_csv()

running = True
thread = None
root.mainloop()
