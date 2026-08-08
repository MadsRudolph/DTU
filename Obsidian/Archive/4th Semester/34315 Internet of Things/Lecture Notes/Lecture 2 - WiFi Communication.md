---
course: "34315"
course-name: "Internet of Things"
type: lecture-note
week: 7
tags: [IoT, lecture]
date: 2026-02-12
---
# Lecture 2 - WiFi Communication

> [!abstract] Lecture Overview
> Lesson 2/13 — Teacher: Henrik
> Topics: Wireless network properties, IEEE 802.11 architecture & standards, MAC layer protocols (ALOHA, CSMA/CD, CSMA/CA), hidden node problem, 802.11 frame format, association process, WiFi channels, Wireshark demo.
> Reading: Arduino Ch. 3-4, Data Comm Networks Ch. 4.5 & 5.5.

> [!example] Related Materials
> - Slides: [[260211 Wireless lecture.pdf]]
> - Exercise: [[34315_Intro to Ex 2-7.pdf|Exercises 2-7 -- Communication & WiFi]]
> - Solutions: [[Ex 2_4 Solution.pdf|Solution Ex 2-4]], [[Ex 5_7 Solution.pdf|Solution Ex 5-7]]
> - Previous: [[Lecture 1 - Introduction to IoT]]

---

## 1. Wireless Network Properties

Wireless communication introduces challenges not present in wired networks:

| Property | Wired | Wireless |
|----------|-------|----------|
| **Medium** | Dedicated cable | Shared air/spectrum |
| **Interference** | Low (shielded) | High (other devices, walls) |
| **Security** | Physical access needed | Anyone in range can listen |
| **Collision detection** | Easy (CSMA/CD) | Hard (hidden node problem) |
| **Signal degradation** | Predictable | Varies with distance, obstacles |

Key wireless-specific issues:
- **Path loss** — Signal attenuates with distance ($\propto \frac{1}{d^2}$)
- **Multipath fading** — Reflections cause constructive/destructive interference
- **Hidden node problem** — Two stations can't hear each other but both interfere at the AP
- **Exposed node problem** — A station unnecessarily defers transmission

---

## 2. IEEE 802.11 Architecture

### 2.1 Network Components

The 802.11 standard defines the following components:

| Component | Description |
|-----------|-------------|
| **STA** (Station) | Any device with a WiFi interface |
| **AP** (Access Point) | Station that provides access to the distribution system |
| **BSS** (Basic Service Set) | A group of stations communicating with one AP |
| **DS** (Distribution System) | Backbone connecting multiple APs (typically Ethernet) |
| **ESS** (Extended Service Set) | Multiple BSSs connected via a DS, appearing as one network |

### 2.2 Operating Modes

- **Infrastructure mode**: All communication goes through the AP. Stations associate with an AP to join the network. This is the most common mode.
- **Ad-hoc mode (IBSS)**: Stations communicate directly with each other without an AP. Used for peer-to-peer connections.

### 2.3 WiFi Standards

| Standard | Year | Frequency | Max Data Rate | Key Feature |
|----------|------|-----------|---------------|-------------|
| 802.11a | 1999 | 5 GHz | 54 Mbps | OFDM |
| 802.11b | 1999 | 2.4 GHz | 11 Mbps | DSSS, first mass-market |
| 802.11g | 2003 | 2.4 GHz | 54 Mbps | OFDM at 2.4 GHz |
| 802.11n (WiFi 4) | 2009 | 2.4/5 GHz | 600 Mbps | MIMO |
| 802.11ac (WiFi 5) | 2013 | 5 GHz | 6.9 Gbps | MU-MIMO, wider channels |
| 802.11ax (WiFi 6) | 2020 | 2.4/5/6 GHz | 9.6 Gbps | OFDMA, better density |

---

## 3. MAC Layer Protocols

The MAC (Medium Access Control) layer manages how stations share the wireless medium. Understanding the evolution from ALOHA to CSMA/CA explains why WiFi works the way it does.

### 3.1 ALOHA

The simplest protocol — transmit whenever you have data:
- **Pure ALOHA**: Transmit anytime. If a collision occurs (detected by lack of ACK), wait a random time and retransmit.
- **Slotted ALOHA**: Time is divided into slots. Transmit only at the start of a slot. Doubles throughput compared to pure ALOHA.
- **Max throughput**: ~18% (pure) / ~37% (slotted) — very inefficient.

### 3.2 CSMA/CD (Carrier Sense Multiple Access / Collision Detection)

Used in wired Ethernet (802.3):
1. **Listen before transmitting** (carrier sense)
2. **If busy**, wait until the medium is free
3. **Transmit** and simultaneously monitor for collisions
4. **If collision detected**, send a jam signal and back off (exponential backoff)

> [!warning] Why CSMA/CD Doesn't Work Wirelessly
> A wireless station cannot transmit and listen simultaneously on the same channel — its own transmission drowns out any incoming signal. Therefore, **collision detection is impossible** in wireless networks.

### 3.3 CSMA/CA (Carrier Sense Multiple Access / Collision Avoidance)

Used in WiFi (802.11) — avoids collisions instead of detecting them:

1. **Listen** to the medium (carrier sense)
2. **If busy**, wait until free + DIFS (Distributed Inter-Frame Spacing)
3. **Random backoff**: Wait a random number of slots (contention window)
4. **Transmit** the frame
5. **Wait for ACK**: The receiver sends an ACK after SIFS (Short Inter-Frame Spacing)
6. **No ACK received** → assume collision, double backoff window, retransmit

