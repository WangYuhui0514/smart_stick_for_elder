from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st

# 设置页面标题
st.title("Smart Walking Stick for Elderly")

# 在侧边栏添加标签
st.sidebar.header("Functions")
acceleration_tag = st.sidebar.checkbox("Step Count")
heart_rate_tag = st.sidebar.checkbox("Heart Rate")
pressure_sensor_tag = st.sidebar.checkbox("Pressure Sensor")


# 假设我们有一些示例数据
def generate_data(
    frequency="H", start_date="2024-01-01", end_date="2024-06-01", column_name="Value"
):
    date_range = pd.date_range(start=start_date, end=end_date, freq=frequency)
    data = np.random.rand(len(date_range)) * 100  # 生成随机数据
    return pd.DataFrame({"DateTime": date_range, column_name: data})


# 加速数据
accel_data = generate_data("H", "2024-01-01", "2024-06-01", "Acceleration")

# 从CSV文件加载心率数据
heart_rate_data = pd.read_csv("heart_rate_data.csv")
# 确保DateTime列存在并转换为日期格式
if "Time" in heart_rate_data.columns and "HeartRate" in heart_rate_data.columns:
    heart_rate_data["Time"] = pd.to_datetime(heart_rate_data["Time"])
else:
    st.error("CSV文件中缺少 'Time' 或 'HeartRate' 列，请检查文件格式。")

# 压力数据
pressure_data = generate_data("H", "2024-01-01", "2024-06-01", "Pressure")

# 加速度页面
if acceleration_tag:
    st.header("Step Count")

    # 日历选择器
    selected_date = st.date_input("Select Date", value=datetime.now().date())

    # 筛选数据
    daily_accel_data = accel_data[accel_data["DateTime"].dt.date == selected_date]

    if not daily_accel_data.empty:
        st.line_chart(
            daily_accel_data.set_index("DateTime")["Acceleration"],
            width=0,
            height=0,
            use_container_width=True,
        )
    else:
        st.write("No data available for the selected date.")

# 心率页面
if heart_rate_tag:
    st.header("Heart Rate Data")

    # 创建三列布局
    col1, col2, col3 = st.columns([2, 0.2, 2])

    with col1:
        start_date = st.date_input("Select Start Date", value=datetime(2024, 10, 15))

    with col2:
        st.markdown(
            "<div style='text-align: center; padding-top: 35px;'>-</div>",
            unsafe_allow_html=True,
        )

    with col3:
        end_date = st.date_input("Select End Date", value=datetime(2024, 10, 30))

    # 选择时间粒度
    granularity = st.selectbox("Select Frequency", ["Minute", "Hour", "Day"])

    # 根据用户选择的日期范围筛选数据
    filtered_data = heart_rate_data[
        (heart_rate_data["Time"] >= pd.to_datetime(start_date))
        & (heart_rate_data["Time"] <= pd.to_datetime(end_date))
    ]

    # 根据选择的频率调整数据
    if granularity == "Minute":
        # 保持数据为分钟级别
        plot_data = filtered_data
    elif granularity == "Hour":
        # 每小时平均心率
        plot_data = (
            filtered_data.set_index("Time")
            .resample("H")["HeartRate"]
            .mean()
            .reset_index()
        )
    else:
        # 每日平均心率
        plot_data = (
            filtered_data.set_index("Time")
            .resample("D")["HeartRate"]
            .mean()
            .reset_index()
        )

    # 绘制折线图
    if not plot_data.empty:
        st.line_chart(
            plot_data.set_index("Time")["HeartRate"],
            width=0,
            height=0,
            use_container_width=True,
        )
    else:
        st.write("No heart rate data available for the selected period.")

    # 计算并显示选定时间段内的平均心率
    avg_heart_rate = plot_data["HeartRate"].mean()
    st.write(
        f"Average Heart Rate for Selected Period ({granularity}-level): {avg_heart_rate:.2f}"
    )

    # 显示过去几天的平均心率表格
    daily_avg_heart_rate = (
        filtered_data.set_index("Time").resample("D")["HeartRate"].mean().reset_index()
    )
    st.write("Daily Average Heart Rate for Selected Period")
    st.table(daily_avg_heart_rate[["Time", "HeartRate"]])


# 压力传感器页面
if pressure_sensor_tag:
    st.header("Pressure Sensor Data")

    # 显示过去小时级的平均压力
    st.write("Average Pressure Sensor Data (Hourly)")
    avg_pressure = (
        pressure_data.set_index("DateTime").resample("H").mean().reset_index()
    )
    st.line_chart(
        avg_pressure.set_index("DateTime")["Pressure"],
        width=0,
        height=0,
        use_container_width=True,
    )
