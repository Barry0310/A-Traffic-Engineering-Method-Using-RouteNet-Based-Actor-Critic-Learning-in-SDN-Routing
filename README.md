# A Traffic Engineering Method Using RouteNet-Based Actor-Critic Learning in SDN Routing

- Reference:
    - [ENERO: Efficient Real-Time WAN Routing
Optimization with Deep Reinforcement Learning](https://arxiv.org/pdf/2109.10883.pdf)
    - https://github.com/BNN-UPC/ENERO
    
- python 版本: 3.10
- requirement: `pip install -r requirement.txt`
- 安裝自訂環境: 以 SAC_PL_KP 為例，在 SAC_PL_KP 目錄下 `pip install -e gym-graph/`
    - 因為有分為 KP 與 SP，gym 環境不同，所以每種方法最好開不同的 conda 環境安裝
- dataset: [download](https://drive.google.com/file/d/1I8txvqhQLfiRGfn1DqafeW7YLYwtfXOk/view?usp=sharing) (Reference: [ENERO dataset](https://drive.google.com/file/d/1gem-VQ5MY3L54B77XUYt-rTbemyKmaqs/view))
    - 下載解壓縮後放在與 SAC_PL_KP 等目錄同層中

- PPO_L_KP 為 tensorflow 版本，所以訓練執行及所需 requirement 參照 ENERO 的 github

- PPO_PL_SP
    - train: `python main.py`
    - test: `python eval.py`
- PPO_PL_KP、SAC_PL_KP
    - train: `python main.py`
    - test: `python eval.py`
    - link failure: `python eval_linkfailure.py`
    - zoo test: `python eval_zoo.py`
- other_figs 中 draw_topology、fig9、10、11 可直接執行
    - fig14 指令
    ```
    python fig14.py -d Enero_3top_15_B_SAC49 -p ../Enero_datasets/rwds-results-1-link_capacity-unif-05-1-zoo
    ```
