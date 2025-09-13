from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime
from dateutil import parser
import re

def extract_sales_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    sales = soup.find_all("div", class_="panel-sale")

    result = []
    for sale in sales:
        name_tag = sale.find("h4", class_="panel-sale-name")
        date_tag = name_tag.find_next("div") if name_tag else None

        name = name_tag.get_text(strip=True) if name_tag else "Unknown"
        date = date_tag.get_text(strip=True) if date_tag else "Unknown date"
        result.append(f"{name} — {date}")
    return result


def events_to_ics(event_list, output_file="events.ics"):
    cal = Calendar()

    for raw in event_list:
        try:
            parts = [p.strip(" .…") for p in raw.split("—")]
            title = parts[0]

            if len(parts) != 3:
                print(f"Skipping (bad format): {raw}")
                continue

            start_str, mid_str, end_str = parts

            # Detect year from title (fallback: current year)
            year_match = re.search(r"\b(20\d{2})\b", title)
            base_year = int(year_match.group(1)) if year_match else datetime.now().year

            # Case A: "29 September — 6 October" → mid has month
            if re.search(r"[A-Za-z]", mid_str):
                start_date = parser.parse(f"{mid_str} {base_year}", dayfirst=True, fuzzy=True)
                end_date = parser.parse(f"{end_str} {base_year}", dayfirst=True, fuzzy=True)

            # Case B: "13 — 20 October" → mid is just a day, end has month
            else:
                start_date = parser.parse(f"{mid_str} {end_str} {base_year}", dayfirst=True, fuzzy=True)
                end_date = parser.parse(f"{end_str} {base_year}", dayfirst=True, fuzzy=True)

            # If end < start, roll forward a year
            if end_date < start_date:
                end_date = parser.parse(f"{end_str} {base_year + 1}", dayfirst=True, fuzzy=True)

            # Create calendar event
            event = Event()
            event.name = title
            event.begin = start_date
            event.end = end_date.replace(hour=23, minute=59)
            cal.events.add(event)

        except Exception as e:
            print(f"Error parsing '{raw}': {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(cal)

    print(f"ICS file saved as {output_file}")

if __name__ == "__main__":
    filename = 'sales.html'
    sales = extract_sales_from_file(filename)
    events_to_ics(sales, "steam_events.ics")
#    print(sales)
#    for sale in sales:
#        print(sale)
