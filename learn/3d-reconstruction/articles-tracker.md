# 3DGS 文章追踪

> 记录发现的有价值文章，持续更新

---

## 追踪规则

- 发现新文章时，按以下格式记录
- 优先记录：论文解读、实战教程、前沿进展
- 标注来源公众号和日期

---

## 文章记录

### 2026-04-10

#### SurfelSplat：稀疏视角表面重建的高效通用高斯 Surfel 表示
- **来源**：arXiv
- **日期**：2026-04-09
- **链接**：https://arxiv.org/search/?searchtype=all&query=SurfelSplat
- **作者**：Chensheng Dai, Shengjun Zhang, Min Chen, Yueqi Duan
- **摘要**：3DGS 在 3D 场景重建表现优异。本文提出 SurfelSplat，学习高效通用的 Gaussian Surfel 表示用于稀疏视角表面重建。
- **标签**：稀疏视角、表面重建

#### BLaDA：连接语言与 3DGS 字段功能灵巧操作
- **来源**：arXiv
- **日期**：2026-04-09
- **链接**：https://arxiv.org/search/?searchtype=all&query=BLaDA
- **作者**：Fan Yang, Wenrui Chen 等
- **摘要**：在非结构化环境中，功能灵巧抓取需要语义理解、精确 3D 功能定位和物理可解释执行的紧密整合。模块化分层方法比端到端 VLA 更可控和可解释。
- **标签**：灵巧操作、语言控制、机器人

#### DOC-GS：双域观测与校准的可靠稀疏视角高斯泼溅
- **来源**：arXiv
- **日期**：2026-04-08
- **链接**：https://arxiv.org/search/?searchtype=all&query=DOC-GS+Dual-Domain+Observation+Calibration
- **作者**：Hantang Li, Qiang Zhu 等
- **摘要**：稀疏视角 3DGS 重建的双域观测与校准方法，提升可靠性。
- **标签**：稀疏视角、稀疏重建

#### From Blobs to Spokes：面向高保真表面重建的有向高斯
- **来源**：arXiv
- **日期**：2026-04-08
- **链接**：https://arxiv.org/search/?searchtype=all&query=From+Blobs+to+Spokes+Oriented+Gaussians
- **作者**：Diego Gomez, Antoine Guédon, Nissim Maruani, Bingchen Gong, Maks Ovsjanikov
- **摘要**：3DGS 革新了快速渲染，但球谐函数表达能力有限。本文提出用有向高斯替代斑点（blobs）实现高保真表面重建。
- **标签**：表面重建、新表示方法

---

## 2026-04-12 新增

#### Generative 3DGS：大气降尺度与预报的生成式高斯泼溅
- **来源**：arXiv
- **日期**：2026-04-09
- **链接**：https://arxiv.org/search/?searchtype=all&query=Generative+3D+Gaussian+Splatting+Atmospheric+Downscaling
- **作者**：Tao Hana, Zhibin Wen, Zhenghao Chen 等
- **摘要**：大气降尺度与预报中，生成高分辨率输出因多尺度适应性和数据表示效率受限。本文提出 3D Gaussian Splatting 用于任意分辨率大气预测。
- **标签**：大气科学、生成式模型、科学应用

#### ReconPhys：单目视频联合重建外观与物理属性
- **来源**：arXiv
- **日期**：2026-04-09
- **链接**：https://arxiv.org/search/?searchtype=all&query=ReconPhys+Physical+Attributes+3DGS
- **作者**：Boyuan Wang, Xiaofeng Wang 等
- **摘要**：首个前馈框架，从单目视频联合学习物理属性估计和 3DGS 重建。双分支架构兼顾外观和物理属性。
- **标签**：单目视频、物理属性、前馈重建

#### Splats under Pressure：边缘GPU约束下的性能-能耗权衡
- **来源**：arXiv
- **日期**：2026-04-08
- **链接**：https://arxiv.org/search/?searchtype=all&query=Splats+under+Pressure+Edge+GPU+3DGS
- **作者**：Muhammad Fahim Tajwar, Arthur Wuhrlin, Bhojan Anand
- **摘要**：研究边缘客户端在不同高斯数量和 GPU 算力约束下实时 3DGS 光栅化的可行性，探讨性能-能耗权衡。
- **标签**：边缘计算、实时渲染、资源优化

#### Genie Sim PanoRecon：单张全景图快速生成沉浸式场景
- **来源**：arXiv
- **日期**：2026-04-08
- **链接**：https://arxiv.org/search/?searchtype=all&query=Genie+Sim+PanoRecon+Panorama+3DGS
- **作者**：Zhijun Li, Yongxin Su, Di Yang 等
- **摘要**：前馈式高斯泼溅方法，从单张全景图快速生成沉浸式场景。
- **标签**：全景图、场景生成、前馈方法

#### AnchorSplat：基于3D几何先验的前馈3DGS
- **来源**：arXiv
- **日期**：2026-04-09
- **链接**：https://arxiv.org/search/?searchtype=all&query=AnchorSplat+3D+Geometric+Priors
- **作者**：Xiaoxue Zhang, Xiaoxu Zheng, Yixuan Yin 等
- **摘要**：近期前馈高斯重建模型采用像素对齐公式，将每个 2D 像素映射到 3D 高斯。AnchorSplat 引入 3D 几何先验提升前馈重建质量。
- **标签**：前馈重建、几何先验、深度估计

