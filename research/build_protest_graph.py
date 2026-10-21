from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl
from PIL import Image, ImageDraw, ImageFont

EUROPE = {
    'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium',
    'Bailiwick of Guernsey', 'Bailiwick of Jersey',
    'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Czech Republic',
    'Denmark', 'Estonia', 'Faroe Islands', 'Finland', 'France', 'Germany',
    'Gibraltar', 'Greece', 'Greenland', 'Hungary', 'Iceland', 'Ireland',
    'Isle of Man', 'Italy', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania',
    'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands',
    'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia',
    'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden',
    'Switzerland', 'Ukraine', 'United Kingdom', 'Vatican City',
}
YEARS = list(range(2016, 2027))
AS_OF = '2026-10-16'
SOURCE = 'Armed Conflict Location & Event Data Project (ACLED), Demonstration Events, HDX; https://data.humdata.org/dataset/demonstration-events'


def load_counts(workbook: Path):
    wb = openpyxl.load_workbook(workbook, read_only=True, data_only=True)
    annual = Counter()
    covered_countries = defaultdict(set)
    for sheet_name in ('Non_HRP', 'HRP_1', 'HRP_2'):
        ws = wb[sheet_name]
        for row in ws.iter_rows(min_row=2, values_only=True):
            country, month, year, events = row[0], row[-3], int(row[-2]), row[-1]
            if country not in EUROPE:
                continue
            annual[year] += int(events or 0)
            covered_countries[year].add(country)
    wb.close()
    return annual, covered_countries


