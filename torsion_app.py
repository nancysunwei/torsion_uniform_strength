import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. 页面配置与空天教学情境导入
# ==========================================
st.set_page_config(page_title="数智力学交互学案", layout="centered")

st.title("🚁 空天传动轴：轻量化与稳定性博弈")
st.markdown("""
**长空创新班《材料力学A》专属数字伴学资源** > **探究任务**：假设您正在为某型直升机设计尾桨传动轴。在保证最大切应力（强度）不变的前提下，请滑动下方“内外径比例”滑块，将实心轴“掏空”，观察材料分布与减重效果，并警惕薄壁结构的失稳风险！
---
""")

# ==========================================
# 2. 交互控制区：定义掏空程度 (alpha = d/D)
# ==========================================
st.header("⚙️ 截面拓扑优化调节")
st.caption("调整内径与外径的比例 α (alpha)。α=0 代表实心轴，α 越接近 1 代表管壁越薄。")

alpha = st.slider("内外径比例 α (d/D) 🔄", min_value=0.0, max_value=0.98, value=0.0, step=0.01)

st.divider()

# ==========================================
# 3. 后端引擎：等强度轻量化数理推导
# ==========================================
# 基准参数：假设实心轴直径为 100 mm，承受某固定扭矩
D_solid = 100.0
A_solid = np.pi * (D_solid**2) / 4

# 为了保证抗扭截面系数 W_t 相等（等强度设计）
# W_t_solid = W_t_hollow  => D_solid^3 = D_hollow^3 * (1 - alpha^4)
if alpha == 0:
    D_hollow = D_solid
    d_inner = 0.0
else:
    D_hollow = D_solid / (1 - alpha**4)**(1/3)
    d_inner = D_hollow * alpha

# 计算优化后的横截面积与减重比例
A_hollow = np.pi * (D_hollow**2 - d_inner**2) / 4
weight_saving = (A_solid - A_hollow) / A_solid * 100

# 壁厚计算
thickness = (D_hollow - d_inner) / 2

# ==========================================
# 4. 可视化空间：截面对比与应力分布
# ==========================================
st.subheader("⭕ 几何空间：截面形态动态演化")

fig_shapes = go.Figure()

# 绘制左侧：传统实心轴
fig_shapes.add_shape(type="circle",
    xref="x", yref="y",
    x0=-D_solid/2 - 60, y0=-D_solid/2,
    x1=D_solid/2 - 60, y1=D_solid/2,
    line_color="gray", fillcolor="lightgray"
)
fig_shapes.add_annotation(
    x=-60, y=0, text="传统实心轴", showarrow=False, 
    font=dict(size=14, color="black")
)

# 绘制右侧：等强度空心轴
fig_shapes.add_shape(type="circle",
    xref="x", yref="y",
    x0=-D_hollow/2 + 60, y0=-D_hollow/2,
    x1=D_hollow/2 + 60, y1=D_hollow/2,
    line_color="#1f77b4", fillcolor="#1f77b4"
)
# 挖空内部
if alpha > 0:
    fig_shapes.add_shape(type="circle",
        xref="x", yref="y",
        x0=-d_inner/2 + 60, y0=-d_inner/2,
        x1=d_inner/2 + 60, y1=d_inner/2,
        line_color="white", fillcolor="white"
    )

text_color = "white" if alpha < 0.8 else "black"
fig_shapes.add_annotation(
    x=60, y=0, text=f"优化空心轴<br>α={alpha:.2f}", showarrow=False, 
    font=dict(size=14, color=text_color)
)

# 布局设置 (包含强制中文字体族，解决方块乱码问题)
fig_shapes.update_layout(
    font=dict(family="Microsoft YaHei, SimHei, Arial, sans-serif"),
    xaxis=dict(range=[-140, 140], showgrid=False, zeroline=False, visible=False),
    yaxis=dict(range=[-100, 100], showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1),
    margin=dict(l=0, r=0, t=20, b=0),
    height=300,
    plot_bgcolor="white"
)
st.plotly_chart(fig_shapes, use_container_width=True)

# ==========================================
# 5. 核心数据仪表板与高阶工程警告
# ==========================================
col_data1, col_data2, col_data3 = st.columns(3)

with col_data1:
    st.metric(label="实心轴外径 (mm)", value=f"{D_solid:.1f}")
with col_data2:
    st.metric(label="等强度空心轴外径 (mm)", value=f"{D_hollow:.1f}", delta=f"+{(D_hollow-D_solid):.1f} mm外扩")
with col_data3:
    st.metric(label="✈️ 成功减重比例", value=f"{weight_saving:.1f} %", delta=f"节省 {weight_saving:.1f}% 材料", delta_color="inverse")

st.divider()

# 引入稳定性约束（系统思维疲劳的破局点）
st.subheader("⚠️ 工程极限与稳定性边界")

if alpha < 0.8:
    st.success(f"✅ **设计安全**：当前壁厚为 {thickness:.1f} mm。材料成功外移，既减轻了重量，又具备良好的抗局部失稳能力。")
    st.info("💡 **力学洞察**：您可以看到，内部原本处于低应力状态的“摸鱼”材料被剔除了，材料利用率大幅提升。")
elif 0.8 <= alpha < 0.92:
    st.warning(f"⚠️ **边缘警告**：当前壁厚降至 {thickness:.1f} mm！虽然满足强度要求，但壁厚较薄，在剧烈扭转或震动工况下，需开始关注管壁的皱折风险。")
else:
    st.error(f"🚨 **失稳危险 (Local Buckling)**：当前壁厚仅为 {thickness:.1f} mm！这已经变成了一根“易拉罐”管。虽然理论上最省材料，但在实际受扭时会瞬间发生**局部失稳**而失效。设计不合理！")
    st.markdown("> **工程师箴言**：极致的轻量化绝不是无底线的减薄。强度只是基础，**稳定性**才是悬在空天结构头顶的达摩克利斯之剑！")
