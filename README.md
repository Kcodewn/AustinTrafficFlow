
<h1>Austin Traffic Flow Simulator</h1>

<h2>Overview</h2>

This project delivers an end-to-end pipeline to forecast and visualize 15‑minute traffic volumes across over 5,000 road-segment sensors in Austin, Texas. It includes:

Data ingestion & preprocessing from the City of Austin Open Data Portal.

Forecasting models (ARIMA baseline, historical-average fallback).

Flask API serving JSON predictions at /traffic?time=<ISO_TIMESTAMP>.

Interactive front‑end using Google Maps JavaScript API to display live and predicted traffic overlays.

<h2>Goals</h2>

Provide commuters and planners with a tool to anticipate future congestion.

Demonstrate a full‑stack application from data to visualization.

Establish baseline performance (MAE, RMSE) for future model improvements.

<h2>Setup & Usage</h2>

1. Clone repository

git clone https://github.com/Kcodewn/austin-traffic-simulator.git
cd austin-traffic-simulator

2. Obtain and configure Google Maps API Key:

Go to the Google Cloud Console.

Enable Maps JavaScript API.

Create a new API key.

Open frontend/index.html and replace the placeholder YOUR_GOOGLE_MAPS_API_KEY with your key.

3. Create Python environment

python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

6. Fetch & preprocess data

cd src
python fetch_metadata.py       # downloads and saves full detector_locations.csv
python merge_metadata.py       # merges with traffic data → traffic_with_loc.csv

7. Run backend API

cd ../backend
python app.py                  # serves http://127.0.0.1:5000/traffic?time=...

8. Launch front‑end

cd ../frontend
python3 -m http.server 8000    # serves index.html at http://127.0.0.1:8000

Open your browser to http://127.0.0.1:8000/index.html, pick a date/time, and click Load Prediction.

<h2>Dependencies & Versions</h2>

Library Version

Python >=3.8

pandas 1.4.x

numpy 1.22.x

statsmodels 0.13.x

Flask 2.1.x

flask-cors 3.0.x

sodapy 2.1.x

joblib 1.1.x

matplotlib 3.5.x

Note: If you add deep‑learning models, you may need tensorflow or torch.

<h2>Assumptions & Notes</h2>

All timestamps are normalized to UTC in the backend; the front‑end converts local picker values to UTC.

Geo‑coordinates are filtered to remove any sensors with missing lat/lon.

The ARIMA baseline models traffic volume per 15‑min bin; speed forecasting is planned for future work.

Plotting thousands of circles can impact browser performance; clustering or WebGL rendering is recommended for production.

<h2>License</h2>

MIT License

Copyright (c) 2025 Khanh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

