def load_data(file_or_db, table_name=None):
    try:
        if file_or_db.endswith(('.csv', '.xlsx')):
            # Load from spreadsheet
            if file_or_db.endswith('.csv'):
                return pd.read_csv(file_or_db)
            elif file_or_db.endswith('.xlsx'):
                return pd.read_excel(file_or_db)
        elif '://' in file_or_db:
            # Load from a database
            engine = create_engine(file_or_db)
            return pd.read_sql_query(f'SELECT * FROM {table_name}', con=engine)
        else:
            raise ValueError("Invalid file or database format")
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")