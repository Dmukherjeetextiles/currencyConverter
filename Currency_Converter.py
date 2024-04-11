import streamlit as st
from datetime import date
import requests

access_key = st.secrets["access_key"]

# Currency symbols dictionary (from Forbes article)
currency_symbols = {
    "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥",
    "AUD": "A$", "CAD": "C$", "CHF": "CHF", "CNY": "¥",
    "HKD": "HK$", "NZD": "NZ$", "SEK": "kr", "KRW": "₩",
    "INR": "₹"  # Add more symbols as needed...
}

# Function to get currency list with caching
@st.cache_data
def get_currency_list():
    url = f"http://api.currencylayer.com/list?access_key={access_key}"
    response = requests.get(url)
    data = response.json()
    return list(data["currencies"].keys())

# Function to perform currency conversion with error handling
def convert_currency(amount, from_currency, to_currency, conversion_date=None):
    endpoint = "convert"
    url = f"http://api.currencylayer.com/{endpoint}?access_key={access_key}&from={from_currency}&to={to_currency}&amount={amount}"

    if conversion_date:
        url += f"&date={conversion_date}"

    try:
        response = requests.get(url)
        data = response.json()

        if data["success"]:
            return data["result"]
        else:
            st.error(f"Error: {data['error']['info']}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

# Streamlit app
def main():
    st.title("Currency Converter")

    # Get currency list
    currencies = get_currency_list()

    # Amount input with validation
    amount = st.number_input("Amount", min_value=0.01, max_value=1e14, value=1.0)

    # Currency selection
    col1, col2 = st.columns(2)
    with col1:
        from_currency = st.selectbox("From", currencies)
    with col2:
        to_currency = st.selectbox("To", currencies, index=1)  # Default to second currency

    # Conversion date (default to current date)
    conversion_date = st.date_input("Conversion Date", value=date.today())

    # Convert button with loading indicator
    if st.button("Convert"):
        with st.spinner("Converting..."):
            result = convert_currency(amount, from_currency, to_currency, conversion_date.strftime("%Y-%m-%d"))
        if result:
            from_symbol = currency_symbols.get(from_currency, from_currency)
            to_symbol = currency_symbols.get(to_currency, to_currency)
            st.success(f"{to_symbol} {result:.2f}") 

if __name__ == "__main__":
    main()
