# Decision-Tree-Character-Identifier-CSC311

# Decision-Tree Character Identifier

A simple Python CLI that “20 Questions”-style guesses a character from a CSV dataset by asking the most informative yes/no questions.


## Features
- Builds a binary decision tree over any “attribute = value” question space.  
- Chooses splits by computing information gain via log₂-based entropy.  
- Limits tree depth (default max 20) to avoid overfitting.  
- Formats human-readable yes/no questions on the fly.  
- Reports actual vs. theoretical question bounds at the end.  

## Requirements
- Python 3.7+  
- pandas  

## Installation
1. Clone this repo:  
   ```bash

