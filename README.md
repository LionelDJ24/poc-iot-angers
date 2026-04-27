# POC IoT — Territoire Intelligent Angers

Preuve de concept d'un système IoT urbain pour Angers Métropole. Simulation de capteurs urbains (qualité de l'air, trafic, déchets) avec collecte MQTT, détection d'alertes, visualisation temps réel et authentification MFA.

---

## Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.x](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

---

## Installation et démarrage

### 1. Cloner le projet

```bash
git clone https://github.com/LionelDJ24/poc-iot-angers.git
cd poc-iot-angers
```

### 2. Lancer les conteneurs

```bash
docker-compose up -d
```

Attendre 30 secondes que tous les services démarrent.

### 3. Installer les dépendances Python

```bash
pip install paho-mqtt
```

### 4. Lancer le simulateur de capteurs

```bash
python simulateur/capteur.py
```

---

## Interfaces disponibles

| Service | URL | Identifiants |
|---------|-----|--------------|
| Node-RED | http://localhost:1880 | — |
| InfluxDB | http://localhost:8086 | admin / angers2025 |
| Grafana | http://localhost:3000 | admin / admin |
| Keycloak | http://localhost:8080 | admin / angers2025 |
| Prometheus | http://localhost:9090 | — |

---

## Configuration sur un nouveau PC

### InfluxDB — Générer un token

1. Ouvrir http://localhost:8086
2. **Load Data** → **API Tokens** → **Generate API Token** → **All Access**
3. Copier le token

### Node-RED — Configurer le token InfluxDB

1. Ouvrir http://localhost:1880
2. Double-cliquer sur le nœud **requête http**
3. Dans **En-têtes**, mettre :
   - Clé : `Authorization`
   - Valeur : `Token VOTRE_TOKEN`
4. **Terminer** → **Déployer**

### Grafana — Configurer la source de données

1. Ouvrir http://localhost:3000
2. **Connections** → **Data sources** → **Add data source** → **InfluxDB**
3. Configurer :
   - Query language : **Flux**
   - URL : `http://influxdb:8086`
   - Organization : `angers-metropole`
   - Token : coller le token InfluxDB
   - Default Bucket : `iot-capteurs`
4. **Save & test**

### Grafana — Importer le dashboard

1. **Dashboards** → **New** → **Import**
2. Coller le contenu de `grafana/dashboard.json`
3. **Load** → **Import**

### Keycloak — Importer le realm

1. Ouvrir http://localhost:8080 → **Administration Console**
2. Cliquer sur **master** → **Create Realm**
3. Activer **Browse** → sélectionner `keycloak/realm-export.json`
4. **Create**

---

## Capteurs simulés

| Capteur | Topic MQTT | Plage | Unité | Seuil alerte |
|---------|-----------|-------|-------|--------------|
| air_01 | angers/air/capteur_01/data | 80–260 | µg/m³ | 200 |
| trafic_01 | angers/trafic/capteur_01/data | 0–120 | vh/min | 100 |
| dechet_01 | angers/dechet/capteur_01/data | 0–100 | % | 80 |

---

## Scénarios démontrés

| Séquence | Description | Où le voir |
|----------|-------------|------------|
| 1 | Collecte nominale | Grafana — courbes en temps réel |
| 2 | Détection d'alertes | Grafana — panneau Alertes Actives |
| 3 | Authentification MFA | Keycloak — connexion alice/bob/charlie |
| 6 | Store and Forward | Node-RED — bouton "Lancer Simulation Panne" |

---

## Utilisateurs Keycloak

| Utilisateur | Rôle | Password |
|-------------|------|---------|
| alice | administrateur | angers2025 |
| bob | operateur | angers2025 |
| charlie | lecteur | angers2025 |

---

## Stack technique

- **Mosquitto** — Broker MQTT
- **Node-RED** — Moteur de règles et traitement
- **InfluxDB 2.7** — Base de données séries temporelles
- **Grafana** — Visualisation et dashboards
- **Prometheus** — Supervision des métriques
- **Keycloak 23.0** — Authentification et MFA
- **Python / paho-mqtt** — Simulation des capteurs