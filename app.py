import streamlit as st

# Thiết lập cấu hình trang
st.set_page_config(
    page_title="Tính Lãi Gửi Tiết Kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Ứng Dụng Tính Lãi Gửi Tiết Kiệm")
st.write("Nhập thông tin khoản tiền gửi của bạn để tính toán tiền lãi và tổng số tiền nhận được.")

st.markdown("---")

# --- FORM NHẬP THÔNG TIN ---
col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input(
        "Số tiền gửi (VNĐ):",
        min_value=1000000,
        value=100000000,
        step=1000000,
        format="%d"
    )

    ky_han_thang = st.number_input(
        "Kỳ hạn gửi (Tháng):",
        min_value=1,
        max_value=360,
        value=12,
        step=1
    )

    lai_suat_nam = st.number_input(
        "Lãi suất (%/năm):",
        min_value=0.1,
        max_value=30.0,
        value=6.0,
        step=0.1,
        format="%.1f"
    )

with col2:
    loai_lai = st.radio(
        "Phương thức tính lãi:",
        options=["Lãi đơn", "Lãi kép"],
        help="Lãi đơn: Tiền lãi không gộp gốc.\nLãi kép: Tiền lãi mỗi kỳ được gộp vào gốc để tính lãi kỳ tiếp theo."
    )

    hinh_thuc_tra_lai = st.selectbox(
        "Hình thức nhận lãi:",
        options=["Cuối kỳ", "Hàng tháng", "Hàng quý"]
    )

# --- XỬ LÝ LÝ THUYẾT & TÍNH TOÁN ---
# Quy đổi số kỳ trả lãi dựa vào hình thức
if hinh_thuc_tra_lai == "Hàng tháng":
    so_ky_per_nam = 12
    so_thang_per_ky = 1
elif hinh_thuc_tra_lai == "Hàng quý":
    so_ky_per_nam = 4
    so_thang_per_ky = 3
else:  # Cuối kỳ
    so_ky_per_nam = 12 / ky_han_thang
    so_thang_per_ky = ky_han_thang

# Tổng số kỳ trả lãi trong suốt thời gian gửi
tong_so_ky = ky_han_thang / so_thang_per_ky

# Tính toán chi tiết
if loai_lai == "Lãi đơn":
    # Lãi đơn = Gốc * Lãi suất năm * (Số tháng / 12)
    tong_tien_lai = so_tien_gui * (lai_suat_nam / 100) * (ky_han_thang / 12)
    tien_lai_dinh_ky = tong_tien_lai / tong_so_ky
    tong_tien_goc_lai = so_tien_gui + tong_tien_lai

else:  # Lãi kép
    lai_suat_moi_ky = (lai_suat_nam / 100) / so_ky_per_nam
    # Công thức lãi kép: A = P * (1 + r)^n
    tong_tien_goc_lai = so_tien_gui * ((1 + lai_suat_moi_ky) ** tong_so_ky)
    tong_tien_lai = tong_tien_goc_lai - so_tien_gui
    
    if hinh_thuc_tra_lai == "Cuối kỳ":
        tien_lai_dinh_ky = tong_tien_lai
    else:
        # Với lãi kép định kỳ, tiền lãi trung bình mỗi kỳ
        tien_lai_dinh_ky = tong_tien_lai / tong_so_ky

st.markdown("---")

# --- HIỂN THỊ KẾT QUẢ ---
st.subheader("📊 Kết quả tính toán")

# Định dạng hiển thị tiền VNĐ
def format_vnd(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric(
        label=f"Lãi mỗi kỳ ({hinh_thuc_tra_lai.lower()})" if hinh_thuc_tra_lai != "Cuối kỳ" else "Tiền lãi nhận được",
        value=format_vnd(tien_lai_dinh_ky)
    )

with m2:
    st.metric(
        label="Tổng tiền lãi",
        value=format_vnd(tong_tien_lai)
    )

with m3:
    st.metric(
        label="Tổng gốc + lãi",
        value=format_vnd(tong_tien_goc_lai)
    )

# --- BẢNG BẢNG TÓM TẮT THÔNG TIN ---
st.markdown("### 📝 Chi tiết khoản gửi")
st.json({
    "Số tiền gốc": format_vnd(so_tien_gui),
    "Kỳ hạn": f"{ky_han_thang} tháng",
    "Lãi suất": f"{lai_suat_nam}% / năm",
    "Phương thức": loai_lai,
    "Hình thức nhận lãi": hinh_thuc_tra_lai,
    "Tổng số kỳ nhận lãi": f"{tong_so_ky:.1f} kỳ"
})
