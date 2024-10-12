# Reco Evaluation Tool

The Reco Evaluation Tool simplifies result evaluation by offering the following functions:

1. reading results from file or directory
2. analyzing features (including single feature distribution, pivot tables, and feature shifts)
3. calculating PR numbers

All functions are achievable with a single line of code.

## Overview

Reco Evaluation Tool is a Python library that consists of the following components:


| Component                          | Description                                                         |
| ---------------------------------- | ------------------------------------------------------------------- |
| [**reco_eval_tool.datasets**]      | Read results from file or directory then return a dataframe        |
| [**reco_eval_tool.metrics**]       | Calculate pr numbers                                                |
| [**reco_eval_tool.statistics**]    | Analyze single feature; Analyze feature shift; Generate pivot table |
| [**reco_eval_tool.visualization**] | Visualize evaluation result                                         |

# Installation

To install the current release:

```shell
$ pip install --upgrade reco_eval_tool
```

# Getting Started

## Minimal Example

```python
import os
import reco_eval_tool as ret

ret.set_output_dir("./eval_results")
all_df = ret.datasets.load_dir("demo")
per_language_prf = ret.metrics.calculate_prf(all_df, 'HumanIsLimitedUse', 'GPTIsLimitedUseV6', 'Language')
```

![1728654952757](images/README/1728654952757.png)

Please go this below file for more details: [demo.ipynb](https://microsoftapc-my.sharepoint.com/:u:/g/personal/mingleiguo_microsoft_com/EbtFefg6-KhIpdUW8AAladEBobUwWyNpCLBmrX-OcT0miw?e=1XMqHc)
