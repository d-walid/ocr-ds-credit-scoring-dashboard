import pkg_resources

libraries = [
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "plotly",
    "requests",
    "scikit-learn",
    "shap",
    "mlflow",
    "joblib",
    "flask",
    "lightgbm",
    "streamlit",
    "werkzeug"
]

for lib in libraries:
    try:
        version = pkg_resources.get_distribution(lib).version
        print(f"{lib}: {version}")
    except pkg_resources.DistributionNotFound:
        print(f"{lib} n'est pas installé.")
