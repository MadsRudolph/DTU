# 30035 — Exercises 9  
## Recap: Vector Calculus (Cartesian)

---

## Exercise 9.1 — Norm and Unit Vector

> **Given**  
> Vector in rectangular (Cartesian) form:  
> $$
 \mathbf a = 2\hat{\mathbf x} - 3\hat{\mathbf y} + 1\hat{\mathbf z}.
 $$
>
> (a) Compute the **length** (norm) $|\mathbf a|$.  
> (b) Find the **unit vector** $\hat{\mathbf a}$ in the same direction as $\mathbf a$.

---

### (a) Norm of $\mathbf a$

The norm of a Cartesian vector is
$$
|\mathbf a| = \sqrt{a_x^2 + a_y^2 + a_z^2}.
$$

Here:
- $a_x = 2$,  
- $a_y = -3$,  
- $a_z = 1$.

Thus:
$$
|\mathbf a|
= \sqrt{2^2 + (-3)^2 + 1^2}
= \sqrt{4 + 9 + 1}
= \sqrt{14}.
$$

---

### (b) Unit vector in the direction of $\mathbf a$

By definition:
$$
\hat{\mathbf a} = \frac{\mathbf a}{|\mathbf a|}
= \frac{1}{\sqrt{14}}\,(2\hat{\mathbf x} - 3\hat{\mathbf y} + 1\hat{\mathbf z}).
$$

So:
$$
\hat{\mathbf a}
= \frac{2}{\sqrt{14}}\hat{\mathbf x}
- \frac{3}{\sqrt{14}}\hat{\mathbf y}
+ \frac{1}{\sqrt{14}}\hat{\mathbf z}.
$$

---

### Final boxed results

$$
\boxed{
|\mathbf a| = \sqrt{14},
\qquad
\hat{\mathbf a} = \frac{2}{\sqrt{14}}\hat{\mathbf x}
- \frac{3}{\sqrt{14}}\hat{\mathbf y}
+ \frac{1}{\sqrt{14}}\hat{\mathbf z}
}
$$

---

### MATLAB — Exercise 9.1

> [!code]- MATLAB — Exercise 9.1  
> ```matlab
>a = [2; -3; 1];
>
>a_norm = norm(a);          % length of a
>a_hat  = a / a_norm;       % unit vector
>
>fprintf('||a|| = %.6f\n', a_norm);
>fprintf('a_hat = [%.6f  %.6f  %.6f]^T\n', a_hat);
>```
---

## Exercise 9.2 — Vector Sum, Difference, Dot and Cross Products

> **Given**  
> Vectors in **column (component)** form:
> $$
> \mathbf a =
> \begin{pmatrix}
> 2\\-3\\1
> \end{pmatrix},
> \qquad
> \mathbf b =
> \begin{pmatrix}
> 5\\2\\-6
> \end{pmatrix}.
> $$
>  
> Compute:  
> (a) $\mathbf c = \mathbf a + \mathbf b$  
> (b) $\mathbf c = \mathbf a - \mathbf b$  
> (c) $\mathbf c = \mathbf b - \mathbf a$  
> (d) $\mathbf a\cdot\mathbf b$  
> (e) $\mathbf b\cdot\mathbf a$  
> (f) $\mathbf a\times\mathbf b$  
> (g) $\mathbf b\times\mathbf a$

---

### (a) Sum $\mathbf a + \mathbf b$

$$
\mathbf a + \mathbf b
=
\begin{pmatrix}
2\\-3\\1
\end{pmatrix}
+
\begin{pmatrix}
5\\2\\-6
\end{pmatrix}
=
\begin{pmatrix}
2+5\\-3+2\\1+(-6)
\end{pmatrix}
=
\begin{pmatrix}
7\\-1\\-5
\end{pmatrix}.
$$

---

### (b) Difference $\mathbf a - \mathbf b$

