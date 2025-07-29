# Verwende ein minimales Node-Image mit http-server
FROM node:18-alpine

# Setze das Arbeitsverzeichnis auf /usr/src/app (Name egal, aber konsistent)
WORKDIR /app

# Installiere http-server
RUN npm install -g http-server

# Kopiere den gesamten Inhalt vom lokalen frontend/ in das Container-Verzeichnis
COPY . .

# Öffne Port 3000 (damit du lokal über localhost:3000 zugreifen kannst)
EXPOSE 3000

# Starte den Server
CMD ["http-server", "-p", "3000"]
