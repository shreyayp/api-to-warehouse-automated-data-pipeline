# WeatherScope India — Weather Intelligence Dashboard

A Power BI portfolio dashboard that explores short-range weather forecasts for selected Indian cities. It is designed to demonstrate data preparation, KPI design, slicers, time-series analysis, city comparisons, and a detailed forecast table.

> **Where this project lives:** `reports/powerbi/weather-scope-india/` inside the `api-to-warehouse-automated-data-pipeline` repository. It is kept under `reports/powerbi/` because it is a reporting/BI layer that complements the repository's existing data pipeline.

## Dashboard highlights

- KPI cards for average maximum temperature, peak temperature, average rain probability, and rain-risk forecasts.
- City slicer for Bengaluru, Chennai, Hyderabad, Mumbai, and Mysuru.
- Rain probability by forecast date.
- Average maximum temperature by city.
- Detailed weather forecast table for record-level inspection.
- A dark navy/teal Power BI theme.

## Repository files

| File | Purpose |
|---|---|
| `data/WeatherScope_PowerBI_Import.csv` | Standalone CSV prepared for importing into Power BI. |
| `WeatherScope_PowerBI_Theme.json` | Theme JSON for the report's colors and visual styling. |
| `WeatherScope_India_Dashboard.html` | Static HTML preview of the dashboard concept; it is not the Power BI report itself. |
| `screenshots/powerbi-edit-view-reference.png` | Screenshot reference of the Power BI editing view. Replace/add a clean report-canvas screenshot when available. |
| `README.md` | Project description and step-by-step setup guide. |

The Power BI `.pbix` file is not included yet. Once you have downloaded/saved the report as a `.pbix` file from Power BI (if your tenant/report settings allow it), place it in this folder as `WeatherScope_India_Dashboard.pbix`.

## Data source: which CSV should I select?

This repository already has a pipeline output at the repository root:

`data/processed/weather_forecast.csv`

Use that file if it contains the columns required by the visuals and measures below. The standalone import file bundled with this dashboard is:

`reports/powerbi/weather-scope-india/data/WeatherScope_PowerBI_Import.csv`

**Important:** These are two different paths and may have different column names or schema. Start with the bundled `WeatherScope_PowerBI_Import.csv` if you want to reproduce this dashboard using the field names documented below. If you want to use the pipeline output instead, inspect its headers in Power Query and map the fields to the corresponding names. Do not rename columns blindly if your CSV has a different schema.

## Step-by-step: open the CSV in Power BI Service (browser)