$$
\mathbf a - \mathbf b
=
\begin{pmatrix}
2\\-3\\1
\end{pmatrix}
-
\begin{pmatrix}
5\\2\\-6
\end{pmatrix}
=
\begin{pmatrix}
2-5\\-3-2\\1-(-6)
\end{pmatrix}
=
\begin{pmatrix}
-3\\-5\\7
\end{pmatrix}.
$$

---

### (c) Difference $\mathbf b - \mathbf a$

$$
\mathbf b - \mathbf a
=
\begin{pmatrix}
5\\2\\-6
\end{pmatrix}
-
\begin{pmatrix}
2\\-3\\1
\end{pmatrix}
=
\begin{pmatrix}
5-2\\2-(-3)\\-6-1
\end{pmatrix}
=
\begin{pmatrix}
3\\5\\-7
\end{pmatrix}.
$$

---

### (d) Dot product $\mathbf a \cdot \mathbf b$

$$
\mathbf a\cdot\mathbf b
=
\begin{pmatrix}
2\\-3\\1
\end{pmatrix}
\cdot
\begin{pmatrix}
5\\2\\-6
\end{pmatrix}
=
2\cdot 5 + (-3)\cdot 2 + 1\cdot (-6)
= 10 - 6 - 6 = -2.
$$

---

### (e) Dot product $\mathbf b \cdot \mathbf a$

Dot product is **commutative**, so:
$$
\mathbf b\cdot\mathbf a = \mathbf a\cdot\mathbf b = -2.
$$

---

### (f) Cross product $\mathbf a \times \mathbf b$

$$
\mathbf a \times \mathbf b
=
\begin{vmatrix}
\hat{\mathbf x} & \hat{\mathbf y} & \hat{\mathbf z}\\
2 & -3 & 1\\
5 & 2 & -6
\end{vmatrix}
=
\hat{\mathbf x}((-3)(-6) - 1\cdot 2)
-\hat{\mathbf y}(2(-6) - 1\cdot 5)
+\hat{\mathbf z}(2\cdot 2 - (-3)\cdot 5).
$$

Compute each term:
- $x$-component: $(-3)(-6) - 1\cdot 2 = 18 - 2 = 16$  
- $y$-component: $2(-6) - 1\cdot 5 = -12 - 5 = -17$, then minus sign gives $+17$  
- $z$-component: $2\cdot 2 - (-3)\cdot 5 = 4 + 15 = 19$  

So:
$$
\mathbf a \times \mathbf b
=
\begin{pmatrix}
16\\17\\19
\end{pmatrix}.
$$

---

### (g) Cross product $\mathbf b \times \mathbf a$

We know:
$$
\mathbf b\times \mathbf a = -(\mathbf a\times \mathbf b).
$$

So:
$$
\mathbf b \times \mathbf a
=
-\begin{pmatrix}
16\\17\\19
\end{pmatrix}
=
\begin{pmatrix}
-16\\-17\\-19
\end{pmatrix}.
$$

---

### Final boxed results

$$
\boxed{
\begin{aligned}
\mathbf a + \mathbf b &= (7,\,-1,\,-5)^T \\
\mathbf a - \mathbf b &= (-3,\,-5,\,7)^T \\
\mathbf b - \mathbf a &= (3,\,5,\,-7)^T \\
\mathbf a\cdot\mathbf b &= -2 \\
\mathbf b\cdot\mathbf a &= -2 \\
\mathbf a\times\mathbf b &= (16,\,17,\,19)^T \\
\mathbf b\times\mathbf a &= (-16,\,-17,\,-19)^T
\end{aligned}
}
$$

---

### MATLAB — Exercise 9.2

