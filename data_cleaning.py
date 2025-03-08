import pandas as pd

def clean_data(file_path):
    df = pd.read_csv(file_path)
    
    # Drop null and duplicate values
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    
    # Remove invalid entries
    df = df[df['value_column'] >= 0]
    
    df.to_csv("cleaned_data.csv", index=False)
    print("Data cleaned and saved as 'cleaned_data.csv'.")

# Example usage
if __name__ == "__main__":
    clean_data("raw_data.csv")
