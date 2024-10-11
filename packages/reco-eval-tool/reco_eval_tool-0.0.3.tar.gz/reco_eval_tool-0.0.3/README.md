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
import caer

# Load a standard 640x427 test image that ships out-of-the-box with caer
sunrise = caer.data.sunrise(rgb=True)

# Resize the image to 400x400 while MAINTAINING aspect ratio
resized = caer.resize(sunrise, target_size=(400,400), preserve_aspect_ratio=True)
```

<img src="examples/thumbs/resize-with-ratio.png" alt="caer.resize()" />

For more examples, see the [Caer demos](https://github.com/jasmcaus/caer/blob/master/examples/) or [Read the documentation](http://caer.rtfd.io)
