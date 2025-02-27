#!/bin/bash

# Setze die Dauer der Tests und das Intervall
INTERVAL=10  # Interval in Sekunden (z.B. alle 60 Sekunden)
DURATION=60  # Gesamtdauer in Sekunden (z.B. 1 Stunde)

# Ergebnisdatei
OUTPUT_FILE="speedtest_results.txt"

# Starte den Test für die angegebene Dauer
END_TIME=$((SECONDS + DURATION))

while [ $SECONDS -lt $END_TIME ]; do
  # Führe den Speedtest durch und speichere die Ergebnisse
  DATE=$(date "+%Y-%m-%d %H:%M:%S")
  echo "Testing at $DATE" >> $OUTPUT_FILE
  pipenv run python -m speedtest >> $OUTPUT_FILE
  # python -m speedtest >> $OUTPUT_FILE
  echo "----------------------------------------" >> $OUTPUT_FILE

  # Warte für das Intervall
  sleep $INTERVAL
done

echo "Test abgeschlossen. Ergebnisse in $OUTPUT_FILE gespeichert."
