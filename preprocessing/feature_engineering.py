from sklearn.preprocessing import StandardScaler


def scale_features(df):

    scaler = StandardScaler()

    # Remove label column from scaling
    feature_columns = [
        col for col in df.columns
        if col != "label"
    ]

    numeric_columns = df[feature_columns].select_dtypes(
        include=['int64', 'float64']
    ).columns

    df[numeric_columns] = scaler.fit_transform(
        df[numeric_columns]
    )

    return df