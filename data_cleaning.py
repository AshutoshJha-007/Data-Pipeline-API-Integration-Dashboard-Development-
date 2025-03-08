import pandas as pd
import logging
import os

# Logging setup
logging.basicConfig(
    filename="data_cleaning.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DataCleaner:
    def __init__(self, input_file, output_file="cleaned_data.csv"):
        self.input_file = input_file
        self.output_file = output_file

    def load_data(self):
        """ Load CSV file into a Pandas DataFrame """
        try:
            df = pd.read_csv(self.input_file)
            logging.info(f"Loaded data from {self.input_file}. Shape: {df.shape}")
            return df
        except FileNotFoundError:
            logging.error(f"File {self.input_file} not found.")
            raise
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise

    def remove_duplicates(self, df):
        """ Remove duplicate rows """
        before = df.shape[0]
        df = df.drop_duplicates()
        after = df.shape[0]
        logging.info(f"Removed {before - after} duplicate rows.")
        return df

    def handle_missing_values(self, df, strategy="drop"):
        """ Handle missing values """
        before = df.shape[0]
        if strategy == "drop":
            df = df.dropna()
        elif strategy == "fill":
            df = df.fillna(df.median())  # Fill with median values
        after = df.shape[0]
        logging.info(f"Missing values handled using {strategy}. Rows before: {before}, After: {after}")
        return df

    def validate_data(self, df):
        """ Apply data validation rules """
        before = df.shape[0]

        # Example: Remove negative values from a specific column
        if "value_column" in df.columns:
            df = df[df["value_column"] >= 0]

        # Example: Keep only valid names (non-empty)
        if "name" in df.columns:
            df = df[df["name"].str.strip() != ""]

        after = df.shape[0]
        logging.info(f"Data validation applied. Rows before: {before}, After: {after}")
        return df

    def generate_summary_report(self, df):
        """ Generate a quick summary of cleaned data """
        report = {
            "Total Rows": df.shape[0],
            "Total Columns": df.shape[1],
            "Missing Values": df.isnull().sum().to_dict(),
            "Column Data Types": df.dtypes.to_dict()
        }
        logging.info(f"Summary Report: {report}")
        return report

    def save_cleaned_data(self, df):
        """ Save the cleaned data to CSV """
        df.to_csv(self.output_file, index=False)
        logging.info(f"Cleaned data saved to {self.output_file}.")

    def clean_data_pipeline(self):
        """ Full Cleaning Pipeline """
        logging.info("Starting data cleaning pipeline...")
        df = self.load_data()
        df = self.remove_duplicates(df)
        df = self.handle_missing_values(df, strategy="drop")
        df = self.validate_data(df)
        report = self.generate_summary_report(df)
        self.save_cleaned_data(df)
        logging.info("Data cleaning pipeline completed successfully.")
        return report

# Run the script
if __name__ == "__main__":
    cleaner = DataCleaner("raw_data.csv")
    report = cleaner.clean_data_pipeline()
    print("Cleaning complete. Summary report generated.")