> [!code]- MATLAB — Exercise 9.2 
> ```matlab 
>a = [2; -3; 1];
>b = [5;  2; -6];
>
>c_add  = a + b;
>c_sub1 = a - b;
>c_sub2 = b - a;
>
>dot_ab = dot(a,b);
>dot_ba = dot(b,a);
>
>cross_ab = cross(a,b);
>cross_ba = cross(b,a);
>
>fprintf('a + b      = [%g %g %g]^T\n', c_add);
>fprintf('a - b      = [%g %g %g]^T\n', c_sub1);
>fprintf('b - a      = [%g %g %g]^T\n', c_sub2);
>fprintf('a·b        = %g\n', dot_ab);
>fprintf('b·a        = %g\n', dot_ba);
>fprintf('a×b        = [%g %g %g]^T\n', cross_ab);
>fprintf('b×a        = [%g %g %g]^T\n', cross_ba);
>```
---

## Exercise 9.3 — Angle Between Two Vectors

> **Given**  
> (a)  
> $$
> \mathbf a = 3\hat{\mathbf x} + 2\hat{\mathbf y} - 5\hat{\mathbf z},\qquad
> \mathbf b = 9\hat{\mathbf x} - 4\hat{\mathbf y} + 2\hat{\mathbf z}.
> $$
> (b)  
> $$
> \mathbf a =
> \begin{pmatrix}
> 3\\1\\2
> \end{pmatrix},
> \qquad
> \mathbf b =
> \begin{pmatrix}
> -1\\1\\1
> \end{pmatrix}.
> $$
>
> For each pair, find the **angle** $\alpha$ between the vectors.

---

### General formula

For two non-zero vectors:
$$
\cos\alpha = \frac{\mathbf a\cdot\mathbf b}{|\mathbf a||\mathbf b|}.
$$

---

### (a) Cartesian form

Dot product:
$$
\mathbf a\cdot\mathbf b
= 3\cdot 9 + 2\cdot(-4) + (-5)\cdot 2
= 27 - 8 - 10
= 9.
$$

Magnitudes:
$$
|\mathbf a| = \sqrt{3^2 + 2^2 + (-5)^2} = \sqrt{9 + 4 + 25} = \sqrt{38},
$$
$$
|\mathbf b| = \sqrt{9^2 + (-4)^2 + 2^2} = \sqrt{81 + 16 + 4} = \sqrt{101}.
$$

Then:
$$
\cos\alpha = \frac{9}{\sqrt{38}\sqrt{101}} \approx 0.14527,
\quad
\alpha \approx \cos^{-1}(0.14527) \approx 81.65^\circ.
$$

---

### (b) Column form

Dot product:
$$
\mathbf a\cdot\mathbf b
=
\begin{pmatrix}3\\1\\2\end{pmatrix}
\cdot
\begin{pmatrix}-1\\1\\1\end{pmatrix}
= 3(-1) + 1\cdot 1 + 2\cdot 1
= -3 + 1 + 2
= 0.
$$

Thus:
$$
\cos\alpha = \frac{0}{|\mathbf a||\mathbf b|} = 0
\quad\Rightarrow\quad
\alpha = 90^\circ.
$$

They are **orthogonal**.

---

### Final boxed results

$$
\boxed{
\alpha_a \approx 81.65^\circ,
\qquad
\alpha_b = 90^\circ
}
$$

---

### MATLAB — Exercise 9.3

> [!code]- MATLAB — Exercise 9.3
>```matlab  
>% Part (a)
>a1 = [3;  2; -5];
>b1 = [9; -4;  2];
>
>cos_alpha1 = dot(a1,b1)/(norm(a1)*norm(b1));
>alpha1_deg = acosd(cos_alpha1);
>
>% Part (b)
>a2 = [3; 1; 2];
>b2 = [-1; 1; 1];
>
>cos_alpha2 = dot(a2,b2)/(norm(a2)*norm(b2));
>alpha2_deg = acosd(cos_alpha2);
>
>fprintf('Part (a): alpha ≈ %.2f deg\n', alpha1_deg);
>fprintf('Part (b): alpha ≈ %.2f deg\n', alpha2_deg);
>```
---

## Exercise 9.4 — Mixed Vector Identities with Triple Products

