import pandas as pd
from googletrans import Translator

df = pd.read_csv('DataCoSupplyChainDataset.csv', encoding='ISO-8859-1')

## clean columns 'shipping date (DateOrders)' and 'order date (DateOrders)'
def clean_sDate_oDate():
    # Convert date columns to datetime objects
    df['shipping date (DateOrders)'] = pd.to_datetime(df['shipping date (DateOrders)'])
    df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'])
    
    # Update Days for shipping (real)
    df['Days for shipping (real)'] = (df['shipping date (DateOrders)'] - df['order date (DateOrders)']).dt.days
    
    # Remove negative values and replace them with 0
    df['Days for shipping (real)'] = df['Days for shipping (real)'].apply(lambda x: max(x, 0))
    df['Days for shipment (scheduled)'] = df['Days for shipment (scheduled)'].apply(lambda x: max(x, 0))

    return df

## clean column Order Country
def translate_country_names():
    # Use googletrans to translate the values of this column from spanish to english
    translator = Translator()
    translated_countries = {}

    for country in df['Order Country'].unique():
        translated_country = translator.translate(country, src='es', dest='en').text
        translated_countries[country] = translated_country
    df['Order Country'] = df['Order Country'].map(translated_countries)

    return df

if __name__ == "__main__":
    csv_file = "DataCoSupplyChainDataset.csv"  
    cleaned_df = clean_sDate_oDate()
    translated_df = translate_country_names(cleaned_df)
    # Create new file to save cleaned Data
    cleaned_file = "cleaned_" + csv_file
    translated_df.to_csv(cleaned_file, index=False)
    
    print(f"Data cleaning and translation complete. Cleaned file saved as: {cleaned_file}")