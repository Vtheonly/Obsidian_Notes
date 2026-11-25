# 60-Second Exam Recovery Sheet

*The ASCII memory dump to write on scrap paper the moment the exam begins. It compresses the seven Universal Core Invariants and the highest-frequency signatures of the 26 companion notes into one writable block. Every line below is verified against live library behavior (NumPy 2.1.3 / Pandas 2.2.3 / OpenCV 4.13.0 / SciPy / Scikit-Learn / Matplotlib / Seaborn).*

```text
======================= 60-SECOND EXAM BRAIN DUMP =======================
1. COORDS:   NumPy = [row, col] -> [y, x]   |   OpenCV = (col, row) -> (x, y)
             h, w = img.shape[:2]  (works gray AND color)
2. RADIUS:   rad = ksize // 2 (DOUBLE SLASH! / gives float -> slice crash)
    SANDWICH: np.clip(np.round(img.astype(np.float64) OP x), 0, 255).astype(np.uint8)
3. OPENCV:   resize(im, (w, h))  [W FIRST!] |  rectangle(im, (x1, y1), (x2, y2), BGR, t)
             blur(im, (k, k)) TUPLE          |  GaussianBlur(im, (k, k), sigmaX)
             medianBlur(im, k) INTEGER ONLY! |  bilateralFilter(im, d, sc, ss) 4 args
             _, mask = cv2.threshold(g, T, 255, cv2.THRESH_BINARY)   [TUPLE!]
             calcHist([im], [0], None, [256], [0, 256])  [I-C-M-B-R, 256 exclusive]
             n, lab, stats, cent = cv2.connectedComponentsWithStats(m, 8)
             objects = n - 1  (label 0 = background);  stats[i, cv2.CC_STAT_AREA]
             pad reflect:  np.pad(im, r, 'reflect') == cv2.BORDER_REFLECT_101
             if img is None: raise FileNotFoundError(path)   [NEVER img == None]
4. NUMPY:    attrs bare (.shape .dtype .T)  |  methods called (.copy() .astype())
             arr.median() DOES NOT EXIST -> np.median(arr)
             masks: (a > 80) & (a <= 150)   [PARENTHESES MANDATORY]
             sort copy: np.sort(a) | in-place a.sort() returns None
             descending: a[np.argsort(a)[::-1]]  |  argmax -> np.unravel_index(f, shape)
             randint(high EXCLUSIVE): [0,20] -> randint(0,21)
             rand(H, W) loose ints | normal(mu, sig, (H, W)) TUPLE
             solve: x = np.linalg.solve(A, b)   [NOT inv(A) @ b; A.T no parens]
5. PANDAS:   .loc['A':'C'] INCLUSIVE | .iloc[0:2] EXCLUSIVE
             df[(df.A > 5) & (df.B < 10)] | query('A > 5 and B < 10')
             df = df.dropna()  [NEVER df = df.dropna(inplace=True) -> None]
             methods: dropna fillna drop rename groupby sort_values
             top-level: pd.get_dummies pd.concat pd.merge pd.to_datetime pd.crosstab
             df.drop(columns=['x']) [default searches ROWS!] rename(columns={...})
             .str.lower() .dt.year  [accessors mandatory on Series]
             rolling(window=3).mean() keeps rows | resample('QE').sum() collapses
             agg collapses | transform('mean') broadcasts (dept-average diff!)
             get_dummies(df, columns=['Sex'], drop_first=True, dtype=int)
6. SKLEARN:  df[['Age']] 2D DOUBLE BRACKETS! | X = img.reshape((-1, 3)).astype(np.float32)
             X_train, X_test, y_train, y_test = train_test_split(X, y, 0.2, random_state=42)
             fit_transform(X_train) | transform(X_test) ONLY [leakage!]
             jaccard_score(gt.ravel(), pred.ravel())
7. METRICS:  PSNR = 10.0 * np.log10((255.0 ** 2) / mse)  [** NOT ^! log10 NOT log!]
             if mse == 0.0: return float('inf')   [guard BEFORE dividing]
8. MPL/SNS:  ax.set_title (NOT ax.title) | imshow(gray, cmap='gray', vmin=0, vmax=255)
             ax.axis('off') | ax.hist(im.ravel(), bins=256, range=(0, 256))
             sns.histplot(data=df, x=..., kde=True, ax=ax) | sns.heatmap(df.corr(), annot=True, fmt='.2f')
             CV images -> cv2.cvtColor(im, cv2.COLOR_BGR2RGB) before plt
==========================================================================
```

