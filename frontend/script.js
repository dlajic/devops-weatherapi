// immer über Caddy, https + /api:
const API_BASE = `${window.location.origin}/api`;

document.addEventListener("DOMContentLoaded", () => {
  const startSelect = document.getElementById("start-date");
  const endSelect = document.getElementById("end-date");
  const resultsDiv = document.getElementById("range-results");
  const loadButton = document.getElementById("load-range");

  // Lade verfügbare Daten-Daten aus dem Backend
  fetch(`${API_BASE}/weather/dates`)
    .then((response) => response.json())
    .then((dates) => {
      dates.forEach((date) => {
        const option1 = document.createElement("option");
        option1.value = date;
        option1.textContent = date;
        startSelect.appendChild(option1);

        const option2 = document.createElement("option");
        option2.value = date;
        option2.textContent = date;
        endSelect.appendChild(option2);
      });
    });

  // Lade Daten im Bereich
  loadButton.addEventListener("click", () => {
    const from = startSelect.value;
    const to = endSelect.value;

    if (!from || !to) {
      resultsDiv.textContent = "Bitte Start- und Enddatum wählen.";
      return;
    }

    fetch(`${API_BASE}/weather/preview?from_date=${from}&to_date=${to}`)
      .then(response => response.json())
      .then(data => {
        resultsDiv.innerHTML = "";

        if (data.length === 0) {
          resultsDiv.textContent = "Keine Daten für diesen Zeitraum.";
          return;
        }

        // Vorschau-Tabelle
        const table = document.createElement("table");
        table.border = "1";
        table.style.borderCollapse = "collapse";
        table.style.marginTop = "10px";

        const header = table.insertRow();
        ["Zeitpunkt", "Stadt", "Temperatur (°C)"].forEach(text => {
          const th = document.createElement("th");
          th.textContent = text;
          th.style.padding = "6px";
          header.appendChild(th);
        });

        data.forEach((entry, index) => {
          // Bei genau 10 Zeilen → Trennzeile nach den ersten 5
          if (data.length === 10 && index === 5) {
            const dotsRow = table.insertRow();
            ["...", "...", "..."].forEach(text => {
              const cell = dotsRow.insertCell();
              cell.textContent = text;
              cell.style.textAlign = "center";
              cell.style.fontStyle = "italic";
              cell.style.padding = "6px";
            });
          }

          const row = table.insertRow();

          const timeCell = document.createElement("td");
          timeCell.textContent = entry.timestamp;
          timeCell.style.padding = "6px";
          row.appendChild(timeCell);

          const cityCell = document.createElement("td");
          cityCell.textContent = entry.city;
          cityCell.style.padding = "6px";
          row.appendChild(cityCell);

          const tempCell = document.createElement("td");
          tempCell.textContent = `${entry.temperature}°C`;
          tempCell.style.padding = "6px";
          row.appendChild(tempCell);
        });

        resultsDiv.appendChild(table);
      });
  });

  // Dowload option/button
  const downloadButton = document.getElementById("download-csv");

  document.getElementById("download-xlsx").addEventListener("click", () => {
    const from = startSelect.value;
    const to = endSelect.value;

    if (!from || !to) {
      alert("Bitte Start- und Enddatum wählen.");
      return;
    }

    const url = `${API_BASE}/weather/download_excel?from_date=${from}&to_date=${to}`;

    fetch(url)
      .then(res => {
        if (!res.ok) {
          throw new Error("Download fehlgeschlagen. Keine Daten gefunden oder Serverfehler.");
        }
        return res.blob();
      })
      .then(blob => {
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = "wetterdaten.xlsx";
        link.click();
      })
      .catch(error => {
        console.error("Fehler beim Herunterladen:", error);
        alert("Fehler beim Herunterladen der Datei.\nBitte überprüfe Zeitraum oder Verbindung.");
      });
  });


});
