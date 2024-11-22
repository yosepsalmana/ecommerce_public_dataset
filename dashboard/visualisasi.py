import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
first_final_dataset = pd.read_csv("./data_1.csv")
second_final_dataset = pd.read_csv("./data_2.csv")


first_problem_df = (
    first_final_dataset.groupby(by="product_category_name_english").agg(
        purchase_frequency=("product_category_name_english", "count"),
        average_review_score=("review_score", lambda x: round(x.mean(), 2))
    )
    .query("purchase_frequency > 5000 and average_review_score > 4.00")
    .sort_values(by="purchase_frequency", ascending=False)
)


second_problem_df = (
    second_final_dataset.query("order_status == 'delivered'")
    .groupby(by="customer_city")
    .agg(city_frequency=("customer_city", "count"))
    .sort_values(by="city_frequency", ascending=False)
)


## Visualisasi No.1
st.title("E-Commerce Public Dataset Dashboard")
st.header("1. Analisis Kategori Produk")
st.write("Produk dengan frekuensi pembelian >5000 dan rating > 4")

fig, ax = plt.subplots(figsize=(15, 6))
bars = ax.barh(
    first_problem_df.index,
    first_problem_df["purchase_frequency"],
    color="skyblue",
    edgecolor="black"
)

for bar, label in zip(bars, first_problem_df.index):
    ax.text(
        50,
        bar.get_y() + bar.get_height() / 2,
        label,
        va="center",
        ha="left",
        color="red", 
        fontsize=10
    )


for bar in bars:
    ax.text(
        bar.get_width() + 100,  
        bar.get_y() + bar.get_height() / 2,
        f"{int(bar.get_width())}", 
        va="center",
        fontsize=10
    )

ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Produk dengan frekuensi pembelian > 5000 dan rating > 4", fontsize=14)
ax.set_xlabel("Frekuensi Pembelian", fontsize=12)
ax.set_ylabel("Kategori Produk", fontsize=12)
ax.grid(axis="x", linestyle="--", alpha=0.7)

plt.tight_layout()
st.pyplot(fig)

## Visualisasi No.2
st.header("2. Analisis Kota Customer")
st.write("Kota dengan pembelian terbanyak")


top_cities = second_problem_df.head(5)

cmap = plt.cm.get_cmap("viridis", len(top_cities))
colors = [cmap(i) for i in range(len(top_cities))]

fig, ax = plt.subplots(figsize=(8, 8))

wedges, texts, autotexts = ax.pie(
    top_cities["city_frequency"],
    labels=None,
    autopct=lambda pct: f"{pct:.1f}%\n({int(pct/100.*top_cities['city_frequency'].sum())})",
    colors=colors, 
    textprops={'fontsize': 10, 'color': 'white'},  
)


ax.legend(
    handles=wedges,
    labels=list(top_cities.index),  
    loc='lower center',
    bbox_to_anchor=(0.5, -0.2),  
    ncol=len(top_cities), 
    frameon=False,  
    fontsize=10
)

ax.set_title("Top 5 Kota dengan Pembelian Terbanyak", fontsize=14)

st.pyplot(fig)
