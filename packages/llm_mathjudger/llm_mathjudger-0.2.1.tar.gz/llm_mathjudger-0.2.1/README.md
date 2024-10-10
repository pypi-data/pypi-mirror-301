# LLM-MathJudger

基于 [LLM-Math](https://github.com/CoderBak/llm-math) 简化的数学判别器. 该版本仅用于数学检查，因此不需要加载模型.

### Usage

1. `basic_check(A, B)`

   检查 A, B 两个**纯数学**表达式是否一致，返回 True / False.

2. `check(prompt_type, data_name, target, pred)`

   检查 pred 是否与 target 一致，返回 True / False. target 即为数据集的某一行.

- 支持的 prompt 类型: `tool-integrated`, `direct`, `cot`, `pal`, `self-instruct`, `self-instruct-boxed`, `tora`, `wizard_zs`, `platypus_fs`, `deepseek-math`, `kpmath`.

- 支持的数据集: `gsm8k`, `math`, `svamp`, `asdiv`, `mawps`, `tabmwp`, `mathqa`, `mmlu_stem`, `sat_math`.

### Note

该版本为了提高速度采用了激进的修改，还未经严格测试，请谨慎使用.
