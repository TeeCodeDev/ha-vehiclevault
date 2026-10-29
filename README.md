# VehicleVault for Home Assistant 🚗⚡

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![GitHub release](https://img.shields.io/github/v/release/TeeCodeDev/ha-vehiclevault)](https://github.com/TeeCodeDev/ha-vehiclevault/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Official Home Assistant custom integration for **[VehicleVault](https://github.com/TeeCodeDev/VehicleVault)**. Automatically creates dedicated **Devices** and live **Sensors** for every vehicle in your fleet with zero YAML configuration needed!

---

## ✨ Features

- **Zero YAML Required:** Simple UI config flow via **Settings → Devices & Services → Add Integration**.
- **Dedicated Device Per Vehicle:** Automatically groups all sensors under each vehicle in your garage (e.g. *KIA NIRO*, *Golf 7*, *Tesla Model 3*).
- **Comprehensive Telemetry:**
  - 🚗 **Odometer** (`km`) with native distance device class and total increasing state.
  - 🛡️ **APK Status & Expiration Date** (`sensor.kia_niro_apk_vervaldatum`) and days remaining with overdue alerts.
  - ⛽ **Fuel Economy** in both `km/L` and `L/100km`.
  - 💶 **Last Fill-up Details** (Total cost, volume in liters or kWh, fuel station name, and unit price).
  - ⚡ **PHEV & EV Ready:** Seamlessly handles electric charging sessions (kWh) as well as conventional fuels.
  - 🔧 **Maintenance Intervals & Alerts:** Real-time count and detailed breakdown of upcoming or overdue service items.
- **Customizable Polling:** Default 5-minute polling, configurable via integration options.

---

## 📦 Installation

### Option 1: Via HACS (Recommended)

1. Open **Home Assistant** and navigate to **HACS** → **Integrations**.
2. Click the three dots in the top right corner and select **Custom repositories**.
3. Add the following repository:
   - **Repository:** `https://github.com/TeeCodeDev/ha-vehiclevault`
   - **Type:** `Integration`
4. Click **Add**, find **VehicleVault** in the list, and click **Download**.
5. **Restart Home Assistant**.

### Option 2: Manual Installation

1. Download the latest release from the [Releases](https://github.com/TeeCodeDev/ha-vehiclevault/releases) page.
2. Copy the `custom_components/vehiclevault` folder into your Home Assistant `<config_dir>/custom_components/` directory.
3. **Restart Home Assistant**.

---

## ⚙️ Configuration

1. In Home Assistant, go to **Settings** → **Devices & Services**.
2. Click **Add Integration** in the bottom right corner.
3. Search for **VehicleVault**.
4. Enter your connection details:
   - **VehicleVault URL:** `https://voertuigen.romanas.nl` (or local IP like `http://192.168.1.100:3084`)
   - **API Key:** *(Optional)* Create an API key in **VehicleVault → Instellingen → Gebruikers & Toegang** if you have authentication enabled.
5. Click **Submit**. Home Assistant will immediately detect all active vehicles and create their sensors!

---

## 📊 Sensors Created Per Vehicle

| Sensor | Entity ID Example | Description |
|---|---|---|
| **Kilometerstand** | `sensor.kia_niro_kilometerstand` | Current vehicle odometer in km |
| **APK Vervaldatum** | `sensor.kia_niro_apk_vervaldatum` | Official RDW inspection expiry date |
| **APK Dagen Resterend** | `sensor.kia_niro_apk_dagen_resterend` | Days remaining until APK expiry |
| **APK Status** | `sensor.kia_niro_apk_status` | Status (`ok`, `due_soon`, `overdue`) |
| **Verbruik (km/L)** | `sensor.kia_niro_verbruik_km_l` | Average fuel economy in km/L |
| **Verbruik (L/100km)** | `sensor.kia_niro_verbruik_l_100km` | Average fuel economy in L/100km |
| **Laatste Tankbeurt** | `sensor.kia_niro_laatste_tankbeurt` | Date of last fueling or charging stop |
| **Laatste Tankkosten** | `sensor.kia_niro_laatste_tankkosten` | Cost of last fill-up in € |
| **Laatst Getankt Volume**| `sensor.kia_niro_laatst_getankt_volume` | Liters pumped or kWh charged |
| **Onderhoudsmeldingen** | `sensor.kia_niro_onderhoudsmeldingen` | Count of service items due/overdue |

---

## 💡 Lovelace Dashboard Example

Add this Entities card to your Home Assistant dashboard:

```yaml
type: entities
title: 🚗 KIA NIRO
show_header_toggle: false
entities:
  - entity: sensor.kia_niro_kilometerstand
    name: Huidige Kilometerstand
  - entity: sensor.kia_niro_apk_vervaldatum
    name: APK Vervaldatum
  - entity: sensor.kia_niro_apk_dagen_resterend
    name: Dagen tot APK
  - entity: sensor.kia_niro_verbruik_km_l
    name: Gemiddeld Verbruik
  - entity: sensor.kia_niro_laatste_tankbeurt
    name: Laatst Getankt
  - entity: sensor.kia_niro_laatste_tankkosten
    name: Laatste Kosten
  - entity: sensor.kia_niro_onderhoudsmeldingen
    name: Onderhoudswaarschuwingen
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