> **Given**  
> Three vectors:
> $$
> \mathbf a = \hat{\mathbf x} + 2\hat{\mathbf y} - 3\hat{\mathbf z},\quad
> \mathbf b = 2\hat{\mathbf x} - 4\hat{\mathbf y} + 0\hat{\mathbf z},\quad
> \mathbf c = 0\hat{\mathbf x} + 2\hat{\mathbf y} - 4\hat{\mathbf z}.
> $$
> i.e.
> $$
> \mathbf a=
> \begin{pmatrix}1\\2\\-3\end{pmatrix},\ 
> \mathbf b=
> \begin{pmatrix}2\\-4\\0\end{pmatrix},\ 
> \mathbf c=
> \begin{pmatrix}0\\2\\-4\end{pmatrix}.
> $$
>
> Compute:
> (a) $\mathbf a\cdot(\mathbf b\times\mathbf c)$  
> (b) $(\mathbf b\times\mathbf c)\cdot\mathbf a$  
> (c) $\mathbf a\times(\mathbf b\times\mathbf c)$  
> (d) $(\mathbf b\times\mathbf c)\times\mathbf a$  
> (e) $(\mathbf c\times\mathbf b)\times\mathbf a$  
> (f) $(\mathbf a\times\mathbf b)\times\mathbf c$  
> (g) $\hat{\mathbf x}\times\mathbf b$  
> (h) $(\mathbf a\times\hat{\mathbf y})\cdot\hat{\mathbf z}$  

---

### Pre-computation: $\mathbf b\times\mathbf c$

$$
\mathbf b\times\mathbf c
=
\begin{vmatrix}
\hat{\mathbf x} & \hat{\mathbf y} & \hat{\mathbf z}\\
2 & -4 & 0\\
0 & 2 & -4
\end{vmatrix}
=
\hat{\mathbf x}((-4)(-4) - 0\cdot 2)
-\hat{\mathbf y}(2(-4) - 0\cdot 0)
+\hat{\mathbf z}(2\cdot 2 - (-4)\cdot 0).
$$

Compute:

- $x$-component: $(-4)(-4) - 0 = 16$  
- $y$-component: $2(-4) - 0 = -8$, with minus → $+8$  
- $z$-component: $2\cdot 2 - 0 = 4$  

So:
$$
\mathbf b\times\mathbf c =
\begin{pmatrix}
16\\8\\4
\end{pmatrix}.
$$

---

### (a) $\mathbf a\cdot(\mathbf b\times\mathbf c)$

$$
\mathbf a\cdot(\mathbf b\times\mathbf c)
=
\begin{pmatrix}1\\2\\-3\end{pmatrix}
\cdot
\begin{pmatrix}16\\8\\4\end{pmatrix}
= 1\cdot 16 + 2\cdot 8 + (-3)\cdot 4
= 16 + 16 - 12
= 20.
$$

---

### (b) $(\mathbf b\times\mathbf c)\cdot\mathbf a$

Scalar triple product is **cyclically invariant**, so  

$$
(\mathbf b\times\mathbf c)\cdot\mathbf a
= 20.
$$

---

### (c) $\mathbf a\times(\mathbf b\times\mathbf c)$

$$
\mathbf a\times(\mathbf b\times\mathbf c)
=
\begin{pmatrix}1\\2\\-3\end{pmatrix}
\times
\begin{pmatrix}16\\8\\4\end{pmatrix}.
$$

Components:

- $x$-component: $2\cdot 4 - (-3)\cdot 8 = 8 + 24 = 32$  
- $y$-component: $(-3)\cdot 16 - 1\cdot 4 = -48 - 4 = -52$  
- $z$-component: $1\cdot 8 - 2\cdot 16 = 8 - 32 = -24$

Thus:
$$
\mathbf a\times(\mathbf b\times\mathbf c)
=
\begin{pmatrix}
32\\-52\\-24
\end{pmatrix}.
$$

