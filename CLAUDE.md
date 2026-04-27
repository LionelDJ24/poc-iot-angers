\# POC IoT — Territoire Intelligent Angers



\## Contexte du projet

Preuve de concept d'un système IoT urbain pour Angers Métropole, réalisé dans le cadre d'un projet académique à l'ESAIP. L'objectif est de simuler la collecte, le traitement, le stockage et la visualisation de données de capteurs urbains (qualité de l'air, trafic, déchets).



\## Stack technique

Tout tourne en local via \*\*Docker Compose\*\* :

\- \*\*Mosquitto\*\* (broker MQTT) — port 1883 / 9001

\- \*\*Node-RED\*\* (moteur de règles) — port 1880

\- \*\*InfluxDB 2.7\*\* (base de données séries temporelles) — port 8086

\- \*\*Prometheus\*\* (métriques système) — port 9090

\- \*\*Grafana\*\* (dashboards) — port 3000

\- \*\*Keycloak 23.0\*\* (authentification MFA) — port 8080

\- \*\*Script Python\*\* (`simulateur/capteur.py`) avec `paho-mqtt` — joue le rôle des capteurs physiques



\## Capteurs simulés

Définis dans `simulateur/capteur.py` :

| ID | Topic MQTT | Plage | Unité | Seuil alerte |

|----|-----------|-------|-------|--------------|

| `air\_01` | `angers/air/capteur\_01/data` | 80–260 | µg/m³ | 200 |

| `trafic\_01` | `angers/trafic/capteur\_01/data` | 0–120 | vh/min | 100 |

| `dechet\_01` | `angers/dechet/capteur\_01/data` | 0–100 | % | 80 |



Format JSON publié : `{"capteur\_id", "valeur", "unite", "seuil", "alerte" (bool), "timestamp"}`



\## InfluxDB

\- Organisation : `angers-metropole`

\- Bucket : `iot-capteurs`

\- Measurement : `mesures\_brutes`

\- Identifiants : `admin` / `angers2025`

\- Les champs stockés : `capteur\_id`, `valeur`, `unite`, `seuil`, `alerte`, `timestamp`



\## Requête Flux (Grafana) qui fonctionne — base de référence

```flux

from(bucket: "iot-capteurs")

&#x20; |> range(start: v.timeRangeStart, stop: v.timeRangeStop)

&#x20; |> filter(fn: (r) => r\["\_measurement"] == "mesures\_brutes")

&#x20; |> pivot(rowKey:\["\_time"], columnKey: \["\_field"], valueColumn: "\_value")

&#x20; |> filter(fn: (r) => r\["capteur\_id"] == "air\_01")

&#x20; |> keep(columns: \["\_time", "valeur"])

```

Remplacer `air\_01` par `trafic\_01` ou `dechet\_01` pour les autres capteurs.



\## Node-RED — Flux configurés

\- \*\*Flux 1\*\* : collecte nominale → `mqtt in (angers/#)` → `json` → `debug` → `influxdb out`

\- \*\*Flux 2\*\* : détection d'alerte → `switch (msg.payload.alerte == true)` → `change` → `debug`

\- \*\*Flux 3\*\* : Store and Forward simulé → `inject` → `function (10 messages passés)` → `influxdb out`



Important : dans Node-RED, le serveur MQTT s'appelle `mosquitto` (pas `localhost`) car les conteneurs Docker communiquent par nom de service.



\## Keycloak

\- Realm : `angers-iot`

\- Rôles : `administrateur`, `operateur`, `lecteur`

\- MFA TOTP activé

\- Identifiants admin : `admin` / `angers2025`



\## Identifiants de toutes les interfaces

| Service | URL | Login |

|---------|-----|-------|

| Node-RED | http://localhost:1880 | — |

| InfluxDB | http://localhost:8086 | admin / angers2025 |

| Grafana | http://localhost:3000 | admin / admin |

| Keycloak | http://localhost:8080 | admin / angers2025 |

| Prometheus | http://localhost:9090 | — |



\## État d'avancement

\- \[x] Structure du projet créée

\- \[x] docker-compose.yml écrit et fonctionnel

\- \[x] mosquitto.conf configuré

\- \[x] prometheus.yml configuré

\- \[x] simulateur/capteur.py fonctionnel, paho-mqtt installé

\- \[x] Docker Compose up — tous les services démarrés

\- \[x] Node-RED : flux 1 (collecte) et flux 2 (alertes) configurés

\- \[x] InfluxDB : bucket et token créés

\- \[x] Grafana : dashboard qualité de l'air fonctionnel (requête Flux validée)

\- \[ ] Grafana : panneaux trafic et déchets à finaliser

\- \[ ] Flux 3 Node-RED (Store and Forward) à tester

\- \[ ] Keycloak : realm, rôles et utilisateurs à créer

\- \[ ] Volumes de persistance à ajouter dans docker-compose.yml (données non encore persistées !)

\- \[ ] Export flows.json Node-RED à committer sur GitHub



\## Problème persistance — IMPORTANT

Les configurations Grafana, Keycloak et InfluxDB ne sont PAS encore sauvegardées sur disque. Si `docker-compose down` est exécuté, tout est perdu. Ajouter les volumes manquants dans docker-compose.yml avant de continuer.



\## Diagrammes de séquence couverts

6 scénarios : collecte nominale, détection d'anomalie, authentification utilisateur, provisionnement capteur (OTAA), mise à jour firmware OTA, panne réseau et mode dégradé.



\## Objectif final

Produire un rapport avec captures d'écran réelles (Grafana, Node-RED, Keycloak) pour valider les choix techniques de l'architecture IoT.

