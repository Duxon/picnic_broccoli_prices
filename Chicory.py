import re
import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


directory = '/home/duxon/Downloads/attachments'

price_pattern = r'1\s+Witlof\s+=20\n500 gram\s+(\d+\.\d+)'
date_pattern = r'Received:.*\n.*(\d{0,2})\s+(\w+)\s+(\d{4})\s+\d{2}:\d{2}:\d{2}'

prices = []
dates = []

for filename in sorted(os.listdir(directory)):
    if filename.endswith('.eml'):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            file_content = file.read()
            price_match = re.search(price_pattern, file_content)
            date_match = re.search(date_pattern, file_content)
            if price_match and date_match:
                price = float(price_match.group(1).replace(',', '.'))
                prices = np.append(prices, price)

                day = date_match.group(1).lstrip('0')
                day = '1' if not day else day
                date_str = f"{day} {date_match.group(2)} {date_match.group(3)}"
                date_obj = datetime.strptime(date_str, '%d %b %Y')
                dates = np.append(dates, date_obj)

            else:
                print(f"Missing price or date in file: {filename}")


# Create a pandas DataFrame with dates as index and prices as values
data = pd.DataFrame({'Price': prices}, index=pd.to_datetime(dates))

# Resample the data using 'W' frequency for weeks and take the mean
weekly_data = data.resample('W').mean()


# %% Plot the weekly data
plt.plot(weekly_data.index, weekly_data['Price'], marker='o')
plt.xlabel('Date')
plt.ylabel('Price [€]')  # Updated ylabel with EUR symbol
plt.title('Chicory Price over time (Picnic delivery service)')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('broccoli_prices.png', dpi = 600)