---

### (d) $(\mathbf b\times\mathbf c)\times\mathbf a$

$$
(\mathbf b\times\mathbf c)\times\mathbf a
=
\begin{pmatrix}16\\8\\4\end{pmatrix}
\times
\begin{pmatrix}1\\2\\-3\end{pmatrix}.
$$

Components:

- $x$-component: $8\cdot(-3) - 4\cdot 2 = -24 - 8 = -32$  
- $y$-component: $4\cdot 1 - 16\cdot(-3) = 4 + 48 = 52$  
- $z$-component: $16\cdot 2 - 8\cdot 1 = 32 - 8 = 24$

So:
$$
(\mathbf b\times\mathbf c)\times\mathbf a
=
\begin{pmatrix}
-32\\52\\24
\end{pmatrix}.
$$

---

### (e) $(\mathbf c\times\mathbf b)\times\mathbf a$

We know:
$$
\mathbf c\times\mathbf b = -(\mathbf b\times\mathbf c)
= -\begin{pmatrix}16\\8\\4\end{pmatrix}
=
\begin{pmatrix}-16\\-8\\-4\end{pmatrix}.
$$

Then:
$$
(\mathbf c\times\mathbf b)\times\mathbf a
=
\begin{pmatrix}-16\\-8\\-4\end{pmatrix}
\times
\begin{pmatrix}1\\2\\-3\end{pmatrix}.
$$

This is just $-(\mathbf b\times\mathbf c)\times\mathbf a$, so:
$$
(\mathbf c\times\mathbf b)\times\mathbf a
=
-\begin{pmatrix}
-32\\52\\24
\end{pmatrix}
=
\begin{pmatrix}
32\\-52\\-24
\end{pmatrix}.
$$

---

### (f) $(\mathbf a\times\mathbf b)\times\mathbf c$

First compute:
$$
\mathbf a\times\mathbf b
=
\begin{pmatrix}
1\\2\\-3
\end{pmatrix}
\times
\begin{pmatrix}
2\\-4\\0
\end{pmatrix}.
$$

Components:

- $x$-component: $2\cdot 0 - (-3)(-4) = 0 - 12 = -12$  
- $y$-component: $(-3)\cdot 2 - 1\cdot 0 = -6 - 0 = -6$  
- $z$-component: $1(-4) - 2\cdot 2 = -4 - 4 = -8$

So:
$$
\mathbf a\times\mathbf b =
\begin{pmatrix}-12\\-6\\-8\end{pmatrix}.
$$

Now:
$$
(\mathbf a\times\mathbf b)\times\mathbf c
=
\begin{pmatrix}-12\\-6\\-8\end{pmatrix}
\times
\begin{pmatrix}0\\2\\-4\end{pmatrix}.
$$

Components:

- $x$-component: $(-6)(-4) - (-8)\cdot 2 = 24 + 16 = 40$  
- $y$-component: $(-8)\cdot 0 - (-12)\cdot(-4) = 0 - 48 = -48$  
- $z$-component: $(-12)\cdot 2 - (-6)\cdot 0 = -24 - 0 = -24$

Thus:
$$
(\mathbf a\times\mathbf b)\times\mathbf c
=
\begin{pmatrix}
40\\-48\\-24
\end{pmatrix}.
$$

---

### (g) $\hat{\mathbf x}\times\mathbf b$

$$
\hat{\mathbf x}\times\mathbf b
=
\begin{pmatrix}1\\0\\0\end{pmatrix}
\times
\begin{pmatrix}2\\-4\\0\end{pmatrix}.
$$

Components:

- $x$-component: $0\cdot 0 - 0\cdot (-4) = 0$  
- $y$-component: $0\cdot 2 - 1\cdot 0 = 0$  
- $z$-component: $1\cdot(-4) - 0\cdot 2 = -4$

So:
$$
\hat{\mathbf x}\times\mathbf b = (0,0,-4)^T = -4\hat{\mathbf z}.
$$

