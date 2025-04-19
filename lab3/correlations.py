import streamlit as st
from utils import load_db
import seaborn as sns
import matplotlib.pyplot as plt

def show_correlations():
    df = load_db()

    numeric = df.select_dtypes(include='number')
    corr = numeric.corr()

    fig, ax = plt.subplots(figsize=(24, 14))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
    st.pyplot(fig)

