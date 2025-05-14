# ───────────────────────────────────────────────
# 0. Imports & data load
# ───────────────────────────────────────────────
import pandas as pd
import plotly.express as px
import preswald

df = pd.read_csv("data/Superstore.csv")  # adjust path if needed

# ───────────────────────────────────────────────
# 1. Dashboard header & dataset overview
# ───────────────────────────────────────────────
preswald.text("# 📦 Superstore Sales Dashboard")

preswald.text("""
**Dataset:** 9,994 orders from a US office-supply retailer (2014-2017).  
**Key fields:**  
* *Sales* & *Profit* (USD)  
* *Discount* (0 – 0.8)  
* Hierarchies: Category ▸ Sub-Category ▸ Product  
* Customer *Segment* & geographic *Region*
""")

# ───────────────────────────────────────────────
# 2. Sales vs Profit  ▸ Scatter
# ───────────────────────────────────────────────
fig_sales_profit = px.scatter(
    df, x="Sales", y="Profit",
    opacity=0.5,
    title="Sales vs. Profit",
    labels={"Sales": "Sales (USD)", "Profit": "Profit (USD)"},
)
preswald.text("## 1️⃣ Sales vs Profit")
preswald.text("Shows whether high-revenue orders always generate high profit (spoiler: they don’t).")
preswald.plotly(fig_sales_profit)

# ───────────────────────────────────────────────
# 3. Sales by Category  ▸ Bar
# ───────────────────────────────────────────────
category_sales = df.groupby("Category", as_index=False)["Sales"].sum()

fig_category_sales = px.bar(
    category_sales, x="Category", y="Sales",
    text_auto=".2s",
    title="Total Sales by Category",
    labels={"Sales": "Total Sales (USD)"},
)
fig_category_sales.update_traces(marker_color="skyblue")
fig_category_sales.update_layout(xaxis_tickangle=0)

preswald.text("## 2️⃣ Total Sales by Category")
preswald.text("Technology edges out Office Supplies; Furniture trails in overall revenue.")
preswald.plotly(fig_category_sales)

# ───────────────────────────────────────────────
# 4. Profit Margin by Sub-Category  ▸ H-Bar
# ───────────────────────────────────────────────
df["Profit Margin"] = df["Profit"] / df["Sales"]
subcat_margin = (
    df.groupby("Sub-Category", as_index=False)["Profit Margin"]
      .mean()
      .sort_values("Profit Margin", ascending=False)
)

fig_profit_margin = px.bar(
    subcat_margin, x="Profit Margin", y="Sub-Category",
    orientation="h",
    text="Profit Margin",
    title="Average Profit Margin by Sub-Category",
    labels={"Profit Margin": "Profit Margin"},
    height=750,
)
fig_profit_margin.update_traces(
    marker_color="lightgreen",
    texttemplate="%{text:.2%}",
    textposition="outside",
)
fig_profit_margin.update_layout(yaxis={"categoryorder": "total ascending"})

preswald.text("## 3️⃣ Profit Margin by Sub-Category")
preswald.text("Highlights winners (Copiers) and losers (Tables) in profitability.")
preswald.plotly(fig_profit_margin)

# ───────────────────────────────────────────────
# 5. Discount vs Sales & Profit  ▸ Scatter
# ───────────────────────────────────────────────
fig_discount = px.scatter(
    df, x="Discount", y="Sales",
    color="Profit", color_continuous_scale="RdBu",
    opacity=0.55,
    title="Impact of Discount on Sales and Profit",
    labels={"Discount": "Discount", "Sales": "Sales (USD)", "Profit": "Profit (USD)"},
)

preswald.text("## 4️⃣ Discount Impact")
preswald.text("Blue = high profit, red = losses. Steep discounts (>50 %) often destroy margin.")
preswald.plotly(fig_discount)

# ───────────────────────────────────────────────
# 6. Regional Performance  ▸ Grouped Bar
# ───────────────────────────────────────────────
region_perf = (
    df.groupby("Region", as_index=False)[["Sales", "Profit"]].sum()
      .rename(columns={"Sales": "Total Sales", "Profit": "Total Profit"})
)

fig_region = px.bar(
    region_perf, x="Region", y=["Total Sales", "Total Profit"],
    barmode="group",
    text_auto=".2s",
    title="Sales vs Profit by Region",
)

preswald.text("## 5️⃣ Sales & Profit by Region")
preswald.text("West leads in both sales and profit; Central is the weakest region.")
preswald.plotly(fig_region)


# ───────────────────────────────────────────────
# 7. Closing snapshot
# ───────────────────────────────────────────────
preswald.text("### ✅ Key Takeaways")
preswald.text("""
* **Technology** drives revenue *and* margin; **Furniture Tables** are a drag.  
* Deep discounts erode profit—especially on large orders.  
* The **West** region is the profit engine; Central needs attention.  
* Seasonal peaks suggest Q4 promotions and inventory planning.  
""")