---

### (h) $(\mathbf a\times\hat{\mathbf y})\cdot\hat{\mathbf z}$

$$
\hat{\mathbf y} =
\begin{pmatrix}0\\1\\0\end{pmatrix},\quad
\mathbf a=
\begin{pmatrix}1\\2\\-3\end{pmatrix}.
$$

Compute $\mathbf a\times\hat{\mathbf y}$:

- $x$-component: $2\cdot 0 - (-3)\cdot 1 = 3$  
- $y$-component: $(-3)\cdot 0 - 1\cdot 0 = 0$  
- $z$-component: $1\cdot 1 - 2\cdot 0 = 1$

So:
$$
\mathbf a\times\hat{\mathbf y} = (3,0,1)^T.
$$

Then:
$$
(\mathbf a\times\hat{\mathbf y})\cdot\hat{\mathbf z}
=
\begin{pmatrix}3\\0\\1\end{pmatrix}
\cdot
\begin{pmatrix}0\\0\\1\end{pmatrix}
= 1.
$$

---

### Final boxed results (Exercise 9.4)

$$
\boxed{
\begin{aligned}
\text{(a)}&\quad \mathbf a\cdot(\mathbf b\times\mathbf c) = 20 \\
\text{(b)}&\quad (\mathbf b\times\mathbf c)\cdot\mathbf a = 20 \\
\text{(c)}&\quad \mathbf a\times(\mathbf b\times\mathbf c) = (32,\,-52,\,-24)^T \\
\text{(d)}&\quad (\mathbf b\times\mathbf c)\times\mathbf a = (-32,\,52,\,24)^T \\
\text{(e)}&\quad (\mathbf c\times\mathbf b)\times\mathbf a = (32,\,-52,\,-24)^T \\
\text{(f)}&\quad (\mathbf a\times\mathbf b)\times\mathbf c = (40,\,-48,\,-24)^T \\
\text{(g)}&\quad \hat{\mathbf x}\times\mathbf b = (0,0,-4)^T = -4\hat{\mathbf z} \\
\text{(h)}&\quad (\mathbf a\times\hat{\mathbf y})\cdot\hat{\mathbf z} = 1
\end{aligned}
}
$$

---

### MATLAB — Exercise 9.4

> [!code]- MATLAB — Exercise 9.4  
> ```matlab
>a = [1; 2; -3];
>b = [2; -4;  0];
>c = [0; 2; -4];
>
>bx_c = cross(b,c);
>ax_bx_c = cross(a, bx_c);
>bx_cx_a = cross(bx_c, a);
>cx_b = cross(c,b);
>cx_bx_a = cross(cx_b, a);
>ax_b = cross(a,b);
>ax_bx_c2 = cross(ax_b, c);
>
>res_a = dot(a, bx_c);
>res_b = dot(bx_c, a);
>res_g = cross([1;0;0], b);
>res_h = dot(cross(a, [0;1;0]), [0;0;1]);
>
>fprintf('(a) a·(b×c)          = %g\n', res_a);
>fprintf('(b) (b×c)·a          = %g\n', res_b);
>fprintf('(c) a×(b×c)          = [%g %g %g]^T\n', ax_bx_c);
>fprintf('(d) (b×c)×a          = [%g %g %g]^T\n', bx_cx_a);
>fprintf('(e) (c×b)×a          = [%g %g %g]^T\n', cx_bx_a);
>fprintf('(f) (a×b)×c          = [%g %g %g]^T\n', ax_bx_c2);
>fprintf('(g) x-hat×b          = [%g %g %g]^T\n', res_g);
>fprintf('(h) (a×y-hat)·z-hat  = %g\n', res_h);
>```
---

## Exercise 9.5 — Vector Perpendicular to Two Given Vectors with Given Magnitude

