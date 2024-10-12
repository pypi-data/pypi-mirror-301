
# Criteria Performance

The **Criteria Performance** package provides tools for visualizing performance criteria in machine learning, including ROC, Precision-Recall, and DET curves. This package is designed to help users evaluate the performance of their models through intuitive visualizations.

## Features

- Compute and plot **ROC** (Receiver Operating Characteristic) curves
- Compute and plot **Precision-Recall** curves
- Compute and plot **DET** (Detection Error Tradeoff) curves
- Integrated plotting with `matplotlib` for seamless visualization
- Support for loading data from a CSV file via a URL

## Installation

You can install the package using pip:

```bash
pip install criteria_performance
```

## Usage

### Example

To use the `PerformanceCriteria` class, you need to provide a URL pointing to a CSV file with two columns: one for the class labels (1 for positive class and -1 for negative class) and another for the corresponding scores (predicted probabilities). The 1s and -1s will be grouped separately in the analysis.

Here’s an example of how to use the package:

```python
from criteria_performance import PerformanceCriteria

# Initialize the PerformanceCriteria object with the URL to the CSV file
criteria = PerformanceCriteria("url_data_csv")

# Plot the ROC curve
criteria.dispROC()

# Plot the Precision-Recall curve
criteria.dispPR()

# Plot the DET curve
criteria.dispDET()
```

## Data Format

The input CSV file must follow the specific structure below to be compatible with the package:

| Class | Score |
|-------|-------|
| 1     | 0.9   |
| 1     | 0.8   |
| -1    | 0.4   |
| -1    | 0.1   |

- **Class**: The actual class label (1 for positive class, grouped together, and -1 for negative class, also grouped together).
- **Score**: The predicted score or probability associated with the positive class.

Ensure that your CSV file adheres to this format for the package to function correctly.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.
