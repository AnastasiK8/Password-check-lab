"""ПР5, варіант 8. Симулятор датчиків тиску у водопровідній мережі.

Чотири вузли p-01..p-04 публікують тиск p (бар) і витрату q (м3/год)
кожні 5 с у теми kharkiv/water/<id>/telemetry.
Сценарій (цикл 10 хв): на 2-4 хв порив біля p-02 (тиск -1 бар,
витрата x1,3), на 6-8 хв знеструмлення p-04, ~2 % збоїв сенсора.
"""
import argparse
import json
import math
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

# ---------- Параметри мережі вузлів ----------
STATIONS = [
    {"id": "p-01", "name": "Вузол 1", "p0": 5.2, "q0": 220.0},
    {"id": "p-02", "name": "Вузол 2", "p0": 4.8, "q0": 180.0},
    {"id": "p-03", "name": "Вузол 3", "p0": 4.5, "q0": 150.0},
    {"id": "p-04", "name": "Вузол 4", "p0": 4.0, "q0": 120.0},
]
PREFIX = "kharkiv/water"
INTERVAL = 5           # період вимірювання, с
PHI = 0.8              # інерційність ряду AR(1)
SIGMA_P = 0.05         # шум тиску, бар
SIGMA_Q = 3.0          # шум витрати, м3/год
GLITCH_P = 0.02        # імовірність збою сенсора

# ---------- Сценарій подій (секунди від початку циклу) ----------
CYCLE = 600
# порив: (вузол, з, по, падіння тиску в барах, множник витрати)
BURST = ("p-02", 120, 240, 1.0, 1.3)
OUTAGE = ("p-04", 360, 480)            # знеструмлення


class Station:
    """Один вузол: власне MQTT-з'єднання і власні ряди p та q."""

    def __init__(self, cfg, host, port):
        self.id = cfg["id"]
        self.p0 = cfg["p0"]
        self.q0 = cfg["q0"]
        self.xp = self.mup = None      # попередні значення тиску
        self.xq = self.muq = None      # попередні значення витрати
        self.online = False
        self.host, self.port = host, port
        self.c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                             client_id=f"sim-{self.id}")
        # Last Will: брокер сам опублікує offline при обриві
        self.c.will_set(self.topic("status"), "offline",
                        qos=1, retain=True)
        self.c.on_connect = self.on_connect

    def topic(self, kind):
        return f"{PREFIX}/{self.id}/{kind}"

    def on_connect(self, client, userdata, flags, rc, props):
        client.publish(self.topic("status"), "online",
                       qos=1, retain=True)

    def start(self):
        self.c.connect(self.host, self.port, keepalive=10)
        self.c.loop_start()
        self.online = True

    def power_cut(self):
        """Знеструмлення: вузол замовкає без DISCONNECT."""
        self.c.loop_stop()
        self.online = False

    def power_on(self):
        self.c.reconnect()
        self.c.loop_start()
        self.online = True

    def stop(self):
        """Коректне вимкнення: offline публікуємо самі."""
        self.c.publish(self.topic("status"), "offline",
                       qos=1, retain=True).wait_for_publish(2)
        self.c.disconnect()
        self.c.loop_stop()

    def measure(self, hour, burst):
        # Формула (3): добовий профіль, пік споживання о 19:00.
        # У пік витрата вища на 35 %, тиск нижчий на 10 %.
        c = math.cos(2 * math.pi * (hour - 19) / 24)
        mu_p = self.p0 * (1 - 0.10 * c)
        mu_q = self.q0 * (1 + 0.35 * c)
        if self.xp is None:
            self.xp = self.mup = mu_p
            self.xq = self.muq = mu_q
        # Формула (4): AR(1) навколо добового профілю
        p = (mu_p + PHI * (self.xp - self.mup)
             + SIGMA_P * random.gauss(0, 1))
        q = (mu_q + PHI * (self.xq - self.muq)
             + SIGMA_Q * random.gauss(0, 1))
        self.xp, self.mup = max(p, 0.5), mu_p
        self.xq, self.muq = max(q, 1.0), mu_q
        p_out, q_out = self.xp, self.xq
        if burst:                      # порив: тиск падає, витрата росте
            p_out = max(p_out - BURST[3], 0.0)
            q_out = q_out * BURST[4]
        if random.random() < GLITCH_P:  # збій сенсора
            if random.random() < 0.5:
                p_out = random.choice([-1.0, 99.0])
            else:
                q_out = random.choice([-1.0, 9999.0])
        return {
            "ts": int(time.time() * 1000),   # мс від 1970 р.
            "p": round(p_out, 2),
            "q": round(q_out, 1),
        }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default="localhost")
    ap.add_argument("--port", type=int, default=1883)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()
    random.seed(args.seed)

    stations = [Station(s, args.host, args.port) for s in STATIONS]
    for s in stations:
        s.start()
    print(f"Підключено до {args.host}:{args.port}. Ctrl+C - зупинити.")
    t0 = time.monotonic()
    try:
        while True:
            phase = (time.monotonic() - t0) % CYCLE
            now = datetime.now()
            hour = now.hour + now.minute / 60
            for s in stations:
                cut = (s.id == OUTAGE[0]
                       and OUTAGE[1] <= phase < OUTAGE[2])
                if cut and s.online:
                    s.power_cut()
                    print(f"{now:%H:%M:%S} {s.id} ЗНЕСТРУМЛЕНО")
                elif not cut and not s.online:
                    s.power_on()
                    print(f"{now:%H:%M:%S} {s.id} живлення відновлено")
                if not s.online:
                    continue
                burst = (s.id == BURST[0]
                         and BURST[1] <= phase < BURST[2])
                m = s.measure(hour, burst)
                s.c.publish(s.topic("telemetry"),
                            json.dumps(m), qos=1)
                print(f"{now:%H:%M:%S} {s.id} "
                      f"p={m['p']:>6} q={m['q']:>7}")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Зупинка…")
    finally:
        for s in stations:
            if s.online:
                s.stop()


if __name__ == "__main__":
    main()