def load_summary(csv_path: Path):
    annual = {}
    covered = {}
    with csv_path.open(newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            year = int(row['year'])
            if row['acled_demonstration_events']:
                annual[year] = int(row['acled_demonstration_events'])
            n_areas = row.get('areas_with_records') or row.get('countries_with_records') or '0'
            covered[year] = set(range(int(n_areas)))
    return annual, covered


def font(size, bold=False):
    path = r'C:\Windows\Fonts\segoeuib.ttf' if bold else r'C:\Windows\Fonts\segoeui.ttf'
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def build_chart(annual, covered, out: Path):
    W, H = 1440, 960
    bg, ink, muted = '#F7F7F3', '#182421', '#56635E'
    primary, partial, incomplete, grid = '#245E55', '#9AA9A3', '#E8E9E3', '#D8DCD6'
    image = Image.new('RGB', (W, H), bg)
    d = ImageDraw.Draw(image)
    d.text((100, 54), 'Recorded protest events in Europe', font=font(43, True), fill=ink)
    d.text((103, 113), 'ACLED-coded protests and violent demonstrations by calendar year', font=font(23), fill=muted)
    d.text((103, 151), 'European observations are incomplete before 2020; 2026 is year to date.', font=font(20), fill=muted)

    left, right, top, bottom = 150, 1365, 245, 690
    max_value = 50000
    # Earlier years use an explicit shaded field because the country coverage is not comparable.
    step = (right - left) / len(YEARS)
    d.rectangle((left, top, left + step * 4, bottom), fill=incomplete)
    for tick in range(0, max_value + 1, 10000):
        y = bottom - (tick / max_value) * (bottom - top)
        d.line((left, y, right, y), fill=grid, width=1)
        label = f'{tick:,}' if tick else '0'
        box = d.textbbox((0, 0), label, font=font(17))
        d.text((left - 18 - (box[2] - box[0]), y - 12), label, font=font(17), fill=muted)
    d.text((left, top - 28), 'Count of events', font=font(17, True), fill=muted)

    d.text((left + 20, top + 14), 'Coverage incomplete / uneven', font=font(17, True), fill=muted)
    d.text((left + 19, top + 43), 'No data in 2016–17', font=font(16), fill=muted)
    d.text((left + step * 6.15, top + 12), 'Full coverage across the defined set begins in 2020', font=font(16), fill=muted)

    centers = []
    for i, year in enumerate(YEARS):
        cx = left + step * (i + 0.5)
        centers.append(cx)
        val = annual.get(year)
        if val is not None:
            bar_h = val / max_value * (bottom - top)
            y = bottom - bar_h
            color = partial if year in (2018, 2019) else primary
            d.rectangle((cx - 31, y, cx + 31, bottom), fill=color)
            if year == 2026:
                # Hatch marks distinguish the partial calendar year without relying on color alone.
                for yy in range(int(y + 7), bottom, 15):
                    d.line((cx - 29, yy, cx + 29, yy - 22), fill='#D3E0DA', width=2)
            label = f'{val:,}'
            box = d.textbbox((0, 0), label, font=font(17, True))
            d.text((cx - (box[2] - box[0]) / 2, y - 29), label, font=font(17, True), fill=ink)
        else:
            d.text((cx, bottom - 25), '—', font=font(19, True), fill=muted, anchor='mm')
        d.text((cx, bottom + 15), str(year), font=font(18, True), fill=ink, anchor='mt')

    # Compact coverage/status key.
    key_y = 753
    d.rectangle((105, key_y + 3, 126, key_y + 21), fill=partial)
    d.text((136, key_y), '2018–19: partial area coverage (14/51)', font=font(16), fill=muted)
    d.rectangle((521, key_y + 3, 542, key_y + 21), fill=primary)
    d.text((552, key_y), '2020–25: all 51 areas in defined set', font=font(16), fill=muted)
    d.rectangle((1032, key_y + 3, 1053, key_y + 21), fill=primary)
    for yy in range(key_y + 5, key_y + 20, 6):
        d.line((1034, yy + 3, 1050, yy - 3), fill='#D3E0DA', width=2)
    d.text((1063, key_y), '2026 partial', font=font(16), fill=muted)

    d.line((102, 800, 1365, 800), fill=grid, width=1)
    d.text((103, 817), 'Source: Armed Conflict Location & Event Data Project (ACLED), Demonstration Events, HDX.', font=font(16), fill=ink)
    d.text((103, 843), 'Dataset: data.humdata.org/dataset/demonstration-events | Data as of 16 October 2026.', font=font(15), fill=muted)
    d.text((103, 868), 'Includes protests and violent demonstrations; excludes mob violence. Not a census or legal registry; counter-protests are not separately tallied.', font=font(15), fill=muted)
    d.text((103, 893), '2026 covers 1 January–16 October. Geographic set: UN M49 Europe, plus Kosovo and European territories in the ACLED file.', font=font(15), fill=muted)

    image.save(out, format='PNG', optimize=True)


def main():
    parser = argparse.ArgumentParser(description='Create an annual Europe protest-events graph from the ACLED HDX workbook.')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--input', type=Path, help='Path to the downloaded demonstration-events.xlsx workbook')
    source.add_argument('--from-csv', type=Path, help='Regenerate the graph from an existing annual CSV')
    parser.add_argument('--out-dir', type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    annual, covered = load_counts(args.input) if args.input else load_summary(args.from_csv)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.out_dir / 'protest-events-europe-by-year.csv'
    with csv_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['year', 'acled_demonstration_events', 'areas_with_records', 'areas_in_scope', 'coverage_status', 'dataset_as_of', 'data_source'])
        for year in YEARS:
            n_countries = len(covered.get(year, set()))
            if year <= 2017:
                count, status = '', 'no European observations in this extract'
            elif year <= 2019:
                count, status = annual[year], 'partial area coverage'
            elif year == 2026:
                count, status = annual[year], 'partial calendar year through 16 October'
            else:
                count, status = annual[year], 'full calendar year; all areas in scope represented'
            writer.writerow([year, count, n_countries, len(EUROPE), status, AS_OF, SOURCE])
    build_chart(annual, covered, args.out_dir / 'protest-events-europe-by-year.png')
    print('Annual totals and area coverage:')
    for year in YEARS:
        print(year, annual.get(year), len(covered.get(year, set())))
    print('Wrote', csv_path)
    print('Wrote', args.out_dir / 'protest-events-europe-by-year.png')


if __name__ == '__main__':
    main()
