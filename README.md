# Empirical Study of Union-Find

## Overview
This project implements and evaluates multiple variants of the Union-Find data structure. The study measures performance through Total Path Length (TPL) and Total Pointer Updates (TPU) across different union and path compression strategies.

## Author
Pierre Jézégou  
(Engineering student at École Centrale de Lille, Exchange student at UPC)

## Contents
1. Introduction
2. Implementation
3. Experimental Setup
4. Results
5. Discussion and Conclusion

## 1. Introduction
The objective is to implement different Union-Find variants and evaluate their performance using TPL and TPU metrics.

## 2. Implementation
- **Union-Find Variants**: Implemented using class inheritance to handle different union strategies (Quick Union, Union by Size, Union by Rank) and path compression techniques (No Compression, Full Path Compression, Path Splitting, Path Halving).
- **Metrics**: 
  - **Total Path Length (TPL)**: Sum of distances from each element to its root.
  - **Total Pointer Updates (TPU)**: Total number of pointer updates during find operations.

## 3. Experimental Setup
- **Union-Find Strategies**: 12 combinations of union and path compression strategies.
- **Repetition and Data Collection**: Each experiment is repeated 20 times for values of n (1000, 5000, 10000).
- **Performance Metrics**: Measured TPL and TPU at regular intervals and calculated total cost.

## 4. Results
- **Plots**: Display the evolution of TPL and TPU for different n values.
- **Comparison**: Analyze the performance of different strategies based on total cost.

## 5. Discussion and Conclusion
Summarizes findings and performance trade-offs between different strategies.

## How to Run the Project
1. **Install Python**.
2. **Clone the Repository**: `git clone <repository-url>`
3. **Navigate to the Directory**: `cd <project-directory>`
4. **Install Dependencies**: `pip install -r requirements.txt`
5. **Run Experiments**: Execute the provided Python scripts.
6. **View Results**: Results are saved and can be viewed with any plotting tool.