The priority scheme uses inter-frame spacing:
- **SIFS** (Short IFS) — Highest priority (ACKs, CTS)
- **DIFS** (Distributed IFS) — Normal data frames
- **EIFS** (Extended IFS) — After errors

### 3.4 Hidden Node Problem & RTS/CTS

The **hidden node problem** occurs when two stations (A and C) are both in range of the AP (B) but not of each other. A and C cannot sense each other's transmissions, leading to collisions at B.

**Solution — RTS/CTS handshake:**

```
A → B: RTS (Request to Send)        ← A asks permission
B → A: CTS (Clear to Send)          ← B grants, C hears this too
A → B: DATA                         ← A transmits
B → A: ACK                          ← B confirms receipt
```

When C hears the CTS from B, it knows to **wait** (using the NAV timer encoded in the CTS). This prevents C from transmitting during A's data transfer.

> [!tip] RTS/CTS Overhead
> RTS/CTS adds overhead, so it's typically only used for **large frames**. Small frames are sent directly using basic CSMA/CA, accepting the small collision risk.

---

## 4. 802.11 Frame Format

The WiFi frame has a unique structure with **four address fields** (unlike Ethernet's two):

| Field | Size | Purpose |
|-------|------|---------|
| Frame Control | 2 bytes | Type, subtype, flags (ToDS, FromDS) |
| Duration/ID | 2 bytes | NAV timer value |
| **Address 1** | 6 bytes | Receiver address |
| **Address 2** | 6 bytes | Transmitter address |
| **Address 3** | 6 bytes | Additional address (depends on ToDS/FromDS) |
| Sequence Control | 2 bytes | Fragment & sequence numbers |
| **Address 4** | 6 bytes | Used only in WDS (wireless bridge) |
| Frame Body | 0-2312 bytes | Payload data |
| FCS | 4 bytes | Frame Check Sequence (CRC-32) |

### 4.1 Address Interpretation

The **ToDS** and **FromDS** bits in the Frame Control field determine how the four addresses are interpreted:

| ToDS | FromDS | Addr 1 (Receiver) | Addr 2 (Transmitter) | Addr 3 | Addr 4 |
|------|--------|-------------------|---------------------|---------|--------|
| 0 | 0 | Destination | Source | BSSID | — |
| 1 | 0 | BSSID (AP) | Source | Destination | — |
| 0 | 1 | Destination | BSSID (AP) | Source | — |
| 1 | 1 | Receiver AP | Transmitter AP | Destination | Source |

- **ToDS=1, FromDS=0**: Station sending to AP (most common uplink)
- **ToDS=0, FromDS=1**: AP sending to station (most common downlink)
- **ToDS=1, FromDS=1**: WDS bridge (AP to AP)

### 4.2 Frame Types

| Type | Examples |
|------|----------|
| **Management** | Beacon, Probe Request/Response, Association Request/Response, Authentication |
| **Control** | RTS, CTS, ACK |
| **Data** | Data frames carrying user payload |

---

## 5. Association Process

Before a station can communicate through an AP, it must go through an association process:

### 5.1 Scanning

The station first discovers available networks:

- **Passive scanning**: Listen for **beacon frames** broadcast by APs (typically every 100 ms). Beacons contain SSID, supported rates, security info.
- **Active scanning**: Send **probe request** frames on each channel. APs respond with **probe response** frames. Faster but uses more power.

### 5.2 Authentication & Association

1. **Authentication** — The station authenticates with the chosen AP (Open System or Shared Key)
2. **Association Request** — Station sends its capabilities to the AP
3. **Association Response** — AP accepts and assigns an Association ID (AID)
4. The station is now part of the BSS and can transmit data frames

---

## 6. WiFi Channels

### 6.1 2.4 GHz Band

The 2.4 GHz band is divided into channels, each 22 MHz wide with 5 MHz spacing:

- **Channels 1-13** available (11 in the US, 13 in Europe)
- Only **channels 1, 6, and 11** are non-overlapping
- Using overlapping channels causes co-channel interference
- In dense environments, plan AP placement to use channels 1, 6, 11

### 6.2 5 GHz Band

The 5 GHz band offers more non-overlapping channels (typically 20+ depending on region) with less interference, but shorter range due to higher frequency.

---

## 7. Connecting ESP8266 to WiFi

The ESP8266 can connect to a WiFi network using the Arduino WiFi library:

```cpp
#include <ESP8266WiFi.h>

const char* ssid = "NetworkName";
const char* password = "NetworkPass";

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Connected!");
    Serial.println(WiFi.localIP());
}
```

---

## Key Takeaways

1. **Wireless** introduces challenges not present in wired: shared medium, interference, hidden nodes, no collision detection
2. **CSMA/CA** avoids collisions using listen-before-send + random backoff + ACK confirmation (unlike Ethernet's CSMA/CD which detects collisions)
3. **RTS/CTS** solves the hidden node problem by reserving the medium before large transmissions
4. **802.11 frames** have 4 address fields — the ToDS/FromDS bits determine their meaning
5. **Beacon frames** advertise the network; stations discover APs via passive (listen) or active (probe) scanning
6. Only **channels 1, 6, 11** are non-overlapping in the 2.4 GHz band
7. The ESP8266 provides built-in WiFi, enabling IoT connectivity with a few lines of Arduino code

---

> [!nav]
> &nbsp;
>
> [[Lecture 1 - Introduction to IoT|← Previous]] | [[34315 Internet of Things|34315 Home]] | [[Lecture 3 - Basic Electronics for IoT|Next →]]
>
> &nbsp;
