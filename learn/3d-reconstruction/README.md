# 3D 图像重建学习板块

> 专注：图像三维重建技术，从 NeRF 到 3DGS 及相关技术

---

## 📚 技术路线图

### 1. NeRF 系列（Neural Radiance Fields）
**核心理念**：用神经网络隐式表示三维场景

| 论文 | 年份 | 特点 |
|------|------|------|
| NeRF | ECCV 2020 | 开山之作 |
| Instant-NGP | 2022 | 加速版，hash encoding |
| Mip-NeRF 360 | 2022 | 无限场景 |

### 2. 3DGS 系列（3D Gaussian Splatting）
**核心理念**：用高斯球显式表示三维场景，实时渲染

| 论文/项目 | 年份 | 特点 |
|-----------|------|------|
| 3D Gaussian Splatting | SIGGRAPH 2023 | 开山之作 |
| SuGaR | CVPR 2024 | 表面对齐，可导出mesh |
| PGSR | TVCG 2024 | 平面检测，高质量表面 |
| FastGS | CVPR 2026 | 100秒训练 |
| GaussianEditor | 2024 | 编辑功能 |

### 3. EDGS / 相关变体
- **EDGS**：Enhanced 3D Gaussian Splatting（增强版）
- **E-Diffusion**：扩散模型 + 3DGS
- **DreamFusion**：文本生成3D

---

## 🔗 优质资源

### GitHub 仓库
| 仓库 | ⭐ | 说明 |
|------|-----|------|
| awesome-3D-gaussian-splatting | 8488 | 3DGS 论文汇总 |
| gaustudio | 1735 | 模块化3DGS框架 |
| supersplat | 4107 | 3DGS 编辑器 |
| splatviz | 1519 | Python 交互查看器 |

### 学习路径
1. **入门**：3DGS 原理（高斯泼溅）
2. **进阶**：SuGaR（表面重建）
3. **实战**：gaustudio 框架使用
4. **前沿**：CVPR 2024-2026 最新论文

---

## 📝 学习笔记

### 已掌握
- 

### 待学习
- [ ] 3DGS 基础原理
- [ ] 高斯球渲染流程
- [ ] SuGaR 表面重建
- [ ] gaustudio 框架使用
- [ ] EDGS 变体研究

---

## 🔧 工具链

### 训练框架
- gaustudio（模块化，支持多种3DGS变体）
- splatfacotry
- nerfstudio

### 工具
- supersplat（编辑器）
- splatviz（可视化）
- 3D Gaussian Splatting（原始）

---

## 📅 学习计划

**目标**：掌握图像到3D重建的核心技术

**阶段一**：理论入门（1-2周）
- 3DGS 论文精读
- 运行官方 Demo

**阶段二**：实战进阶（2-4周）
- 使用 gaustudio 训练自己的数据
- SuGaR 表面重建实验

**阶段三**：前沿探索（持续）
- 跟进 CVPR/ICCV 最新论文
- 尝试 EDGS 等变体

