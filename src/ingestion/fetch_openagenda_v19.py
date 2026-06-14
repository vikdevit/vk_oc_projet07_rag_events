import requests
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone

API_KEY = "oa_pk_SMOBRlCiEhQcgohvLtbvuakEtxkoopLotSpzTWBIHsboNXMSSLbDdmydSvGcRFAv"

AGENDAS_URL = "https://api.openagenda.com/v2/agendas"
EVENTS_URL = "https://api.openagenda.com/v2/agendas/{uid}/events"

OUTPUT_FILE = Path("data/raw/ingestion_normandie_events.json")

LIMIT = 100

NOW = datetime.now(timezone.utc)
ONE_YEAR_AGO = NOW - timedelta(days=365)

def fetch_agendas():
    r = requests.get(AGENDAS_URL, headers={"key": API_KEY}, timeout=30)

    if r.status_code != 200:
        print("Agenda error:", r.text)
        return []

    return r.json().get("agendas", [])

def is_relevant_agenda(agenda):

    text = (
        (agenda.get("title") or "") + " " +
        (agenda.get("description") or "")
    ).lower()

    keywords = [
        "culture", "festival", "musique",
        "spectacle", "cinéma", "exposition",
        "art", "théâtre", "événement",
        "concert"
    ]

    geo = [
        "normandie", "rouen", "caen",
        "le havre", "seine-maritime",
        "calvados", "manche", "eure", "orne"
    ]

    return any(k in text for k in keywords + geo)

def fetch_events(agenda_uid):

    url = EVENTS_URL.format(uid=agenda_uid)

    events = []
    offset = 0

    while True:

        params = {
            "limit": LIMIT,
            "offset": offset,
            "detailed": 1
        }

        r = requests.get(url, headers={"key": API_KEY}, params=params)

        if r.status_code != 200:
            break

        data = r.json()
        batch = data.get("events", [])

        if not batch:
            break

        events.extend(batch)
        offset += LIMIT

    return events

def extract_date(event):

    for k in [
        "firstdate_begin",
        "firstDate",
        "startDate",
        "start_date"
    ]:
        if isinstance(event.get(k), str):
            return event[k]

    fd = event.get("firstDate")

    if isinstance(fd, dict):
        for k in ["begin", "date", "value"]:
            if isinstance(fd.get(k), str):
                return fd[k]

    for k, v in event.items():
        if "date" in k.lower() and isinstance(v, str):
            return v

    return None

def normalize(event):

    return {
        "id": event.get("uid"),
        "title": event.get("title", {}).get("fr") or event.get("title"),
        "description": event.get("description", {}).get("fr") or "",
        "location": event.get("location", {}).get("name"),
        "city": event.get("location", {}).get("city"),
        "department": event.get("location", {}).get("department"),
        "keywords": event.get("keywords", []),
        "start_date": extract_date(event),
        "url": event.get("canonicalUrl")
    }

def is_in_time_range(event):

    start = event.get("start_date")

    if not start:
        return False

    try:
        d = datetime.fromisoformat(start.replace("Z", "+00:00"))
    except:
        return False

    return d >= ONE_YEAR_AGO

def is_valid(event):
    return event.get("id") and event.get("title") and event.get("start_date")

def run():

    print("1. Fetch agendas...")
    agendas = fetch_agendas()

    print("Total agendas:", len(agendas))

    print("2. Filter relevant agendas...")
    agendas = [a for a in agendas if is_relevant_agenda(a)]

    print("Agendas after filter:", len(agendas))

    all_events = []

    print("3. Fetch events...")

    for a in agendas:

        uid = a.get("uid")
        if not uid:
            continue

        print("   ->", uid)
        all_events.extend(fetch_events(uid))

    print("Raw events:", len(all_events))

    print("4. Normalize...")

    normalized = [normalize(e) for e in all_events]

    print("\nDEBUG SAMPLE DATES:")
    for e in normalized[:5]:
        print(e["start_date"])

    print("5. Filter time...")

    filtered = [
        e for e in normalized
        if is_valid(e) and is_in_time_range(e)
    ]

    print("Final dataset:", len(filtered))

    # objectif OC : 100–300 events
    if len(filtered) < 80:
        print(" dataset faible > élargir filtres recommandé")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    print("Saved >", OUTPUT_FILE)

if __name__ == "__main__":
    run()


