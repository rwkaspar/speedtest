import speedtest
import csv
import time
import os

# Setze die Dauer der Tests und das Intervall
INTERVAL = 10  # Interval in Sekunden (z.B. alle 60 Sekunden)
# DURATION = 3600  # Gesamtdauer in Sekunden (z.B. 1 Stunde)

OUTPUT_FILE = "speedtest_results.csv"
header = ['Timestamp', 'Download Speed (Mbit/s)', 'Upload Speed (Mbit/s)', 'Ping (ms)']

# Initialisiere den Speedtest
st = speedtest.Speedtest()

if not os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        print(f"{OUTPUT_FILE} wurde erstellt.")
else:
    print(f"{OUTPUT_FILE} existiert bereits.")

if 'DURATION' in locals():
    end_time = time.time() + DURATION


while True or time.time() < end_time:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    try:
        ping = st.get_best_server()['host']
        download_speed = st.download() / 1_000_000  # in Mbit/s
        upload_speed = st.upload() / 1_000_000  # in Mbit/s
    except:  # values for no connection
        ping = -1
        download_speed = -1
        upload_speed = -1

    # Schreibe die Ergebnisse in die CSV-Datei
    with open(OUTPUT_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, download_speed, upload_speed, ping])

    # Ausgabe für den Benutzer
    print(f"Test completed at {timestamp}")
    print(f"Download Speed: {download_speed:.2f} Mbit/s")
    print(f"Upload Speed: {upload_speed:.2f} Mbit/s")
    print(f"Ping: {ping} ms")
    print("--------------------------")

    # Warte für das Intervall
    if INTERVAL > 0:
        time.sleep(INTERVAL)
    else:
        continue

print(f"Test abgeschlossen. Ergebnisse in {OUTPUT_FILE} gespeichert.")
