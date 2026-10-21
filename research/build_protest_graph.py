from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

EUROPE = {
    'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bailiwick of Guernsey',
    'Bailiwick of Jersey', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia',
    'Czech Republic', 'Denmark', 'Estonia', 'Faroe Islands', 'Finland', 'France',
    'Germany', 'Gibraltar', 'Greece', 'Greenland', 'Hungary', 'Iceland', 'Ireland',
    'Isle of Man', 'Italy', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania',
    'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands',
    'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia',
    'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland',
    'Ukraine', 'United Kingdom', 'Vatican City',
}
ACLED_YEARS = list(range(2016, 2027))
AS_OF = '2026-10-16'
ACLED_SOURCE = 'ACLED Demonstration Events, HDX; https://data.humdata.org/dataset/demonstration-events'
POLDEM_SOURCE = 'Kriesi et al. (2020), PolDem Protest Dataset 30; https://poldem.eui.eu/downloads/pea/poldem-protest_30.csv'


def load_acled_workbook(workbook: Path):
    wb = openpyxl.load_workbook(workbook, read_only=True, data_only=True)
    annual = Counter()
    covered = defaultdict(set)
    for sheet_name in ('Non_HRP', 'HRP_1', 'HRP_2'):
        for row in wb[sheet_name].iter_rows(min_row=2, values_only=True):
            country, year, events = row[0], int(row[-2]), row[-1]
            if country in EUROPE:
                annual[year] += int(events or 0)
                covered[year].add(country)
    wb.close()
    return annual, covered


def load_acled_csv(path: Path):
    annual, covered = {}, {}
    with path.open(newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            year = int(row['year'])
            if row['acled_demonstration_events']:
                annual[year] = int(row['acled_demonstration_events'])
            count = int(row.get('areas_with_records') or row.get('countries_with_records') or 0)
            covered[year] = set(range(count))
    return annual, covered


def load_poldem(path: Path):
    df = pd.read_csv(path)
    if 'id_event' not in df or 'year' not in df or 'country_name' not in df:
        raise ValueError('PolDem file must include id_event, year, and country_name columns.')
    # Dataset rows are the final de-duplicated event records. Keep raw event counts;
    # do not apply the country/sample weights intended for cross-country comparisons.
    annual = df.groupby('year')['id_event'].nunique().to_dict()
    areas = df.groupby('year')['country_name'].nunique().to_dict()
    return annual, areas


def font(size, bold=False):
    path = r'C:\Windows\Fonts\segoeuib.ttf' if bold else r'C:\Windows\Fonts\segoeui.ttf'
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def label(draw, xy, text, size=17, color='#53625D', bold=False):
    draw.text(xy, text, font=font(size, bold), fill=color)


def panel(draw, values, years, box, max_value, series_color, coverage_note, partial_years=()):
    left, top, right, bottom = box
    grid, ink, muted = '#D8DDD7', '#182421', '#56635E'
    for tick in range(0, max_value + 1, max_value // 4):
        y = bottom - (tick / max_value) * (bottom - top)
        draw.line((left, y, right, y), fill=grid, width=1)
        txt = f'{tick:,}'
        b = draw.textbbox((0, 0), txt, font=font(15))
        draw.text((left - 15 - (b[2] - b[0]), y - 10), txt, font=font(15), fill=muted)
    step = (right - left) / len(years)
    bar_width = max(8, min(22, step * .62))
    for i, year in enumerate(years):
        x = left + step * (i + .5)
        value = values.get(year)
        if value is not None:
            y = bottom - (value / max_value) * (bottom - top)
            color = '#99A9A2' if year in partial_years else series_color
            draw.rectangle((x - bar_width / 2, y, x + bar_width / 2, bottom), fill=color)
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=ink)
        else:
            draw.text((x, bottom - 15), '—', font=font(15), fill=muted, anchor='mm')
        draw.text((x, bottom + 10), str(year), font=font(14, True), fill=ink, anchor='mt')
    label(draw, (left, top - 31), coverage_note, 16, muted)


def build_chart(poldem, acled, out: Path):
    W, H = 1440, 1040
    bg, ink, muted = '#F7F7F3', '#182421', '#56635E'
    image = Image.new('RGB', (W, H), bg)
    d = ImageDraw.Draw(image)
    label(d, (96, 44), 'European protest events, 2000–2026', 39, ink, True)
    label(d, (100, 99), 'Two historical lenses, shown separately because their event counts are not comparable.', 21, muted)

    label(d, (100, 158), 'PolDem · 30-country academic dataset', 24, ink, True)
    label(d, (100, 193), 'Events reported in English-language newswires; 2000–2015', 17, muted)
    panel(d, poldem, list(range(2000, 2016)), (145, 248, 1365, 445), 3000, '#245E55',
          'Raw coded event records per year · 30 countries (Northern Ireland separately coded)')

    label(d, (100, 520), 'ACLED · Demonstration Events', 24, ink, True)
    label(d, (100, 555), 'Protests and violent demonstrations in HDX monthly country totals; 2018 onward', 17, muted)
    panel(d, acled, ACLED_YEARS, (145, 610, 1365, 790), 50000, '#345C8C',
          'Recorded events per year · 2018–19 partial geography (14/51); 2020 onward full defined set (51/51)',
          partial_years=(2018, 2019))

    # Use visible gap labels instead of interpolating across missing or incompatible years.
    label(d, (103, 836), 'No series coverage: 2016–17', 16, muted)
    d.line((100, 874, 1365, 874), fill='#D8DDD7', width=1)
    label(d, (100, 895), 'PolDem spans 2000–2015. ACLED starts in Europe unevenly in 2018 and is geographically complete from 2020.', 16, ink)
    label(d, (100, 923), 'Different source systems, event definitions, and monitoring methods mean the bars cannot be compared across panels.', 16, ink)
    label(d, (100, 954), 'PolDem: hybrid manual/NLP coding of 10 English-language newswires; approximately 31,000 records overall.', 15, muted)
    label(d, (100, 980), 'ACLED: reported events, not a census or legal registry. 2026 covers 1 Jan–16 Oct; counter-protests are not separately tallied.', 15, muted)
    label(d, (100, 1006), 'Sources: poldem.eui.eu/downloads/pea/poldem-protest_30.csv · data.humdata.org/dataset/demonstration-events', 14, muted)
    image.save(out, format='PNG', optimize=True)


def write_poldem_csv(annual, areas, path):
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['year', 'poldem_event_records', 'areas_with_records', 'dataset', 'data_source', 'counting_note'])
        for year in range(2000, 2016):
            writer.writerow([year, annual[year], areas[year], 'PolDem Protest Dataset 30, version 1', POLDEM_SOURCE,
                             'Unweighted unique event IDs; media-coded; separate source from ACLED'])