> **Given**  
> Two vectors:
> $$
> \mathbf a = 2\hat{\mathbf x} - \hat{\mathbf y} + 3\hat{\mathbf z},\qquad
> \mathbf b = 3\hat{\mathbf x} - 2\hat{\mathbf z}.
> $$
>  
> Find a vector $\mathbf c$ such that:
> - $\mathbf c$ is **perpendicular** to both $\mathbf a$ and $\mathbf b$  
> - $|\mathbf c| = 9$  

---

### Strategy

- A vector **perpendicular** to both $\mathbf a$ and $\mathbf b$ is given (up to sign) by the **cross product**:
  $$
  \mathbf c_0 = \mathbf a\times\mathbf b.
  $$
- Then **scale** $\mathbf c_0$ to have magnitude 9.

---

### Step 1: Cross product $\mathbf a\times\mathbf b$

Write components:
$$
\mathbf a =
\begin{pmatrix}
2\\-1\\3
\end{pmatrix},
\quad
\mathbf b =
\begin{pmatrix}
3\\0\\-2
\end{pmatrix}.
$$

Compute:
$$
\mathbf a\times\mathbf b
=
\begin{pmatrix}
2\\-1\\3
\end{pmatrix}
\times
\begin{pmatrix}
3\\0\\-2
\end{pmatrix}.
$$

Components:

- $x$-component: $(-1)(-2) - 3\cdot 0 = 2$  
- $y$-component: $3\cdot 3 - 2(-2) = 9 + 4 = 13$  
- $z$-component: $2\cdot 0 - (-1)\cdot 3 = 0 + 3 = 3$

So:
$$
\mathbf c_0 = \mathbf a\times\mathbf b =
\begin{pmatrix}
2\\13\\3
\end{pmatrix}.
$$

---

### Step 2: Magnitude of $\mathbf c_0$

$$
\|\mathbf c_0\|
= \sqrt{2^2 + 13^2 + 3^2}
= \sqrt{4 + 169 + 9}
= \sqrt{182}.
$$

---

### Step 3: Scale to magnitude 9

We need a scalar $\alpha$ such that:
$$
\mathbf c = \alpha\mathbf c_0,\quad
\|\mathbf c\| = 9.
$$

Since $\|\alpha\mathbf c_0\| = |\alpha|\|\mathbf c_0\|$, choose:
$$
\alpha = \frac{9}{\|\mathbf c_0\|} = \frac{9}{\sqrt{182}}.
$$

Thus:
$$
\mathbf c = \alpha\mathbf c_0
= \frac{9}{\sqrt{182}}
\begin{pmatrix}
2\\13\\3
\end{pmatrix}
=
\begin{pmatrix}
\frac{18}{\sqrt{182}}\\[4pt]
\frac{117}{\sqrt{182}}\\[4pt]
\frac{27}{\sqrt{182}}
\end{pmatrix}.
$$

A second valid solution is $-\mathbf c$ (same magnitude, opposite direction).

---

### Final boxed results

One valid vector is:
$$
\boxed{
\mathbf c = \frac{9}{\sqrt{182}}
\left(2\hat{\mathbf x} + 13\hat{\mathbf y} + 3\hat{\mathbf z}\right),
\quad
|\mathbf c| = 9.
}
$$

The opposite:
$$
\boxed{
-\mathbf c
}
$$
is also perpendicular to both $\mathbf a$ and $\mathbf b$ and has the same magnitude.

---

### MATLAB — Exercise 9.5

> [!code]- MATLAB — Exercise 9.5
> ```matlab  
>a = [2; -1; 3];
>b = [3;  0; -2];
>
>c0   = cross(a,b);          % perpendicular to both
>c0_n = norm(c0);
>
>alpha = 9 / c0_n;
>c     = alpha * c0;
>
>fprintf('c0      = [%g %g %g]^T, ||c0|| = %.6f\n', c0, c0_n);
>fprintf('c (|c|=9) = [%g %g %g]^T, ||c|| = %.6f\n', c, norm(c));
>```
