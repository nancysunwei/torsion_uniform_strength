import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. 頁面配置與空天教學情境導入
# ==========================================
st.set_page_config(page_title="數智力學交互學案", layout="centered")

st.title("🚁 空天傳動軸：輕量化與穩定性博弈")
st.markdown("""
**長空創新班《材料力學A》專屬數字伴學資源** > **探究任務**：假設您正在為某型直升機設計尾槳傳動軸。在保證最大切應力（強度）不變的前提下，請滑動下方「內外徑比例」滑塊，將實心軸「掏空」，觀察材料分佈與減重效果，並警惕薄壁結構的失穩風險！
---
""")

# ==========================================
# 2. 交互控制區：定義掏空程度 (alpha = d/D)
# ==========================================
st.header("⚙️ 截面拓撲優化調節")
st.caption("調整內徑與外徑的比例 α (alpha)。α=0 代表實心軸，α 越接近 1 代表管壁越薄。")

alpha = st.slider("內外徑比例 α (d/D) 🔄", min_value=0.0, max_value=0.98, value=0.0, step=0.01)

st.divider()

# ==========================================
# 3. 後端引擎：等強度輕量化數理推導
# ==========================================
# 基準參數：假設實心軸直徑為 100 mm，承受某固定扭矩
D_solid = 100.0
A_solid = np.pi * (D_solid**2) / 4

# 為了保證抗扭截面係數 W_t 相等（等強度設計）
# W_t_solid = W_t_hollow  => D_solid^3 = D_hollow^3 * (1 - alpha^4)
if alpha == 0:
    D_hollow = D_solid
    d_inner = 0.0
else:
    D_hollow = D_solid / (1 - alpha**4)**(1/3)
    d_inner = D_hollow * alpha

# 計算優化後的橫截面積與減重比例
A_hollow = np.pi * (D_hollow**2 - d_inner**2) / 4
weight_saving = (A_solid - A_hollow) / A_solid * 100

# 壁厚計算
thickness = (D_hollow - d_inner) / 2

# ==========================================
# 4. 可視化空間：截面對比與應力分佈
# ==========================================
st.subheader("⭕ 幾何空間：截面形態動態演化")

fig_shapes = go.Figure()

# 繪製左側：傳統實心軸
fig_shapes.add_shape(type="circle",
    xref="x", yref="y",
    x0=-D_solid/2 - 60, y0=-D_solid/2,
    x1=D_solid/2 - 60, y1=D_solid/2,
    line_color="gray", fillcolor="lightgray"
)
fig_shapes.add_annotation(x=-60, y=0, text="傳統實心軸", showarrow=False, font=dict(size=14, color="black"))

# 繪製右側：等強度空心軸
fig_shapes.add_shape(type="circle",
    xref="x", yref="y",
    x0=-D_hollow/2 + 60, y0=-D_hollow/2,
    x1=D_hollow/2 + 60, y1=D_hollow/2,
    line_color="#1f77b4", fillcolor="#1f77b4"
)
# 挖空內部
if alpha > 0:
    fig_shapes.add_shape(type="circle",
        xref="x", yref="y",
        x0=-d_inner/2 + 60, y0=-d_inner/2,
        x1=d_inner/2 + 60, y1=d_inner/2,
        line_color="white", fillcolor="white"
    )
fig_shapes.add_annotation(x=60, y=0, text=f"優化空心軸\nα={alpha:.2f}", showarrow=False, font=dict(size=14, color="white" if alpha<0.8 else "black"))

# 佈局設置
fig_shapes.update_layout(
    xaxis=dict(range=[-140, 140], showgrid=False, zeroline=False, visible=False),
    yaxis=dict(range=[-100, 100], showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1),
    margin=dict(l=0, r=0, t=20, b=0),
    height=300,
    plot_bgcolor="white"
)
st.plotly_chart(fig_shapes, use_container_width=True)

# ==========================================
# 5. 核心數據儀表板與高階工程警告
# ==========================================
col_data1, col_data2, col_data3 = st.columns(3)

with col_data1:
    st.metric(label="實心軸外徑 (mm)", value=f"{D_solid:.1f}")
with col_data2:
    st.metric(label="等強度空心軸外徑 (mm)", value=f"{D_hollow:.1f}", delta=f"+{(D_hollow-D_solid):.1f} mm外擴")
with col_data3:
    st.metric(label="✈️ 成功減重比例", value=f"{weight_saving:.1f} %", delta=f"節省 {weight_saving:.1f}% 材料", delta_color="inverse")

st.divider()

# 引入穩定性約束（系統思維疲勞的破局點）
st.subheader("⚠️ 工程極限與穩定性邊界")

if alpha < 0.8:
    st.success(f"✅ **設計安全**：當前壁厚為 {thickness:.1f} mm。材料成功外移，既減輕了重量，又具備良好的抗局部失穩能力。")
    st.info("💡 **力學洞察**：您可以看到，內部原本處於低應力狀態的「摸魚」材料被剔除了，材料利用率大幅提升。")
elif 0.8 <= alpha < 0.92:
    st.warning(f"⚠️ **邊緣警告**：當前壁厚降至 {thickness:.1f} mm！雖然滿足強度要求，但壁厚較薄，在劇烈扭轉或震動工況下，需開始關注管壁的皺摺風險。")
else:
    st.error(f"🚨 **失穩危險 (Local Buckling)**：當前壁厚僅為 {thickness:.1f} mm！這已經變成了一根「易拉罐」管。雖然理論上最省材料，但在實際受扭時會瞬間發生**局部失穩**而失效。設計不合理！")
    st.markdown("> **工程師箴言**：極致的輕量化絕不是無底線的減薄。強度只是基礎，**穩定性**才是懸在空天結構頭頂的達摩克利斯之劍！")
