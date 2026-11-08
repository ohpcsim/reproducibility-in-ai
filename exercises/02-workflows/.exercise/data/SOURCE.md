# About this data

`earthquakes.csv` is every earthquake of magnitude 4.0 and above in 2024, worldwide, from the USGS ANSS Comprehensive Earthquake Catalog (ComCat). It is unchanged from the catalog's CSV output: 14,175 rows, 2.7 MB.

- Source: <https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2024-01-01&endtime=2025-01-01&minmagnitude=4.0&orderby=time-asc>
- Catalog: <https://earthquake.usgs.gov/data/comcat/>. Column meanings: <https://earthquake.usgs.gov/data/comcat/data-eventterms.php>
- Downloaded: November 8, 2026.
- License: a work of the United States Government, in the public domain. USGS: "USGS-authored or produced data and information are considered to be in the U.S. Public Domain." <https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits>
- Please cite: U.S. Geological Survey, Earthquake Hazards Program, 2017, Advanced National Seismic System (ANSS) Comprehensive Catalog of Earthquake Events and Products: Various, <https://doi.org/10.5066/F7MS3QZH>.

The catalog mixes magnitude types, mostly `mb`, with `mww` for the largest events. The exercise fits one b-value to them as they are.
