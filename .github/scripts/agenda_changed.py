#!/usr/bin/env python3
"""Compare les evenements A VENIR de agenda.ics (actuel) et agenda.new.ics (frais).

Affiche 'CHANGED' si les evenements futurs different, sinon 'SAME'.
- Ignore l'ordre des evenements (Google ne le garantit pas).
- Ignore les champs volatils (DTSTAMP / LAST-MODIFIED / CREATED / SEQUENCE).
- Ignore TOTALEMENT les evenements anterieurs a aujourd'hui (le site ne les affiche pas).
"""
import datetime
import re

VOLATILE = ("DTSTAMP", "LAST-MODIFIED", "CREATED", "SEQUENCE")


def future_signature(path):
    try:
        raw = open(path, encoding="utf-8").read()
    except OSError:
        return None
    # Deplie les lignes repliees (ICS = continuation par espace/tab en debut de ligne)
    raw = raw.replace("\r\n", "\n").replace("\n ", "").replace("\n\t", "")
    today = datetime.date.today().strftime("%Y%m%d")
    sigs = []
    for block in raw.split("BEGIN:VEVENT")[1:]:
        body = block.split("END:VEVENT")[0]
        lines = [l for l in body.split("\n")
                 if l.strip() and not l.startswith(VOLATILE)]
        start = ""
        for l in lines:
            if l.startswith("DTSTART"):
                m = re.search(r"(\d{8})", l)
                if m:
                    start = m.group(1)
                break
        if start and start >= today:            # uniquement les evenements a venir
            sigs.append("\n".join(sorted(lines)))
    return "\n".join(sorted(sigs))


a = future_signature("agenda.ics")
b = future_signature("agenda.new.ics")
print("SAME" if a is not None and a == b else "CHANGED")