1. Open [Power BI](https://app.powerbi.com/) and sign in.
2. Open the workspace where you are building the report.
3. Choose **New** / **Create** and look for an option such as **Report** or **Get data** / **Text or CSV**. Labels can vary with the Power BI experience and your organization's settings.
4. If the browser experience lets you upload a local file, select `WeatherScope_PowerBI_Import.csv` from this project folder. If you have not downloaded this repository to your computer yet, download the CSV from GitHub first:
   - Open `reports/powerbi/weather-scope-india/data/WeatherScope_PowerBI_Import.csv`.
   - Choose **Download raw file** (or the download icon) and save it locally.
5. If Power BI Service does not offer local CSV import in your workspace, use Power BI Desktop on a Windows machine to import the CSV, create the report, save the `.pbix`, and publish it to the workspace. Power BI Desktop is not available natively for macOS.
6. In the import dialog, confirm the delimiter is comma and the first row is treated as headers. Check that `forecast_date` is recognized as a date and temperature/rain/wind fields are numeric.
7. Load the data and rename the imported table to `WeatherForecast` if desired. If you keep a different table name, update DAX references accordingly.

### Using the existing pipeline CSV instead

If you want the report to connect to the repository's existing pipeline output:

1. In VS Code, use the Explorer at the left.
2. Expand `data` → `processed`.
3. Click `weather_forecast.csv`.
4. To import it, use its local file path from the repository folder: `data/processed/weather_forecast.csv`. Do not select `weather_pipeline.db` when the intention is to load a CSV.
5. If the CSV is already on your Mac, use **Get data → Text/CSV** in Power BI Desktop and select that file. If working only in Power BI Service, upload/import support depends on the tenant and workspace features available to you.
6. In Power Query, review the headers and data types, then select **Close & Apply** (Desktop) or the equivalent load/apply action in the browser.

## Field dictionary for the bundled import CSV

| Column | Meaning / suggested type |
|---|---|
| `city` | City name; text |
| `country` | Country; text |
| `latitude`, `longitude` | Geographic coordinates; decimal number |
| `forecast_date` | Forecast date; Date |
| `fetched_at_utc` | Time the forecast was retrieved; Date/Time or text |
| `weather_code` | Weather provider's weather code; whole number/text |
| `temperature_2m_max` | Forecast maximum temperature at 2 m; decimal number, °C |
| `temperature_2m_min` | Forecast minimum temperature at 2 m; decimal number, °C |
| `precipitation_sum` | Forecast precipitation total; decimal number, mm |
| `precipitation_probability_max` | Maximum precipitation probability; decimal number, % |
| `wind_speed_10m_max` | Maximum wind speed at 10 m; decimal number, according to source units |
| `temperature_range_c` | Difference between maximum and minimum temperature; decimal number, °C |
| `is_rain_risk` | Rain-risk flag; text |
| `needs_review` | Data-quality/review flag; text |

## Build the report visuals

After loading the bundled CSV, use the fields from `WeatherForecast`.

### 1. Create measures

In Power BI, create these measures (the menu is usually **Modeling → New measure** in Desktop; browser editing options may differ):

```DAX
Average Max Temperature =
AVERAGE(WeatherForecast[temperature_2m_max])

Peak Temperature =
MAX(WeatherForecast[temperature_2m_max])

Average Rain Probability =
AVERAGE(WeatherForecast[precipitation_probability_max])

Rain-Risk Forecasts =
CALCULATE(
    COUNTROWS(WeatherForecast),
    WeatherForecast[is_rain_risk] = "Yes"
)
```

If Power BI has named the table something else, replace `WeatherForecast` with your table name. Confirm that the rain-probability column is numeric and stored on a 0–100 scale before formatting it as a percentage; do not apply percentage formatting if the values are already decimal fractions unless you adjust the measure.

### 2. Add KPI cards

Add four **Card** visuals and assign one measure to each:
- `Average Max Temperature` — title: **Average Max Temperature**
- `Peak Temperature` — title: **Peak Temperature**
- `Average Rain Probability` — title: **Average Rain Probability**
- `Rain-Risk Forecasts` — title: **Rain-Risk Forecasts**

Set temperature units to °C and rain probability to a readable percentage format.

### 3. Add the city slicer

- Add a **Slicer** visual.
- Drag `city` into the slicer field.
- Enable list or horizontal/tile style, depending on the options available.
- Use it to filter the cards and charts by Bengaluru, Chennai, Hyderabad, Mumbai, or Mysuru.

### 4. Add the rain-probability chart

- Add a **Clustered column chart** or **Line chart**.
- X-axis: `forecast_date`.
- Y-axis: `precipitation_probability_max` with aggregation **Average** (or Maximum if that better matches the story).
- Title: **Rain Probability by Forecast Date (%)**.
- Sort the date axis ascending.

### 5. Add the temperature-by-city chart

- Add a **Clustered column chart**.
- X-axis: `city`.
- Y-axis: `temperature_2m_max` with aggregation **Average**.
- Title: **Average Maximum Temperature by City (°C)**.

### 6. Add the detailed forecast table

Add a **Table** visual and include:
- `city`
- `forecast_date`
- `temperature_2m_max`
- `temperature_2m_min`
- `precipitation_sum`
- `precipitation_probability_max`
- `wind_speed_10m_max`
- `is_rain_risk`

Rename displayed column headers if needed (for example, `temperature_2m_max` → `Max Temp (°C)`). Format numeric columns to sensible decimal places.

## Apply the theme

1. Open the report's theme or styling options.
2. Choose **Browse for themes / Import theme** if that option is available in your Power BI editing experience.
3. Select `WeatherScope_PowerBI_Theme.json`.
4. Review the visuals after importing, because themes do not always override every visual's manually configured formatting.

## Recommended layout and styling

- Canvas background: dark navy.
- Accent color: teal/cyan.
- Top row: four KPI cards.
- Middle row: rain-probability trend and average maximum temperature by city.
- Lower row: detailed forecast table.
- Place the city slicer where it is easy to find and make sure it filters the intended visuals.
- Use consistent titles, units, readable text, and enough contrast.

## Validate before publishing

- Verify date, temperature, precipitation, and wind-speed data types.
- Check that the KPI values change when a city is selected.
- Check whether the rain-risk flag is populated consistently.
- Confirm chart aggregations and labels are correct.
- Note the forecast period and source/update timestamp in the report.
- Do not describe the data as live or real-time unless the pipeline actually refreshes it.
- Avoid uploading credentials, API keys, secrets, or private source data.

## Publish and share

- Save the `.pbix` file if your Power BI environment permits downloading/saving it.
- Publish the report to the appropriate Power BI workspace.
- For a public portfolio, prefer a screenshot or approved static preview unless the data is safe to expose. **Publish to web makes the report publicly accessible to anyone with the link and may expose underlying report data.** Follow your organization's policies before using it.
- Add the public report link to this README only after verifying that it works and that public sharing is permitted.

## Current limitations

- The `.pbix` file is not included in this folder yet.
- The HTML file is a preview, not a replacement for the Power BI report.
- The bundled CSV is a 35-row import dataset. Check the dataset and source notes before presenting it as a production or continuously refreshed forecast.