def main():
    parser = argparse.ArgumentParser(description='Create a separated long-run graph of PolDem and ACLED Europe protest-event series.')
    p = parser.add_mutually_exclusive_group(required=True)
    p.add_argument('--poldem-csv', type=Path, help='Downloaded PolDem poldem-protest_30.csv')
    p.add_argument('--poldem-summary', type=Path, help='Existing annual PolDem summary CSV')
    a = parser.add_mutually_exclusive_group(required=True)
    a.add_argument('--acled-input', type=Path, help='Downloaded ACLED Demonstration Events workbook')
    a.add_argument('--acled-summary', type=Path, help='Existing annual ACLED summary CSV')
    parser.add_argument('--out-dir', type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    if args.poldem_csv:
        poldem, areas = load_poldem(args.poldem_csv)
        write_poldem_csv(poldem, areas, args.out_dir / 'protest-events-europe-poldem-2000-2015.csv')
    else:
        poldem, areas = {}, {}
        with args.poldem_summary.open(newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = int(row['year'])
                poldem[year] = int(row['poldem_event_records'])
                areas[year] = int(row['areas_with_records'])
    acled, _ = load_acled_workbook(args.acled_input) if args.acled_input else load_acled_csv(args.acled_summary)
    build_chart(poldem, acled, args.out_dir / 'protest-events-europe-by-year.png')
    print('Wrote', args.out_dir / 'protest-events-europe-poldem-2000-2015.csv')
    print('Wrote', args.out_dir / 'protest-events-europe-by-year.png')


if __name__ == '__main__':
    main()
