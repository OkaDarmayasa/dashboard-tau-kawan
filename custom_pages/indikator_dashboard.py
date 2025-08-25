import streamlit as st
import pandas as pd
import json
import time
import plotly.express as px

from db import add_indikator, get_all_indikators
from utils import format_capaian

def admin_view():
    st.header("Dashboard Tau Kawan")

    data = get_all_indikators()
    if not data:
        st.info("Belum ada data indikator.")
        return

    df = pd.DataFrame(data, columns=[
        "Name", "Capaian", "Kategori", "Nilai", "Year", "Bukti"
    ])
    df.index = df.index + 1
    df["Capaian"] = df["Capaian"].apply(format_capaian)
    df["Nilai"] = df["Nilai"].apply(lambda x: json.loads(x)[0] if isinstance(x, str) else x)

    with st.expander("🔍 Filter Indikator", expanded=True):
        selected_years = st.multiselect("Filter Tahun", sorted(df["Year"].unique()))
        selected_kategori = st.multiselect("Filter Kategori", sorted(df["Kategori"].unique()))

        if selected_years:
            df = df[df["Year"].isin(selected_years)]
        if selected_kategori:
            df = df[df["Kategori"].isin(selected_kategori)]

    with st.expander("📋 Tabel Indikator", expanded=True):
        search_query = st.text_input("🔍 Search", "")
        if search_query:
            df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        st.dataframe(
            df,
            column_config={
                "Bukti": st.column_config.LinkColumn(
                    "Bukti", 
                    help="Klik untuk membuka tautan bukti",
                    validate=r"^https:",
                    display_text="Bukti", 
                ),
            },
            use_container_width=True
        )

    st.header("📊 Visualisasi Indikator")

    kategori_counts = df["Kategori"].value_counts().reset_index()
    kategori_counts.columns = ["Kategori", "Jumlah"]

    custom_colors = {
        "Sangat Baik": "#6FFFE9",
        "Baik": "#2BB7DA",
        "Cukup": "#4682B4",
        "Kurang": "#2F4F4F",
        "Sangat Kurang": "#5C4FC8",
    }

    fig_kategori_pie = px.pie(
        kategori_counts,
        names="Kategori",
        values="Jumlah",
        title="Proporsi Indikator Berdasarkan Kategori",
        hole=0.4
    )

    fig_kategori_pie.update_traces(
        textinfo="label+percent",
        textposition="outside",
        marker=dict(colors=[custom_colors.get(k, "#cccccc") for k in kategori_counts["Kategori"]]),
        hoverinfo="label+percent+value",
        showlegend=True
    )

    fig_kategori_pie.update_layout(
        annotations=[dict(text='Kategori', x=0.5, y=0.5, font_size=16, showarrow=False)],
        showlegend=True,
        margin=dict(t=40, b=40, l=0, r=0),
        font=dict(size=16)
    )

    st.plotly_chart(fig_kategori_pie, use_container_width=True)

def user_view():
    st.header("📌 Tambah Indikator Baru")

    if "indikator_success" not in st.session_state:
        st.session_state.indikator_success = False

    if st.session_state.indikator_success:
        st.success("Indikator berhasil ditambahkan!")
        time.sleep(2)
        st.session_state.indikator_success = False
        st.rerun()

    with st.form("indikator_form"):
        name = st.text_input("Nama Indikator")
        capaian = st.text_input("Capaian")
        kategori = st.text_input("Kategori")
        nilai = st.text_area("Nilai (JSON Array)", value="[100, 80, 60, 40, 0]")
        year = st.number_input("Tahun", min_value=2000, max_value=2100, value=2025)
        bukti = st.text_input("Bukti")

        submitted = st.form_submit_button("Tambah")
        if submitted:
            try:
                parsed_nilai = json.loads(nilai)
                add_indikator(name, capaian, kategori, parsed_nilai, year, bukti)
                st.session_state.indikator_success = True
                st.rerun()
            except json.JSONDecodeError:
                st.error("Format JSON tidak valid.")

    st.header("📊 Daftar Indikator")
    data = get_all_indikators()
    if data:
        df = pd.DataFrame(data, columns=[
            "Name", "Capaian", "Kategori", "Nilai", "Year", "Bukti"
        ])
        df.index = df.index + 1
        df["Capaian"] = df["Capaian"].apply(format_capaian)
        df["Nilai"] = df["Nilai"].apply(lambda x: json.loads(x)[0] if isinstance(x, str) else x)
        search_query = st.text_input("🔍 Search", "")
        if search_query:
            df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        st.dataframe(df)
    else:
        st.info("Belum ada indikator.")


