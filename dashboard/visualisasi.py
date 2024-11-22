import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
first_final_dataset = pd.read_csv("data_1.csv")
second_final_dataset = pd.read_csv("data_2.csv")


second_problem_df = (
    second_final_dataset.query("order_status == 'delivered'")
    .groupby(by="customer_city")
    .agg(city_frequency=("customer_city", "count"))
    .sort_values(by="city_frequency", ascending=False)
)

# Vis no 1
first_final_dataset['purchase_frequency'] = first_final_dataset.groupby('product_category_name_english')['product_category_name_english'].transform('count')


purchase_frequency_filter = st.selectbox(
    "Pilih Rentang Purchase Frequency",
    ["1000 - 2000", "2001 - 3000", "3001 - 4000", "4001 - 5000", "> 5000"]
)


if purchase_frequency_filter == "1000 - 2000":
    min_freq, max_freq = 1000, 2000
elif purchase_frequency_filter == "2001 - 3000":
    min_freq, max_freq = 2001, 3000
elif purchase_frequency_filter == "3001 - 4000":
    min_freq, max_freq = 3001, 4000
elif purchase_frequency_filter == "4001 - 5000":
    min_freq, max_freq = 4001, 5000
else:  
    min_freq, max_freq = 5001, float('inf')


rating_filter = st.selectbox(
    "Pilih Rentang Rating",
    ["<= 2", "3 - 4", "> 4"]
)


if rating_filter == "<= 2":
    min_rating, max_rating = float('-inf'), 2
elif rating_filter == "3 - 4":
    min_rating, max_rating = 3, 3.9
else:  
    min_rating, max_rating = 4, 5


first_problem_df = (
    first_final_dataset.groupby(by="product_category_name_english").agg(
        purchase_frequency=("product_category_name_english", "count"),
        average_review_score=("review_score", lambda x: round(x.mean(), 2))
    )
)


filtered_data = first_problem_df[
    (first_problem_df['purchase_frequency'] >= min_freq) &
    (first_problem_df['purchase_frequency'] <= max_freq) &
    (first_problem_df['average_review_score'] >= min_rating) &
    (first_problem_df['average_review_score'] <= max_rating)
].sort_values(by="purchase_frequency", ascending=False)


if filtered_data.empty:
    st.write("Tidak ada data yang sesuai dengan filter yang dipilih.")
else:

    st.header(f"Analisis Kategori Produk ({purchase_frequency_filter} - {rating_filter})")
    st.write(f"Produk dengan frekuensi pembelian dalam rentang {purchase_frequency_filter} dan rating dalam rentang {rating_filter}.")


    fig, ax = plt.subplots(figsize=(15, 6))
    bars = ax.barh(
        filtered_data.index,
        filtered_data["purchase_frequency"],
        color="skyblue",
        edgecolor="black"
    )

 
    for bar in bars:
        ax.text(
            bar.get_width() + 100,  
            bar.get_y() + bar.get_height() / 2,
            f"{int(bar.get_width())}", 
            va="center",
            fontsize=10
        )

    ax.set_title(f"Produk dengan frekuensi pembelian dalam rentang {purchase_frequency_filter} dan rating dalam rentang {rating_filter}", fontsize=14)
    ax.set_xlabel("Frekuensi Pembelian", fontsize=12)
    ax.set_ylabel("Kategori Produk", fontsize=12)
    ax.grid(axis="x", linestyle="--", alpha=0.7)

    plt.tight_layout()
    st.pyplot(fig)

st.write("Ringkasan Dataset Sebelum Filter:")
st.write(first_problem_df.describe())
st.write("Data Contoh Sebelum Filter:")
st.write(first_problem_df.head())


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
