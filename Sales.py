from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime, timedelta
from datetime import datetime
from icalendar import Calendar, Event
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

        if "Support SteamDB" in name:
            break  # stop here

        result.append(f"{name} — {date}")
    return result

MONTHS = {
    "january": 1, "jan": 1,
    "february": 2, "februrary": 2, "feb": 2,
    "march": 3, "mar": 3,
    "april": 4, "apr": 4,
    "may": 5,
    "june": 6, "jun": 6,
    "july": 7, "jul": 7,
    "august": 8, "aug": 8,
    "september": 9, "sept": 9, "sep": 9,
    "october": 10, "oct": 10,
    "november": 11, "nov": 11,
    "december": 12, "dec": 12,
}

def parse_event(event_str: str):
    today = datetime.now()

    # Extract year from title if present
    title_year_match = re.search(r"\b(20\d{2})\b", event_str)
    title_year = int(title_year_match.group(1)) if title_year_match else None

    # Split title and date part
    parts = re.split(r"—", event_str)
    if len(parts) < 2:
        raise ValueError(f"Event format not recognized: {event_str}")
    title = parts[0].strip(" .:()")
    date_part = "—".join(parts[1:]).strip()

    # Extract date chunks: day, optional month, optional year
    date_chunks = re.findall(r"(\d{1,2})(?:\s+([A-Za-z]+))?(?:\s+(\d{4}))?", date_part)
    if not date_chunks:
        raise ValueError(f"Unrecognized date format: {event_str}")

    start_day, start_month_str, start_year_str = date_chunks[0]
    end_day, end_month_str, end_year_str = date_chunks[-1]

    start_day, end_day = int(start_day), int(end_day)

    start_month = MONTHS[start_month_str.lower()] if start_month_str else (
        MONTHS[end_month_str.lower()] if end_month_str else None)
    end_month = MONTHS[end_month_str.lower()] if end_month_str else start_month
    if not start_month or not end_month:
        raise ValueError(f"Month not found in: {event_str}")

    # Determine years
    start_year = int(start_year_str) if start_year_str else title_year
    end_year = int(end_year_str) if end_year_str else start_year

    # If still missing, intelligently pick the correct year
    if not start_year:
        start_year = today.year
        end_year = start_year if not end_year else end_year

        start_date = datetime(start_year, start_month, start_day)
        end_date = datetime(end_year, end_month, end_day)

        # If event already ended this year, roll to next year
        if end_date < today:
            start_year += 1
            end_year += 1
            start_date = datetime(start_year, start_month, start_day)
            end_date = datetime(end_year, end_month, end_day)
        # If we are in the middle of the event, keep current year
        elif start_date <= today <= end_date:
            start_year = start_date.year
            end_year = end_date.year
    else:
        # If year is given, just build dates
        start_date = datetime(start_year, start_month, start_day)
        end_date = datetime(end_year, end_month, end_day)

    return {
        "title": title,
        "start_date": start_date.strftime("%d-%m-%Y"),
        "end_date": end_date.strftime("%d-%m-%Y")
    }

def convert_to_ics(events, filename="events.ics"):
    """
    Convert a list of events to an ICS calendar file.

    events: list of dicts, each with 'title', 'start_date', 'end_date' in 'dd-mm-yyyy' format.
    filename: output ICS file name
    """
    cal = Calendar()
    cal.add('prodid', '-//My Calendar//mxm.dk//')
    cal.add('version', '2.0')

    for event in events:
        e = Event()
        e.add('summary', event['title'])

        # Parse dates
        start = datetime.strptime(event['start_date'], "%d-%m-%Y")
        end = datetime.strptime(event['end_date'], "%d-%m-%Y")

        # In ICS, the end date is non-inclusive, so add 1 day
        end = end.replace(hour=0, minute=0, second=0)  # Ensure midnight
        end += timedelta(days=1)

        e.add('dtstart', start)
        e.add('dtend', end)

        cal.add_component(e)

    # Write to file
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())

if __name__ == "__main__":
    filename = 'sales.html'
    sales = extract_sales_from_file(filename)
#    events_to_ics(sales, "steam_events.ics")
#   print(sales)
    results = []
    for sale in sales:
        parsed = parse_event(sale)
        results.append(parsed)
    convert_to_ics(results, "steam_events.ics")