def dashboard_view():
    # st.header("Dashboard Tau Kawan")

    data = get_all_indikators()
    if not data:
        st.info("Belum ada data indikator.")
        return

    # --- Dataset 1: For Pie Chart ---
    df1 = pd.DataFrame(data, columns=[
        "Name", "Capaian", "Kategori", "Nilai", "Year", "Bukti"
    ])
    df1.index = df1.index + 1
    df1["Capaian"] = df1["Capaian"].apply(format_capaian)
    df1["Nilai"] = df1["Nilai"].apply(lambda x: json.loads(x)[0] if isinstance(x, str) else x)

    # --- Dataset 2: Simulate another dataset (use df1.copy() or replace with real source) ---
    df2 = df1.copy()  # Replace this if you have a separate source

    custom_colors = {
        "Sangat Baik": "#6FFFE9",
        "Baik": "#2BB7DA",
        "Cukup": "#4682B4",
        "Kurang": "#2F4F4F",
        "Sangat Kurang": "#5C4FC8",
    }


    # === PIE CHART ===
    kategori_counts_1 = df1["Kategori"].value_counts().reset_index()
    kategori_counts_1.columns = ["Kategori", "Jumlah"]

    fig_pie = px.pie(
        kategori_counts_1,
        names="Kategori",
        values="Jumlah",
        title="Proporsi Indikator Berdasarkan Kategori",
        hole=0.4
    )
    fig_pie.update_traces(
        textinfo="label+percent",
        textposition="outside",
        marker=dict(colors=[custom_colors.get(k, "#cccccc") for k in kategori_counts_1["Kategori"]]),
        hoverinfo="label+percent+value",
        showlegend=True
    )
    fig_pie.update_layout(
        annotations=[dict(text='Kategori', x=0.5, y=0.5, font_size=16, showarrow=False)],
        margin=dict(t=40, b=40, l=0, r=0),
        font=dict(size=16)
    )

    # === BAR CHART ===
    kategori_counts_2 = df2["Kategori"].value_counts().reset_index()
    kategori_counts_2.columns = ["Kategori", "Jumlah"]

    fig_bar = px.bar(
        kategori_counts_2,
        x="Kategori",
        y="Jumlah",
        title="Jumlah Indikator per Kategori",
        color="Kategori",
        color_discrete_map=custom_colors
    )
    fig_bar.update_layout(
        margin=dict(t=40, b=40, l=0, r=0),
        font=dict(size=16)
    )

    # === Visualizations side by side ===
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 21 Indikator")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("📊 TLHP")
        st.plotly_chart(fig_bar, use_container_width=True)

    # === Filters side by side ===
    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        st.subheader("🎛️ Filter 21 Indikator")
        with st.expander("🔍 Filter untuk 21 Indikator", expanded=True):
            selected_years_1 = st.multiselect("Filter Tahun", sorted(df1["Year"].unique()), key="year1")
            selected_kategori_1 = st.multiselect("Filter Kategori", sorted(df1["Kategori"].unique()), key="kategori1")

            if selected_years_1:
                df1 = df1[df1["Year"].isin(selected_years_1)]
            if selected_kategori_1:
                df1 = df1[df1["Kategori"].isin(selected_kategori_1)]

    with filter_col2:
        st.subheader("🎛️ Filter TLHP")
        with st.expander("🔍 Filter untuk TLHP", expanded=True):
            selected_years_2 = st.multiselect("Filter Tahun", sorted(df2["Year"].unique()), key="year2")
            selected_kategori_2 = st.multiselect("Filter Kategori", sorted(df2["Kategori"].unique()), key="kategori2")

            if selected_years_2:
                df2 = df2[df2["Year"].isin(selected_years_2)]
            if selected_kategori_2:
                df2 = df2[df2["Kategori"].isin(selected_kategori_2)]