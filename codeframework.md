# CodeFramework

```text
前端：狼人杀论文的前端实现
前后端交互方法：统一使用JSON存储，与前端交互的数据格式需要一个人来实现

后端：
生成模块  —— 基于用户社会模拟的需求生成合适的 Group 以及 Enviroment JSON文件（start.py Generation）
Agent模块 —— 单个Agent Memory；Plan；StepBack（Reflection）；Perceive
Group模块 —— Group Memory；Select Speaker；Whether Discuss; Mode Decision；
    1. Group Class作为一个基类
    2. Conference ; Web Discussion ; 
Environment模块 —— 时间步模块，需要接受一个初始化的Idea，然后根据Idea生成Group系列，开始时间步循环
Prompt驱动模块
LLM模块
数据存储 & 转换模块
```