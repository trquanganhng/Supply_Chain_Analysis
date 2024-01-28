import SupplyChainAnalysis

def main():
    while True:
        print("============================")
        print("1. Analyze Shipping Times")
        print("2. Analyze Late Delivery Risk")
        print("3. Distribution of Customer Segments")
        print("4. Distribution of Category")
        print("5. Distribution of Department")
        print("6. Category-Department Correlation")
        print("7. Bubble Map of Orders by Region")
        print("8. Visualize Orders and Sales")
        print("9. Analyze Profitability")
        print("10. Segment Customers by Sales")
        print("11. Analyze Product Performance")
        print("12. Analyze Indicators Over a Period of Time")
        print("0. Exit")
        print("============================")

        choice = input("Enter your choice: ")

        if choice == '0':
            print("Exiting...")
            break
        elif choice == '1':
            SupplyChainAnalysis.analyze_shipping_times()
        elif choice == '2':
            SupplyChainAnalysis.analyze_late_delivery_risk()
        elif choice == '3':
            SupplyChainAnalysis.distribution_Customer_Segments()
        elif choice == '4':
            SupplyChainAnalysis.distribution_Category()
        elif choice == '5':
            SupplyChainAnalysis.distribution_Department()
        elif choice == '6':
            SupplyChainAnalysis.Category_Department()
        elif choice == '7':
            SupplyChainAnalysis.bublemap_orders_by_region()
        elif choice == '8':
            SupplyChainAnalysis.visualize_orders_sales()
        elif choice == '9':
            SupplyChainAnalysis.analyze_profitability()
        elif choice == '10':
            SupplyChainAnalysis.segment_customers_by_sales()
        elif choice == '11':
            SupplyChainAnalysis.analyze_product_performance()
        elif choice == '12':
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            print("----------------------------")
            if start_date.strip() == '':
                start_date = None
            if end_date.strip() == '':
                end_date = None
            SupplyChainAnalysis.analyze_time_period(start_date, end_date)
        else:
            print("Invalid choice. Please enter a number between 0 and 12.")

if __name__ == "__main__":
    main()