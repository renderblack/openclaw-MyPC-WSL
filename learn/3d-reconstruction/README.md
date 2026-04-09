# 3D 图像重建学习板块

> 专注：图像三维重建技术，从 NeRF 到 3DGS 及相关技术
> 
> 最后更新：2026-04-10

---

## 📚 技术路线图

### 1. NeRF 系列（Neural Radiance Fields）
**核心理念**：用神经网络隐式表示三维场景

| 论文 | 年份 | 特点 |
|------|------|------|
| NeRF | ECCV 2020 | 开山之作，MLP隐式表示 |
| Instant-NGP | 2022 | 加速版，hash encoding |
| Mip-NeRF 360 | 2022 | 无限场景 |

### 2. 3DGS 系列（3D Gaussian Splatting）
**核心理念**：用高斯球显式表示三维场景，实时渲染

| 论文/项目 | 年份 | 特点 |
|-----------|------|------|
| 3D Gaussian Splatting | SIGGRAPH 2023 | 开山之作，实时渲染 |
| SuGaR | CVPR 2024 | 表面对齐，可导出mesh |
| PGSR | TVCG 2024 | 平面检测，高质量表面 |
| FastGS | CVCV 2026 | 100秒训练 |
| GaussianEditor | 2024 | 编辑功能 |

### 3. EDGS / 相关变体
- **EDGS**：Enhanced 3D Gaussian Splatting（增强版）
- **E-Diffusion**：扩散模型 + 3DGS
- **DreamFusion**：文本生成3D

---

## 🎯 系统性学习计划（12周）

### 阶段一：理论基础（第1-3周）

#### Week 1：NeRF 入门
**目标**：理解隐式表示三维场景的原理

**学习内容**：
1. 精读 NeRF 论文（原版论文 + 中文解读）
2. 理解 MLP 神经网络隐式表示
3. 体素渲染（Volume Rendering）原理

**资源**：
- 原版论文：https://www.mrnerf.com/nerf
- 中文解读：百度/知乎搜索"NeRF论文解读"
- MIT 课程：https://www.scenerepresentations.org/courses/inverse-graphics-23/

**检验标准**：能用自己的话解释 NeRF 的三个核心步骤

---

#### Week 2：3DGS 原理
**目标**：理解高斯球显式表示 vs NeRF 的区别

**学习内容**：
1. 3DGS 原版论文精读
2. 高斯球参数（位置、协方差、颜色、不透明度）
3. 可微渲染（Differenti Rendering）
4. 反向传播训练过程

**资源**：
- 原版论文：https://github.com/graphdeco-inria/gaussian-splatting
- 解读博客：https://huggingface.co/blog/gaussian-splatting
- 理论讲解：https://github.com/chiehwangs/3d-gaussian-theory

**检验标准**：能画出 3DGS 的训练流程图

---

#### Week 3：3DGS vs NeRF 对比
**目标**：理解为什么 3DGS 能实时渲染

**对比维度**：
| 维度 | NeRF | 3DGS |
|------|------|-------|
| 表示方式 | 隐式（MLP） | 显式（高斯球） |
| 渲染速度 | 慢（逐像素） | 快（光栅化） |
| 实时性 | ❌ | ✅ |
| 编辑能力 | 弱 | 强 |

**输出**：整理对比表格，写入学习笔记

---

### 阶段二：工具掌握（第4-6周）

#### Week 4：环境搭建 + 官方Demo
**目标**：跑通 3DGS 官方代码

**任务清单**：
- [ ] 配置 CUDA 环境（确认 GPU 支持）
- [ ] clone 官方仓库：`git clone https://github.com/graphdeco-inria/gaussian-splatting`
- [ ] 安装依赖：`pip install -r requirements.txt`
- [ ] 下载测试数据
- [ ] 运行 Demo：`python render.py -m <model_path>`
- [ ] 输出：截图保存到 `learn/3d-reconstruction/screenshots/`

**检验标准**：成功渲染出第一张 3DGS 图

---

#### Week 5：gaustudio 框架
**目标**：掌握模块化训练框架

**任务清单**：
- [ ] 安装 gaustudio：`pip install gaustudio`
- [ ] 阅读文档：https://github.com/GAP-LAB-CUHK-SZ/gaustudio
- [ ] 运行示例：多种 3DGS 变体对比
- [ ] 理解模块化设计（不用的 backone、renderer）

**支持的模型**：
- Vanilla 3DGS
- SuGaR（表面重建）
- PGSR（平面检测）
- TPGF（ tensor plane）

**检验标准**：能用 gaustudio 训练一个自己的数据

---

#### Week 6：数据采集与处理
**目标**：掌握从图像到 3D 的数据准备

**任务清单**：
- [ ] 了解数据格式要求（COLMAP 稀疏重建）
- [ ] 安装 COLMAP：`sudo apt install colmap`（Linux）或 下载 Windows 版
- [ ] 使用手机采集一组图像
- [ ] 运行 COLMAP 重建
- [ ] 输入到 gaustudio 训练

