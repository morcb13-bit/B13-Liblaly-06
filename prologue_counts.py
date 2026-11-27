# 6冊目『物の形』序章の数え上げ。整数と加算と比較だけで書く。
# (0) 水分子を立方体に置く：酸素＝2段のギャスケット、水素＝1段のギャスケット。
#     水素を置ける16通りのうち、面で付くもの・球が内側から接するもの・腕の角
# (1) 正四面体の辺を n 個に割ったときの、上向き・正八面体・逆向きの個数
# (2) フィボナッチの組 (x, y) のノルム y*y - x*y - x*x

def mul(a, b):
    # 掛け算は足し算の繰り返し（符号は外で処理）
    neg = (a < 0) != (b < 0)
    a, b = abs(a), abs(b)
    s = 0
    for _ in range(b):
        s += a
    return -s if neg else s

def half(v):
    # 偶数を2で割る（足し算で数える）
    neg = v < 0
    v = abs(v)
    h = 0
    while h + h < v:
        h += 1
    assert h + h == v
    return -h if neg else h

def mid(p, q):
    return tuple(half(p[k] + q[k]) for k in range(3))

def gasket(verts, depth):
    # 段数 depth のギャスケットの点の集合
    if depth == 0:
        return set(verts)
    out = set()
    for i in range(4):
        sub = [mid(verts[i], verts[j]) for j in range(4)]
        out |= gasket(sub, depth - 1)
    return out

def cells(verts, depth):
    # 段数 depth のギャスケットの小さな正四面体（頂点の組）の集合
    if depth == 0:
        return {frozenset(verts)}
    out = set()
    for i in range(4):
        out |= cells([mid(verts[i], verts[j]) for j in range(4)], depth - 1)
    return out

def sub3(p, q): return tuple(p[k] - q[k] for k in range(3))
def dot(a, b): return mul(a[0], b[0]) + mul(a[1], b[1]) + mul(a[2], b[2])

# ---- (0) 水分子 ----
print("(0) 一辺4の立方体に置いた水分子")
O = [(0, 0, 0), (4, 4, 0), (4, 0, 4), (0, 4, 4)]       # 酸素：立方体の角を4つ使う
O_pts = gasket(O, 2)
O_cells = cells(O, 2)
O_c = (2, 2, 2)
O_r2 = dot(sub3(O[0], O_c), sub3(O[0], O_c))
print(f"  酸素：2段のギャスケットの点 {len(O_pts)}、外接球の半径の2乗 {O_r2}")

# 水素の候補：一辺2の小さな立方体8つ × 向き2通り（偶の向き・鏡の向き）＝16
cands = []
for ox in (0, 2):
    for oy in (0, 2):
        for oz in (0, 2):
            base = (ox, oy, oz)
            even = [(0, 0, 0), (2, 2, 0), (2, 0, 2), (0, 2, 2)]
            odd = [(2, 0, 0), (0, 2, 0), (0, 0, 2), (2, 2, 2)]
            for name, t in (("偶", even), ("鏡", odd)):
                verts = [tuple(base[k] + v[k] for k in range(3)) for v in t]
                cands.append((name, verts))

face_att = []
overlap = 0
for name, H in cands:
    if cells(H, 1) & O_cells:      # 酸素の小さな正四面体と同じ升を使うものは置けない
        overlap += 1
        continue
    H_pts = gasket(H, 1)
    H_c = tuple(base_c for base_c in mid(mid(H[0], H[1]), mid(H[2], H[3])))
    # 面で付く：水素のどれか一つの面の6点（頂点3＋中点3）がすべて酸素の点
    face = False
    for skip in range(4):
        tri = [H[i] for i in range(4) if i != skip]
        six = set(tri) | {mid(tri[0], tri[1]), mid(tri[1], tri[2]), mid(tri[0], tri[2])}
        if six <= O_pts:
            face = True
    if face:
        H_r2 = dot(sub3(H[0], H_c), sub3(H[0], H_c))
        d2 = dot(sub3(H_c, O_c), sub3(H_c, O_c))
        # 内側から接する ⇔ d = rO − rH ⇔ (rO²＋rH²−d²)² ＝ 4·rO²·rH² かつ rO² > rH²
        lhs = O_r2 + H_r2 - d2
        inner = mul(lhs, lhs) == mul(4, mul(O_r2, H_r2)) and lhs > 0 and O_r2 > H_r2
        out_corner = [v for v in H if v not in O_pts]
        face_att.append((H_c, H_r2, d2, inner, out_corner))

print(f"  水素の置き場の候補 {len(cands)}、酸素と重なるもの {overlap}、重ならずに面で付くもの {len(face_att)}")
for c, r2, d2, inner, oc in face_att:
    print(f"    中心 {c}  半径の2乗 {r2}  中心距離の2乗 {d2}  内側から接する {inner}  酸素の外の頂点 {oc}")

arms = [sub3(c, O_c) for c, *_ in face_att]
keys = set()
for i in range(len(arms)):
    for j in range(i + 1, len(arms)):
        d = dot(arms[i], arms[j])
        keys.add((d, dot(arms[i], arms[i]), dot(arms[j], arms[j])))
print(f"  腕の組 {len(arms)*(len(arms)-1)//2}、（内積, 長さの2乗, 長さの2乗）の種類 {sorted(keys)}")
if len(keys) == 1 and list(keys)[0] == (-1, 3, 3):
    print("  → 余弦は −1/3 の一つ（どの二つの水素を選んでも同じ）")
else:
    print("  → NG：角が一つに決まらない")

# ---- (1) 正四面体を n に割る ----
def tuples(s):
    c = 0
    for i in range(s + 1):
        for j in range(s + 1 - i):
            for k in range(s + 1 - i - j):
                c += 1
    return c

print()
print("(1) 辺を n に割る：上向き / 正八面体 / 逆向き / 体積 / n^3")
ok = True
for n in range(1, 14):
    up = tuples(n - 1)
    octa = tuples(n - 2) if n >= 2 else 0
    down = tuples(n - 3) if n >= 3 else 0
    vol = up + octa + octa + octa + octa + down
    cube = mul(mul(n, n), n)
    ok = ok and vol == cube
    print(f"  n={n:2d}: {up:4d} / {octa:4d} / {down:4d} / {vol:5d} / {cube:5d}  {'OK' if vol == cube else 'NG'}")
print("  すべて一致" if ok else "  不一致あり")

# ---- (2) フィボナッチの組のノルム ----
print()
print("(2) フィボナッチの組 (x, y) とノルム y^2 - xy - x^2")
def norms(x, y, steps):
    out = []
    for _ in range(steps):
        out.append(mul(y, y) - mul(x, y) - mul(x, x))
        x, y = y, x + y
    return out
s = norms(0, 1, 26)
print(f"  0,1 から26組：ノルム {sorted(set(s))}、符号が交互 {'OK' if all(s[i] == -s[i+1] for i in range(25)) else 'NG'}")
print(f"  負の対照（2,1 から26組）：ノルム {sorted(set(norms(2, 1, 26)))}")