#### GS-Surrogate：用于模拟参数空间探索的可变形高斯泼溅
- **来源**：arXiv
- **日期**：2026-04-07
- **链接**：https://arxiv.org/search/?searchtype=all&query=GS-Surrogate+Deformable+Gaussian+Splatting
- **作者**：Ziwei Li, Rumali Perera, Angus Forbes 等
- **摘要**：将可变形高斯用于大规模模拟的参数空间探索，构建代理模型。
- **标签**：可变形 GS、科学计算、可视化

#### ADM-GS：多遍历重建的外观分解高斯泼溅
- **来源**：arXiv
- **日期**：2026-04-07
- **链接**：https://arxiv.org/search/?searchtype=all&query=ADM-GS+Appearance+Decomposition+Gaussian+Splatting
- **作者**：Yangyi Xiao, Siting Zhu, Baoquan Yang 等
- **摘要**：解决跨遍历外观变化问题，应用显式外观分解处理静态背景。
- **标签**：多遍历、外观分解

#### GaussianGrow：文本引导下从 3D 点云几何感知高斯增长
- **来源**：arXiv
- **日期**：2026-04-07
- **链接**：https://arxiv.org/search/?searchtype=all&query=GaussianGrow+Geometry-aware+Gaussian+Growing
- **作者**：Weiqi Zhang, Junsheng Zhou, Haotian Geng 等
- **摘要**：从 3D 点云和文本指导出发，几何感知地增长高斯体。
- **标签**：文本引导、点云、几何感知

#### AvatarPointillist：自回归 4D 高斯化身
- **来源**：arXiv
- **日期**：2026-04-06
- **链接**：https://arxiv.org/search/?searchtype=all&query=AvatarPointillist+AutoRegressive+4D+Gaussian+Avatar
- **作者**：Hongyu Liu, Xuan Wang, Yujun Shen, Qifeng Chen 等
- **摘要**：从单张人像图像生成动态 4D 高斯化身，核心是解码器-only Transformer 自回归生成 3D 点云。
- **标签**：数字人、4D 重建、自回归

#### GaussFly：3D 高斯场的对比强化学习视觉运动策略
- **来源**：arXiv
- **日期**：2026-04-06
- **链接**：https://arxiv.org/search/?searchtype=all&query=GaussFly+Contrastive+Reinforcement+Learning+3D+Gaussian
- **作者**：Yuhang Zhang, Mingsheng Li 等
- **摘要**：real-to-sim-to-real 范式，利用 3DGS 重建训练场景，结合显式几何约束实现鲁棒的 sim-to-real 迁移。
- **标签**：强化学习、机器人、sim-to-real

#### SmokeGS-R：物理引导伪清洁 3DGS 真实多视角烟雾重建
- **来源**：arXiv
- **日期**：2026-04-06
- **链接**：https://arxiv.org/search/?searchtype=all&query=SmokeGS+Physics+Guided+Pseudo+Clean+3DGS
- **作者**：Xueming Fu, Lixia Han
- **摘要**：物理引导生成伪清洁监督，训练 sharp clean-only 3DGS 用于真实多视角烟雾恢复。
- **标签**：物理仿真、烟雾重建、大气

#### Generative 3DGS 用于任意分辨率大气降尺度和预测
- **来源**：arXiv
- **日期**：2026-04-10
- **链接**：https://arxiv.org/search/?searchtype=all&query=Generative+3D+Gaussian+Splatting+Atmospheric+Downscaling
- **作者**：Tao Hana, Zhibin Wen 等
- **摘要**：生成式 3DGS 用于大气降尺度和预测，生成高分辨率输出，解决多尺度适应性和数据表示效率问题。
- **标签**：大气科学、生成模型、预测

#### 室内资产检测：360° 无人机图像大规模室内资产检测
- **来源**：arXiv
- **日期**：2026-04-06
- **链接**：https://arxiv.org/search/?searchtype=all&query=Indoor+Asset+Detection+3D+Gaussian+Splatting+Drone
- **摘要**：360° 无人机拍摄图像中目标室内资产的目标级检测和分割方法，基于 3DGS。
- **标签**：目标检测、无人机、智慧城市/建筑

#### 4D 血管重建用于台式血栓切除分析
- **来源**：arXiv
- **日期**：2026-04-08
- **链接**：https://arxiv.org/search/?searchtype=all&query=4D+Vessel+Reconstruction+Gaussian+Splatting+Thrombectomy
- **摘要**：2160p/20fps 多视角视频标定、分割、4DGS 重建，转换为固定连通性边图用于 ROI 位移跟踪。
- **标签**：医学成像、4D 重建、血管

#### In Depth We Trust：单目深度可靠监督的高斯泼溅
- **来源**：arXiv
- **日期**：2026-04-07
- **链接**：https://arxiv.org/search/?searchtype=all&query=In+Depth+We+Trust+Monocular+Depth+Gaussian+Splatting
- **作者**：Wenhui Xiao, Ethan Goan 等
- **摘要**：单目深度可靠监督方法，提升 3DGS 深度估计精度。
- **标签**：深度估计、自监督

---

## 追踪规则

- 发现新文章时，按以下格式记录
- 优先记录：论文解读、实战教程、前沿进展
- 标注来源公众号和日期
