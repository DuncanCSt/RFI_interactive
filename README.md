# RFI_interactive
An interative data app powered by streamlit that analysis the RFI spectrum from
300 MHz to 1.6GHz from RFI monitor data on Oct 8th 2024.

## Setup

1. Create a new environment named `app_env` using Python 3.12:

   ```bash
   conda create -n app_env python=3.12
   ```
2. Activate the environment and install the required packages:

   ```bash
   conda activate app_env
   pip install -r requirements.txt
   ```
3. Launch the application:

   ```bash
   streamlit run app.py
   ```
