# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    get sales figures input from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 4,76,7,90,4,10 etc\n")

        data_str = input ("Enter your data here: ")
 
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data



def validate_data(values):
    """
    Inside the try, conversts all string values into ints. 
    Raises ValueError if strings cannot be convered into int, 
    or if there arent exactyl 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) !=6:
            raise ValueError(
                f"Exactly 6 values are required, you provided only {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True


def update_sales_worksheet(data):
    """
    update sales worksheet add new row with the list adata provided
    """
    print("updatign sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    comapare sales with stock anc calculate the surplus for each item type.
    The surplus is defined as the salfe figure subtracted from the stock:
    - positive surplis indicates waste
    - negative surplus indicates extra made when stock was sold out.
    """
    print("Caluclating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

print("Welcome to LoveSandwicehes Data Automation")
main()