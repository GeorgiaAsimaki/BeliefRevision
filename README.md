# BeliefRevision
# Belief Revision Agent

## Introduction

This project implements a belief revision agent in Python, focusing on managing and updating a belief base using various operations such as contraction, revision, and expansion. The agent utilizes priority-based belief management to handle conflicting beliefs and ensure coherence within the belief base.

## Files

- **agent.py**: Contains the main script for interacting with the belief revision agent. It allows users to input new beliefs and initiates the revision process accordingly.
- **beliefRevision.py**: Defines the `BeliefBase` and `Belief` classes, which represent the belief base and individual beliefs, respectively. It includes functions for revision, contraction, expansion, and checking entailment.
- **utils.py**: Provides utility functions used in belief revision, such as converting CNF formulas to clauses and performing resolution.

## Installation

No specific installation steps are required. Simply ensure that Python 3.x is installed on your system.
Also 'pip install sympy' 

## Usage

To use the belief revision agent:

1. Run `agent.py`.
2. Input a new belief statement when prompted, along with its priority (an integer from 0 to 10).
3. The agent will process the input, perform belief revision if necessary, and display the updated belief base.
