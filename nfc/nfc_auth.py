import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CARD_DB = os.path.join(
    BASE_DIR,
    "data",
    "authorized_cards.json"
)


def load_cards():

    with open(CARD_DB, "r", encoding="utf-8") as f:
        return json.load(f)


def authenticate_card(uid):

    uid = uid.strip().upper()

    cards = load_cards()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    print("\n" + "=" * 60)
    print("NEXUS NFC AUTHENTICATION")
    print("=" * 60)

    print("UID       :", uid)
    print("Time      :", timestamp)

    if uid in cards:

        card = cards[uid]

        print("\nSTATUS    : AUTHORIZED")
        print("NODE      :", card["node"])
        print("OWNER     :", card["owner"])

        return {
            "status": "authorized",
            "uid": uid,
            "node": card["node"],
            "owner": card["owner"],
            "timestamp": timestamp
        }

    else:

        print("\nSTATUS    : UNAUTHORIZED")
        print("RISK      : HIGH")
        print("ACTION    : ACCESS DENIED")

        return {
            "status": "unauthorized",
            "uid": uid,
            "node": None,
            "risk": "HIGH",
            "timestamp": timestamp
        }


if __name__ == "__main__":

    print("=" * 60)
    print("NEXUS NFC SECURITY GATEWAY")
    print("=" * 60)

    print("\nScan the NFC card using your phone.")
    print("Copy the Serial Number / UID.")
    print("Paste it below.\n")

    uid = input("Enter NFC UID: ")

    result = authenticate_card(uid)

    print("\n" + "=" * 60)
    print("NEXUS DECISION")
    print("=" * 60)

    if result["status"] == "authorized":

        print("✓ CARD VERIFIED")
        print("✓ NODE AUTHENTICATED")
        print("✓ DIGITAL TWIN ACCESS GRANTED")

    else:

        print("✗ CARD REJECTED")
        print("✗ UNKNOWN NFC DEVICE")
        print("✗ DIGITAL TWIN ACCESS DENIED")