## How to Use

1. **At T+0:** write the block verbatim on scrap paper (60-90 seconds; practice until it fits in one minute).
2. **During the exam:** consult the paper, not your memory — the dump frees working memory for the actual problem.
3. **After the exam (motor recall drills):** the block is the reference key for the 15-minute protocol below.

Cross-references: the full invariant derivations live in `Computer Vision.md` Sections 1-2; each numbered family expands into its companion note (`01.5`-`26.5` in `Libraries/`).

---

# 15-Minute Daily Motor Recall Protocol

*Reading code builds passive recognition; written exams test physical motor production. Daily protocol, 15 minutes, pen and blank paper only — no screens, no notes, no interpreter.*

## Step 1 - Setup (30 seconds)
Remove all screens, keyboards, and references. One blank sheet, one pen. Set a 15-minute timer.

## Step 2 - Write the Five Core Routines from memory (9 minutes)

**Routine 1 - Load, convert, save:**
```python
import cv2, numpy as np
img = cv2.imread("photo.bmp")
if img is None: raise FileNotFoundError("photo.bmp")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("out.bmp", gray)
```

**Routine 2 - Both noise generators:**
```python
def add_gaussian_noise(img, var=100.0):
    noise = np.random.normal(0.0, np.sqrt(var), img.shape)
    return np.clip(img.astype(np.float64) + noise, 0, 255).astype(np.uint8)

def add_salt_pepper(img, p=0.10):
    noisy = img.copy(); rnd = np.random.rand(*img.shape[:2])
    noisy[rnd < p / 2] = 255; noisy[rnd > 1 - p / 2] = 0
    return noisy
```

**Routine 3 - Manual 3x3 mean and median filters (np.pad + loops):**
```python
def mean_filter(img, k=3):
    rad = k // 2
    p = np.pad(img.astype(np.float64), rad, mode="reflect")
    out = np.zeros(img.shape, dtype=np.uint8)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            win = p[y:y + k, x:x + k]
            out[y, x] = int(round(win.sum() / (k * k)))
    return out

def median_filter(img, k=3):
    rad = k // 2
    p = np.pad(img.astype(np.float64), rad, mode="reflect")
    out = np.zeros(img.shape, dtype=np.uint8)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            vals = np.sort(p[y:y + k, x:x + k].ravel())
            out[y, x] = int(vals[vals.size // 2])
    return out
```

**Routine 4 - Histogram both ways:**
```python
hist_cv = cv2.calcHist([gray], [0], None, [256], [0, 256]).ravel()
hist_np = np.bincount(gray.ravel(), minlength=256)
```

**Routine 5 - MSE and PSNR with the zero guard:**
```python
def mse(a, b):
    d = a.astype(np.float64) - b.astype(np.float64)
    return float(np.mean(d ** 2))

def psnr(a, b, R=255.0):
    m = mse(a, b)
    if m == 0.0: return float("inf")
    return 10.0 * np.log10((R ** 2) / m)
```

## Step 3 - Red-pen comparison (4 minutes)
Open `Computer Vision.md` (Sections 6 and 7) and the companion notes. Compare your sheet line by line, character by character. Circle every deviation: float indices from a single `/`, missing tuple brackets, wrong ksize dialect (median int vs. blur tuple), forgotten `.astype`, `^` instead of `**`, `log` instead of `log10`, unpacking failures.

## Step 4 - Immediate triple rewrite (2 minutes)
Rewrite each flawed line correctly THREE consecutive times. Motor memory consolidates through corrected repetition, not through re-reading.

## Weekly Rotation
- **Mon/Wed/Fri:** the five core routines above.
- **Tue/Thu:** the Pandas triple — cleaning pipeline (`dropna`/`fillna`/`.str`/`get_dummies`), the groupby pair (`.agg` + `.transform`), the merge/concat pair.
- **Saturday:** the 60-second brain dump itself + one full exam archetype from the companion notes.
- **Sunday:** rest; recognition-mode review only (read one parent note of your weakest family).

## Exit Criterion
You are exam-ready on a routine when you can write it, unprompted, with zero deviations, three days in a row.
