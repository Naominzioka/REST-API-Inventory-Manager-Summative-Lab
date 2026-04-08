import argparse
from tabulate import tabulate
from handlers import add_product,restock_product, delete_product, fetch_product, view_products

class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_section(text, color):
    print(f"{color}{text}{Color.END}")

def main():
    cli_context = {} 

    parser = argparse.ArgumentParser(description="CLI Inventory Management System")
    subparsers = parser.add_subparsers(dest="command")

    # Add Product
    add_prod = subparsers.add_parser("add-product")
    add_prod.add_argument("name")
    add_prod.set_defaults(func=add_product)

    #View Products
    subparsers.add_parser("view-products").set_defaults(func=view_products)

    #Restock
    restock = subparsers.add_parser("restock-product")
    restock.add_argument("product_id", type=str)
    restock.add_argument("quantity", type=int)
    restock.set_defaults(func=restock_product)
    
    #Delete
    delete = subparsers.add_parser("delete-product")
    delete.add_argument("product_id", type=str)
    delete.set_defaults(func=delete_product)

    #FETCH FROM API (NEW)
    fetch = subparsers.add_parser("fetch-product")
    fetch.add_argument("barcode", type=str, help="The barcode to find via API")
    fetch.set_defaults(func=fetch_product)

    args = parser.parse_args()

    # Run argparse commands
    if hasattr(args, "func"):
        args.func(cli_context, args)
    else:
        print_section("CLI Inventory Management System", Color.BOLD + Color.GREEN)
        menu_options = [
            ["#", "Command", "Action"],
            ["1", "view-products", "View inventory"],
            ["2", "add-product", "Create manual entry"],
            ["3", "restock-product", "Increase stock levels"],
            ["4", "fetch-product", "Find & Import product via API"],
            ["5", "delete-product", "Remove from inventory"],
        ]
        
        print(tabulate(menu_options, headers="firstrow", tablefmt="simple"))
        print(f"\n{Color.YELLOW}💡 Hint: Use 'python cli.py fetch-product <barcode>' to add items.{Color.END}\n")

if __name__ == "__main__":
    main()