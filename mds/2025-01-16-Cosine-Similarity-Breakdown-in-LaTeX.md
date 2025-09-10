# Cosine Similarity Breakdown in LaTeX

A mathematical breakdown of cosine similarity, with copy-pastable LaTeX.

## Overview

After hearing so much about cosine similarity, I thought it was something extremely difficult to understand. It turns out it's just the similarity of 2 word vectors, calculated as the cosine of the angle between them.

The result ranges from -1 to 1, where:

* 1 means the vectors point in the same direction (most similar)
* 0 means they're perpendicular (totally unrelated)
* -1 means they point in opposite directions (complete opposites)

Similarity is just about the angle. The vectors are typically normalized to make comparisons make more sense intuitively, and to avoid having to deal with magnitudes as well.

Note: I'm reading that the range used with word vectors is usually [0,1] because word vectors typically are non-negative.

## The Cosine Similarity Formula

The cosine similarity formula in LaTeX:


```latex
%%latex
$$\text{cos}(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$
```


$$\text{cos}(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$



## Dot Product

If you're wondering why it looks so familiar, it's probably because you can get it by rewriting the definition of the dot product:


```latex
%%latex
$$\mathbf{A} \cdot \mathbf{B} = {\|\mathbf{A}\| \|\mathbf{B}\|}\cos(\theta)$$
```


$$\mathbf{A} \cdot \mathbf{B} = {\|\mathbf{A}\| \|\mathbf{B}\|}\cos(\theta)$$



## Expanding Dot Product Sum

In the cosine similarity formula, the numerator is the dot product **A** . **B**. Expanding that, you get the sum of all the vector components multiplied together:


```latex
%%latex
$$\mathbf{A} \cdot \mathbf{B} = \sum_{i=1}^n A_i B_i$$
```


$$\mathbf{A} \cdot \mathbf{B} = \sum_{i=1}^n A_i B_i$$



## Magnitude: Sqrt of Sum of Squares

The magnitude ‖A‖ is the square root of the sum of the squares of its components:


```latex
%%latex
$$\|\mathbf{A}\| = \sqrt{\sum_{i=1}^{n} A_i^2}$$
```


$$\|\mathbf{A}\| = \sqrt{\sum_{i=1}^{n} A_i^2}$$



It's just the length of the vector.

## Multiplying Vector Magnitudes

In the cosine similarity formula, the denominator is multiplying magnitudes $\|\mathbf{A}\| \|\mathbf{B}\|$ together:


```latex
%%latex
$$\|\mathbf{A}\| \|\mathbf{B}\| = {\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$
```


$$\|\mathbf{A}\| \|\mathbf{B}\| = {\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$



## Putting It All Together


```latex
%%latex
$$\text{cos}(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$
```


$$\text{cos}(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$



## Simplifying With Normalization


```python

```

## Summary

Cosine similarity measures how similar two vectors are by finding the cosine of the angle between them. 

The math is not as bad as it looks: we're just comparing the directions vectors point in, normalized by their lengths.
