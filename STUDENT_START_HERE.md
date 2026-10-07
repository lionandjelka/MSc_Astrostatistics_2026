# Student Start Here

Welcome to **Astrostatistics for the Survey Era**.

## Weekly workflow

Before class:
1. open the listed Crete **Learning Notebook**;
2. work through the concepts/exercises requested by the instructor;
3. note one question or assumption you do not understand.

During the 3-hour lecture:
- connect the statistical method to a scientific inference problem;
- derive/interpret the key equations;
- examine one binary-SMBH worked example.

During the 4-hour hands-on:
- complete the scientific statement before coding;
- implement the method;
- add uncertainty and diagnostics;
- finish with a short scientific interpretation.

## Five questions required in every assessed analysis

1. What is the **estimand**?
2. What is actually **observed**?
3. What **generative assumptions** connect them?
4. What uncertainty/selection is present?
5. How will you **validate or falsify** the result?

## Crete answer keys

The source repository contains answer-key notebooks.  They are learning resources, but graded homework/final-project questions are new binary-SMBH tasks.  Copying an answer-key method without checking its assumptions against the new data does not constitute a valid solution.

## Large data

Never load the full 500+ GB parent dataset into RAM.  Use Parquet column projection and row groups, or instructor-prepared subsets.
