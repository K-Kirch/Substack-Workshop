# Protest data for a European trend argument

**Prepared:** 21 October 2026
**Question:** Can we count recurring protests across Europe, including authorized, unauthorized, and counter-protest events, from 7 October 2023 onward?

## Finding

The sources reviewed reveal no single public, harmonized register of every protest in Europe, and “registered demonstrations” cannot stand in for all protests. Notification and authorization rules differ by country. European standards say notification should not become de facto permission and call for spontaneous assemblies to be provided for in law ([Venice Commission / OSCE-ODIHR guidelines](https://www.venice.coe.int/webforms/documents/default.aspx?pdffile=CDL-AD%282019%29017-e)). A government notice register therefore records a legal-administrative subset, not the full universe of protests. The best immediately usable cross-national event source is ACLED. It is a systematically compiled, expert-coded, news-sourced event dataset with European coverage, but it is not an official census and does not encode authorization status in a harmonized way. Pair it with selected official registers or case reporting only as corroboration, not as a Europe-wide count.

For the draft’s actual question, “protest” is the clearer English word. We should measure repeated protest events and separately examine whether they were followed by observable responses (concessions, policy changes, elections, or leadership exits). Event counts alone cannot establish that protest has lost its effect.

The different causes do not invalidate the aggregate question of whether protest, as a political tool, is producing change. They matter when matching a protest to its demand and the response it sought, and when describing what the events were about. The central analysis can still ask whether recurring protests across Europe are followed by change.

## Best available sources

| Source | Coverage and unit | What it can answer | Limits for this article |
|---|---|---|---|
| [ACLED event data](https://acleddata.com/methodology/acled-codebook) | Expert-coded event data across all European countries/territories in its coverage list. Coverage begins Jan. 2018 for some countries and Jan. 2020 for most Western and Northern European countries; check the [country/time coverage table](https://acleddata.com/methodology/countrytime-period-coverage) before comparing. Current data are updated weekly. | The strongest starting point for counting reported protest events by date, location, event type, actor, and source; separates peaceful protests, protests with intervention, excessive force against protesters, and violent demonstrations/riots. Its definition is an in-person public gathering of at least three people advocating a shared cause. | This is not a census: events must be reported in sources ACLED monitors and meet its coding criteria. It excludes strikes absent a demonstration, symbolic or legislative acts, and individual actions. It merges same-day, same-place incidents with the same actors and activity. It records events, not continuous campaigns or whether a protest “worked.” “Counter-demonstration” is a formal tag documented for the US, not a Europe-wide field; elsewhere a counter-protest may be visible in actors/notes/sources but should not be assumed exhaustively tagged. The data do not systematically distinguish legally notified, authorized, prohibited, or spontaneous gatherings. Access requires a myACLED account; API, export and curated downloads are available after registration ([access guide](https://acleddata.com/faq/how-can-i-access-and-use-acled-data), [API guide](https://acleddata.com/api-documentation/getting-started)). |
| [GDELT Event Database](https://www.gdeltproject.org/data.html) | Global, machine-coded events extracted from monitored news, with files/API and broad historical coverage. GDELT 2.0 event files begin 19 Feb. 2015; feeds update every 15 minutes. Its CAMEO event taxonomy includes protest codes such as “demonstrate or rally.” | A useful independent news-coverage cross-check and a way to find reported events/articles ACLED may not capture. | It counts coded media-reported events, not verified gatherings or registrations. News availability, syndication, duplicate reporting, translation, geolocation, event coding, and event-date versus report-date affect counts. The 15-minute feed is not 15-minute event precision. Do not present raw GDELT counts as “all protests.” Use it for discovery/triangulation, with deduplication and manual checks. [Event codebook](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf). |
| [PolDem protest events](https://poldem.eui.eu/data-overview/) | Academic protest-event datasets compiled from media: a 30-country dataset for 2000–2015, plus narrower datasets with other country/time spans. | Valuable historical baseline and a clear demonstration that comparable European event research is possible. | It does not cover the article’s 2023–26 period. It cannot substantiate a post–7 October 2023 trend. |
| [German Protest Registrations Dataset](https://zenodo.org/records/10094245) | FOI-derived records of protests registered with authorities in 16 German cities. Consistent coverage for five cities, 2018–22; all included cities have 2022 data. Contains dates, organizers, topics, registered participants, and observed participants for some cities. | A rare view into notified/registered events, useful for showing how registrations differ from media-coded event data and for German historical context. | City-limited and ends in 2022, so it cannot supply a current European comparison. It excludes gatherings not registered with those authorities and has varying completeness across cities. |
| [UCDP Violent Political Protest GED](https://ucdp.uu.se/downloads/) | Event-level dataset of violent political protest events, 2011–2025, geocoded to village and day; distinct from a dataset of all protests. | A corroborating source for the violent escalation part of the claim, especially when a definition of “violent political protest” is appropriate. | It deliberately excludes peaceful protest and therefore cannot estimate the share of protests that become violent or whether peaceful protest is becoming less effective. Its scope and violence threshold differ from ACLED’s. |
| [OSCE/ODIHR assembly monitoring](https://odihr.osce.org/odihr/663487) | Selected, on-the-ground observations across OSCE states, published in periodic monitoring reports; nearly 150 assemblies observed in 36 participating states across monitoring cycles. | Primary-source evidence about policing, restrictions, facilitation, and practical assembly rights in observed cases. | This is a human-rights monitoring programme, not a comprehensive event-count database. |

## Method recommendation

1. **Define geography before counting.** “Europe” may include or exclude Russia, Belarus, Turkey, the Caucasus, and microstates. Use ACLED’s published regional/country list and state the exact set. Turkey is placed in ACLED’s Middle East region and the Caucasus in Caucasus and Central Asia, so an ACLED “Europe” query will not automatically mean every country a reader might call European. For a cleaner EU or Western-European claim, filter to a fixed set of countries with full coverage from 2020 onward.
2. **Use ACLED as the main series, not as ground truth.** Filter event dates from 2023-10-07 through 2026-10-21; include `Protests` and violent `Riots`/`Violent demonstration` events, but report peaceful and violent categories separately. For a clean equal-length comparison, compare 2020-10-07 through 2023-10-06 with 2023-10-07 through 2026-10-06, then show 2026-10-07 through 2026-10-21 separately as a short tail. Use a fixed country set with full coverage over the comparison windows. Freeze a dated extract because weekly updates can revise history. Report the measure as “ACLED-recorded protest events,” never “all protests.”
3. **Test recurrence at more than one scale.** Show Europe-wide monthly totals and country counts, then identify recurring protest activity by country/city/issue or movement where the data permit. A rise in Europe-wide event totals does not by itself show that the same public is repeatedly protesting or that a Europe-wide movement exists. ACLED’s event unit is location-date-activity, not a campaign.
4. **Treat counter-protests conservatively.** Review the event’s actors, notes, and cited source URLs for evidence of simultaneous opposing gatherings. Do not claim a complete Europe-wide counter-protest count from the US-only ACLED tag. GDELT can help discover reports, but each candidate pair needs validation.
5. **Measure “effect” separately.** For a manageable set of recurring cases, create an outcome table: protest demand; government response and date; whether it is a concession, implementation, reversal, election/leadership change, or no documented response; and evidence/source. This will test the thesis more directly than counting marches alone. It also prevents treating a protest followed by a concession as proof of causation without checking alternative causes.
6. **Check report sources for selected cases.** ACLED’s `SOURCE`/`SOURCE SCALE` fields and event notes identify the reporting basis. Trace a sample of large, repeated, and violent cases to national/local reporting and official statements. Keep crowd-size claims separate: estimates vary substantially, and event count is not attendance.

For “consecutive,” report the daily and weekly series, the number of active countries per week, and the longest gap with no ACLED-recorded event in the defined Europe set. Because ACLED aggregates some same-place, same-day activity (for example, a protest that turns violent can be a single riot event), the event total is a count of coded events, not necessarily the count of distinct street gatherings. A per-country and per-week series helps avoid making the European total look like a single continuous campaign.

## Bottom line for the draft

The data can support a careful claim about the frequency, recurrence, and violence profile of **reported protest events** across a defined set of European countries since 7 October 2023. They cannot establish that every protest was counted, that notification status is comparable, that protests are the same campaign, or that protest has become ineffective. The stronger article would make its unit and denominator explicit, then test effectiveness with a small number of traceable protest–response sequences.

## Primary-source references

- ACLED, [Codebook](https://acleddata.com/methodology/acled-codebook); [country/time coverage](https://acleddata.com/methodology/countrytime-period-coverage); [event disaggregation](https://acleddata.com/faq/how-are-events-disaggregated); [data access](https://acleddata.com/faq/how-can-i-access-and-use-acled-data); [tags](https://acleddata.com/methodology/tags-data).
- GDELT Project, [data download and query documentation](https://www.gdeltproject.org/data.html); [Event Database codebook](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf).
- European University Institute / WZB, [PolDem data overview](https://poldem.eui.eu/data-overview/).
- Zenodo, [German Protest Registrations Dataset](https://zenodo.org/records/10094245).
- Uppsala Conflict Data Program, [dataset download center](https://ucdp.uu.se/downloads/).
- Venice Commission / OSCE-ODIHR, [Guidelines on Freedom of Peaceful Assembly](https://www.venice.coe.int/webforms/documents/default.aspx?pdffile=CDL-AD%282019%29017-e); OSCE/ODIHR, [monitoring reports](https://odihr.osce.org/odihr/663487).

## Annual Europe graph: protest event counts

A first annual graph is now available at `research/protest-events-europe-by-year.png`, with the underlying annual values in `research/protest-events-europe-by-year.csv` and the workbook aggregation in `research/build_protest_graph.py`.

The source is ACLED's public **Demonstration Events** workbook on HDX, dated 16 October 2026. HDX describes this series as monthly country-level reported demonstration events. ACLED's definition in this aggregate includes its protest and violent demonstration events, while excluding mob violence. I summed the monthly records across the workbook's three mutually exclusive sheets for UN M49 Europe countries and areas represented in the file, plus Kosovo. The defined set contains 51 countries and areas.

| Year | ACLED-recorded events | Coverage in defined set |
|---|---:|---|
| 2016 | No European observations | Not available |
| 2017 | No European observations | Not available |
| 2018 | 5,275 | 14 of 51 countries and areas |
| 2019 | 7,508 | 14 of 51 countries and areas |
| 2020 | 37,152 | 51 of 51 countries and areas |
| 2021 | 42,867 | 51 of 51 countries and areas |
| 2022 | 34,275 | 51 of 51 countries and areas |
| 2023 | 31,378 | 51 of 51 countries and areas |
| 2024 | 31,397 | 51 of 51 countries and areas |
| 2025 | 32,834 | 51 of 51 countries and areas |
| 2026 through 16 October | 24,643 | 51 of 51 countries and areas, partial year |

The 2016–17 blanks mean no European observations in this source extract, not zero protests. The 2018–19 totals only cover 14 of the 51 countries and areas and should not be compared directly with later totals. ACLED's published coverage history also says coverage expanded across Europe with 2020 as the start for the newly added countries; the graph treats 2020–25 as the comparable annual series. The 2026 value is year to date.

This is a series of reported, coded events, not a census of every protest, a register of authorized events, or a separate count of counter-protests. Event totals can show frequency and recurrence. They cannot show whether protests produced political change by themselves. For that question, pair the count series with documented protest demands and subsequent government responses.

**Sources:** [HDX ACLED Demonstration Events dataset](https://data.humdata.org/dataset/demonstration-events); [ACLED coverage expansion to all of Europe](https://acleddata.com/press/acled-expands-coverage-all-europe); [ACLED aggregate data description](https://acleddata.com/use-access/how-use-acleds-aggregated-data).
