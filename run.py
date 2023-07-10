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

"""
def update_sales_worksheet(data):
    
    'update sales worksheet add new row with the list adata provided'
    
    print("updatign sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

def update_surplus_worksheet(data):
    
    'update surplus worksheet add new row with the list adata provided'
    
    print("updating SURPLUS worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated successfully.\n")
Refactoring above
"""

def update_worksheet(data, worksheet):
    """ 
    Recieves a list of ints to be instrted into a worksheet
    Update the relevant worksheet with data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully!\n")


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

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting the
    last 5 entries for each sandwich and retunrs the sata as a list
    of lists
    """
    sales = SHEET.worksheet("sales")
 

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns

def calculate_stock_data(data):
    """
    calculate the average stock for each item +10%
    """
    print("calculating stock data...\n")
    new_stock_data =[]

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("Welcome to LoveSandwicehes Data Automation")
main()

# student writes function
def get_stock_values(data):
    """
    Print out the calculated stock numbers for each sandwich type.
    """
    headings = SHEET.worksheet("stock").get_all_values()[0]

    # headings = SHEET.worksheet('stock').row_values(1)

    print("Make the following numbers of sandwiches for next market:\n")

    # new_data = {}
    # for heading, stock_num in zip(headings, data):
    #     new_data[heading] = stock_num
    # return new_data
    
    return {heading: data for heading, data in zip(headings, data)}
    
stock_values = get_stock_values(stock_data)
print(stock_values)
