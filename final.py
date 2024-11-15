from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

# 页面设置
st.set_page_config(page_title="Smart Walking Stick for Elderly", layout="wide")

# 侧边栏功能
st.sidebar.header("🔧 Functions")
acceleration_tag = st.sidebar.checkbox("📊 Step Count")
heart_rate_tag = st.sidebar.checkbox("❤️ Heart Rate")
pressure_sensor_tag = st.sidebar.checkbox("💪 Pressure Sensor")

# 检查是否有功能被选择
is_function_selected = any([acceleration_tag, heart_rate_tag, pressure_sensor_tag])

# 居中页面标题并添加描述
if not is_function_selected:
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>🌟 Smart Walking Stick for Elderly</h1>
            <p>Monitor real-time <strong>Step Count</strong>, <strong>Heart Rate</strong>, and <strong>Pressure</strong> data to support elder mobility and health.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image("4.jpg", width=1400)

# 从CSV文件加载数据
data_file = "data.csv"  # 确保该文件包含Time, HeartRate, steps, force列
data = pd.read_csv(data_file)

# 确保 Time 列存在并转换为日期格式
if "Time" in data.columns:
    data["Time"] = pd.to_datetime(data["Time"])
else:
    st.error("CSV文件中缺少 'Time' 列，请检查文件格式。")

# 样式和CSS
st.markdown(
    """
    <style>
        .stAlert {
            background-color: #f9f9f9;
        }
        .css-1d391kg {
            font-size: 18px;
        }
        .st-bb {
            font-weight: bold;
            font-size: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 功能展示：步数页面
if acceleration_tag:
    st.header("📊 Step Count Data")
    st.markdown(
        "### Explore the step count data with customization options for date range and granularity."
    )

    # 选择起始和终止日期
    col1, col2, col3 = st.columns([2, 0.2, 2])
    with col1:
        start_date = st.date_input(
            "Select Start Date", value=datetime(2024, 10, 15), key="start_date_step"
        )
    with col2:
        st.markdown(
            "<div style='text-align: center; padding-top: 35px;'>-</div>",
            unsafe_allow_html=True,
        )
    with col3:
        end_date = st.date_input(
            "Select End Date", value=datetime(2024, 10, 30), key="end_date_step"
        )

    # 选择时间粒度
    granularity = st.selectbox(
        "Select Frequency", ["Minute", "Hour", "Day"], key="granularity_step"
    )

    # 筛选步数数据
    filtered_data = data[
        (data["Time"] >= pd.to_datetime(start_date))
        & (data["Time"] <= pd.to_datetime(end_date))
    ]

    # 计算数据频率
    if granularity == "Minute":
        plot_data = filtered_data[["Time", "steps"]]
    elif granularity == "Hour":
        plot_data = (
            filtered_data.set_index("Time").resample("H")["steps"].sum().reset_index()
        )
    else:
        plot_data = (
            filtered_data.set_index("Time").resample("D")["steps"].sum().reset_index()
        )

    # 步数柱状图
    st.subheader("Regular Step Count")
    if not plot_data.empty:
        st.bar_chart(
            plot_data.set_index("Time")["steps"],
            width=0,
            height=400,
            use_container_width=True,
        )
    else:
        st.write("No step count data available for the selected period.")

    # 累计步数折线图
    st.subheader("Daily Step Count Trend (Cumulative)")
    specific_date = st.date_input(
        "Select Specific Date for Trend",
        value=datetime(2024, 10, 15),
        key="specific_date_step",
    )
    trend_granularity = st.selectbox(
        "Select Trend Granularity", ["Minute", "Hour"], key="trend_granularity_step"
    )

    # 累计数据处理
    trend_data = filtered_data[filtered_data["Time"].dt.date == specific_date]
    if trend_granularity == "Minute":
        trend_plot_data = trend_data[["Time", "steps"]]
    else:
        trend_plot_data = (
            trend_data.set_index("Time").resample("H")["steps"].sum().reset_index()
        )
    trend_plot_data["Cumulative Steps"] = trend_plot_data["steps"].cumsum()

    # 显示累计步数折线图
    if not trend_plot_data.empty:
        st.line_chart(
            trend_plot_data.set_index("Time")["Cumulative Steps"],
            width=0,
            height=400,
            use_container_width=True,
        )
    else:
        st.write("No step count data available for the selected date and granularity.")

# 心率页面
if heart_rate_tag:
    st.header("❤️ Heart Rate Data")
    st.markdown("### Monitor real-time heart rate data to assess health status.")

    # 日期选择
    col1, col2, col3 = st.columns([2, 0.2, 2])
    with col1:
        start_date = st.date_input(
            "Select Start Date", value=datetime(2024, 10, 15), key="start_date_hr"
        )
    with col2:
        st.markdown(
            "<div style='text-align: center; padding-top: 35px;'>-</div>",
            unsafe_allow_html=True,
        )
    with col3:
        end_date = st.date_input(
            "Select End Date", value=datetime(2024, 10, 30), key="end_date_hr"
        )

    # 时间粒度
    granularity = st.selectbox(
        "Select Frequency", ["Minute", "Hour", "Day"], key="granularity_hr"
    )

    # 数据处理
    filtered_data = data[
        (data["Time"] >= pd.to_datetime(start_date))
        & (data["Time"] <= pd.to_datetime(end_date))
    ]
    if granularity == "Minute":
        plot_data = filtered_data[["Time", "HeartRate"]]
    elif granularity == "Hour":
        plot_data = (
            filtered_data.set_index("Time")
            .resample("H")["HeartRate"]
            .mean()
            .reset_index()
        )
    else:
        plot_data = (
            filtered_data.set_index("Time")
            .resample("D")["HeartRate"]
            .mean()
            .reset_index()
        )

    # 心率折线图
    if not plot_data.empty:
        st.line_chart(
            plot_data.set_index("Time")["HeartRate"],
            width=0,
            height=400,
            use_container_width=True,
        )
    else:
        st.write("No heart rate data available for the selected period.")

# 压力传感器页面
if pressure_sensor_tag:
    st.header("💪 Pressure Sensor Data")
    st.markdown("### View pressure sensor data to gauge support usage and intensity.")

    # 日期选择
    col1, col2, col3 = st.columns([2, 0.2, 2])
    with col1:
        start_date = st.date_input(
            "Select Start Date", value=datetime(2024, 10, 15), key="start_date_pressure"
        )
    with col2:
        st.markdown(
            "<div style='text-align: center; padding-top: 35px;'>-</div>",
            unsafe_allow_html=True,
        )
    with col3:
        end_date = st.date_input(
            "Select End Date", value=datetime(2024, 10, 30), key="end_date_pressure"
        )

    # 时间粒度
    granularity = st.selectbox(
        "Select Frequency", ["Minute", "Hour", "Day"], key="granularity_pressure"
    )

    # 数据处理
    filtered_data = data[
        (data["Time"] >= pd.to_datetime(start_date))
        & (data["Time"] <= pd.to_datetime(end_date))
    ]
    if granularity == "Minute":
        plot_data = filtered_data[["Time", "force"]]
    elif granularity == "Hour":
        plot_data = (
            filtered_data.set_index("Time").resample("H")["force"].mean().reset_index()
        )
    else:
        plot_data = (
            filtered_data.set_index("Time").resample("D")["force"].mean().reset_index()
        )

    # 压力柱状图
    if not plot_data.empty:
        st.bar_chart(
            plot_data.set_index("Time")["force"],
            width=0,
            height=400,
            use_container_width=True,
        )
    else:
        st.write("No pressure data available for the selected period.")
