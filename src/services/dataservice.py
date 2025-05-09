import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


# DataService class to handle data loading, processing, and exporting.
class DataService:
    def __init__(self):
        self.input_file = "../data/raw/sales.csv"
        self.output_file = "../data/interim/sales_calc.csv"
        self.data = None
        self.report = None

    def load_data(self):
        self.data = pd.read_csv(self.input_file)

    def process_data(self):
        self.data["total_sales"] = self.data["quantity"] * self.data["price"]

    def export_data(self):
        self.data.to_csv(self.output_file, index=False)

    def generate_report(self):
        report = (
            self.data.groupby("product")
            .agg({"quantity": "sum", "total_sales": "sum"})
            .reset_index()
        )
        report["avg_price"] = report["total_sales"] / report["quantity"]
        self.report = report
        report.to_csv("../data/processed/sales_report.csv", index=False)
        print("Sales Report generated!")

    def configure_plot_style(self):
        mpl.style.use("default")  # ("seaborn")
        mpl.rcParams["figure.dpi"] = 200

    def generate_chart(self):
        self.configure_plot_style()
        report = pd.read_csv("../data/processed/sales_report.csv")
        products = report["product"]
        total_sales = report["total_sales"]

        plt.figure(figsize=(8, 6))
        plt.bar(products, total_sales)
        plt.xlabel("Product")
        plt.ylabel("Total Sales")
        plt.title("Sales by Product")
        plt.tight_layout()
        plt.savefig("../figures/sales_chart.png")
        print("Sales chart generated! (figures/sales_chart.png)")

    def run(self):
        self.load_data()
        self.process_data()
        self.export_data()
        self.generate_report()
        self.generate_chart()
        print("Data processed and exported to {self.output_file}")