**数据采集技巧**：
- 光照均匀，避免过曝/过暗
- 多角度覆盖，重叠度 60-80%
- 静态场景，避免运动模糊

**检验标准**：用自己的图像成功重建出 3D 模型

---

### 阶段三：进阶应用（第7-9周）

#### Week 7：SuGaR 表面重建
**目标**：掌握如何从 3DGS 导出 Mesh

**学习内容**：
1. SuGaR 论文精读
2. 理解"表面对齐高斯球"
3. 从高斯球提取 mesh（.obj/.ply）

**应用场景**：
- 3D 打印
- 游戏资产生成
- BIM 模型导入

**检验标准**：成功导出 mesh 并能用 MeshLab 查看

---

#### Week 8：编辑器与可视化
**目标**：掌握常用编辑工具

**工具清单**：
| 工具 | 用途 | 链接 |
|------|------|------|
| SuperSplat | 浏览器编辑器 | https://github.com/playcanvas/supersplat |
| SplatViz | Python 可视化 | https://github.com/Florian-Barthel/splatviz |
| Three.js Viewer | Web 查看器 | https://github.com/mkkellogg/GaussianSplats3D |

**任务**：用 SuperSplat 编辑一个高斯模型（裁剪、合并）

---

#### Week 9：工程化与优化
**目标**：了解实际部署中的问题

**学习内容**：
1. 模型压缩与加速（参数量、渲染速度）
2. 多GPU训练
3. 移动端部署（WebGL/WebGPU）
4. 动态场景（4D GS）

**资源**：
- FastGS（100秒训练）：https://github.com/fastgs/FastGS
- GSCodec Studio（压缩）：https://github.com/JasonLSC/GSCodec_Studio

---

### 阶段四：前沿探索（第10-12周）

#### Week 10-11：最新论文导读
**目标**：跟进 CVPR/ICCV 2024-2026 最新工作

**论文清单**：
| 论文 | 会议 | 关键词 |
|------|------|--------|
| SuGaR | CVPR 2024 | 表面重建 |
| PGSR | TVCG 2024 | 平面检测 |
| GaussianEditor | CVPR 2024 | 编辑 |
| FastGS | CVPR 2026 | 加速 |
| Dynamic 3DGS | - | 动态场景 |

**方式**：每周精读1-2篇，整理笔记

---

#### Week 12：项目实战
**目标**：完成一个完整项目

**项目方向**（选其一）：
1. **建筑扫描重建**：用手机扫描一个建筑，导出 mesh
2. **产品 3D 展示**：电商产品多角度拍摄，生成 3D 模型
3. **历史建筑数字化**：古建筑三维重建存档
4. **结合 BIM**：3DGS 导出到 Revit/Revit

**输出**：项目报告（技术路线、遇到问题、解决方案）

---

## 🔗 优质资源汇总

### 论文汇总
| 仓库 | ⭐ | 说明 |
|------|-----|------|
| awesome-3D-gaussian-splatting | 8488 | 最全论文列表 |
| 3D-Gaussian-Splatting-Papers | 2853 | 中文论文汇总 |

### 框架
| 仓库 | ⭐ | 说明 |
|------|-----|------|
| gaustudio | 1735 | 模块化训练框架 |
| nerfstudio/gsplat | - | Nerfstudio 集成 |

### 编辑器
| 仓库 | ⭐ | 说明 |
|------|-----|------|
| supersplat | 4107 | 浏览器3DGS编辑器 |
| splatviz | 1519 | Python 可视化 |

### 游戏引擎支持
| 引擎 | 插件 |
|------|------|
| Unity | arash-p/UnityGaussianSplatting |
| Unreal | XV3DGS-UEPlugin |
| PlayCanvas | 内置支持 |

---

## 📝 学习笔记模板

```markdown
# [日期] 学习笔记：XXX

## 核心概念
...

## 关键代码
...

## 遇到的问题
...

## 解决方案
...
```

---

## 🔧 环境检查清单

在开始之前，确认以下环境已就绪：

- [ ] NVIDIA GPU（CUDA >= 11.0）
- [ ] Python >= 3.8
- [ ] PyTorch >= 1.12
- [ ] COLMAP（可选，用于数据预处理）
- [ ] Git

**检查命令**：
```bash
nvidia-smi  # 确认GPU
python --version  # 确认Python版本
nvcc --version  # 确认CUDA版本
```

---

## 📊 进度追踪

| 阶段 | 周数 | 目标 | 状态 |
|------|------|------|------|
| 理论基础 | 1-3周 | 理解原理 | ⬜ |
| 工具掌握 | 4-6周 | 跑通代码 | ⬜ |
| 进阶应用 | 7-9周 | SuGaR/编辑 | ⬜ |
| 前沿探索 | 10-12周 | 论文+项目 | ⬜ |

**开始日期**：待定
**预计完成**：12周后
