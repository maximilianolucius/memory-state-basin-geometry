# Validated History Strategy

**Owner:** Chief Researcher  
**Date:** 2026-09-30  
**Status:** SOURCE-SPACE OSCILLATION CAP ACTIVE

## 1. TASK-0005 resolved the amplification question

The orbit-linearized discrete response is modest:
- B215 state amplification about \(8.9\);
- W1 about \(133\);
- amplification into the final \(M_T\) functional about \(0.09\) for B215.

Thus absolute-value amplification was the wrong metric.

## 2. Primary benchmark

B215:
\[
\theta=1/2,\ a=1/2,\ b=1,\ m=4/5,\ \alpha=17/20,
\]
\[
p=(277/100,467/1000).
\]

## 3. Rigorous formulation

Use the source equation
\[
\mathcal H(f)=
f-[g(\hat x+I^\alpha f)-g(\hat x)]+\rho.
\]

The derivative is
\[
I-AI^\alpha.
\]

On PL nodal variables:
\[
\boxed{L_h=I-AW.}
\]

This corrects the source/state mixing in the TASK-0005 \(Z_1\) pilot.

## 4. Function space

Use
\[
\|f\|_\vartheta=
\max\left(
\|f\|_\infty,
\max_n \operatorname{osc}_{C_n}(f)/\vartheta_n
\right).
\]

This is an equivalent Banach norm on \(C([0,T])\).

The cell oscillation bounds are therefore not an assumed property of the exact source; they are part of the validated ball.

## 5. Approximate inverse

With \(\pi\) PL interpolation and \(L_h=I-\pi K\pi\),

\[
B=L_h^{-1}\pi+(I-\pi)
\]

is bijective with
\[
B^{-1}=L_h\pi+(I-\pi).
\]

The exact inverse-defect identity is
\[
I-B(I-K)
=
L_h^{-1}\pi K(I-\pi)+(I-\pi)K.
\]

## 6. Goal

TASK-0006 must turn all resulting operator bounds into outward interval quantities and close a strict radii polynomial.

Then the validated source ball is propagated directly into the \(M_T\) functional.
