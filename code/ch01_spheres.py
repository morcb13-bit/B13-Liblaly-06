# 6冊目『物の形』第1章　ギャスケットに接する球
# 整数と加算と比較だけで書く。
# 検定1：ギャスケットの頂点に、直径＝いちばん短い辺の球を置く（球棒の模型の側）
#        接する組・重なる組を数え、同じ大きさの正四面体に球を詰めた数と比べる
# 検定2：一個の球で囲む（空間充填の模型の側）
#        外接球・中接球・内接球の半径の2乗の比と、ギャスケットの点が各球の上・内・外にいくつあるか

def half(v):
    neg = v < 0
    v = abs(v)
    h = 0
    while h + h < v:
        h += 1
    assert h + h == v
    return -h if neg else h

def mul(a, b):
    neg = (a < 0) != (b < 0)
    a, b = abs(a), abs(b)
    s = 0
    for _ in range(b):
        s += a
    return -s if neg else s

def mid(p, q):
    return tuple(half(p[k] + q[k]) for k in range(3))

def gasket(verts, depth):
    if depth == 0:
        return set(verts)
    out = set()
    for i in range(4):
        out |= gasket([mid(verts[i], verts[j]) for j in range(4)], depth - 1)
    return out

def d2(p, q):
    s = 0
    for k in range(3):
        t = p[k] - q[k]
        s += mul(t, t)
    return s

def big_tetra(s):
    return [(0, 0, 0), (s, s, 0), (s, 0, s), (0, s, s)]

def packed_count(s):
    # 辺を s に割った正四面体の格子点の数（4つの非負整数の和が s）を足し算で数える
    c = 0
    for i in range(s + 1):
        for j in range(s + 1 - i):
            for k in range(s + 1 - i - j):
                c += 1
    return c

# ---------------- 検定1 ----------------
print("検定1　頂点に置いた球（直径＝いちばん短い辺、距離の2乗で 2）")
print(" 段 | 頂点 | 詰めた球 | 差 | 接する組 | 重なる組 | 一つの球が接する数（最小〜最大）")
ok1 = True
s = 1
prev_expected = None
for k in range(5):
    pts = sorted(gasket(big_tetra(s), k))
    n = len(pts)
    contact = 0
    overlap = 0
    deg = {p: 0 for p in pts}
    for i in range(n):
        for j in range(i + 1, n):
            dd = d2(pts[i], pts[j])
            if dd < 2:
                overlap += 1
            elif dd == 2:
                contact += 1
                deg[pts[i]] += 1
                deg[pts[j]] += 1
    packed = packed_count(s)
    expect = mul(2, 4 ** k) + 2
    if overlap != 0 or n != expect:
        ok1 = False
    print(f" {k:2d} | {n:4d} | {packed:8d} | {packed - n:3d} | {contact:8d} | {overlap:8d} | {min(deg.values())}〜{max(deg.values())}")
    s = s + s
print(" 判定：", "OK（重なり 0、頂点の数は 2×4^k＋2）" if ok1 else "NG")

# 2 段で、詰めた山とギャスケットの差を点ごとに見る
def packed_points(s):
    # 辺 s の正四面体の格子点：e1=(1,1,0), e2=(1,0,1), e3=(0,1,1) の非負整数の組み合わせで和が s 以下
    out = set()
    for i in range(s + 1):
        for j in range(s + 1 - i):
            for k in range(s + 1 - i - j):
                out.add((i + j, i + k, j + k))
    return out
P = packed_points(4)
G = gasket(big_tetra(4), 2)
missing = sorted(P - G)
print(f" 2段で、詰めた山にあってギャスケットにない点：{missing}（正八面体の穴の中心）")
def contacts(points):
    pts = sorted(points)
    c = 0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if d2(pts[i], pts[j]) == 2:
                c += 1
    return c
print(f" 接する組：詰めた山 35 点で {contacts(P)}、ギャスケット 34 点で {contacts(G)}、抜けた 1 点が接していた数 {sum(1 for q in G if d2(q, missing[0]) == 2)}")

# ---------------- 検定2 ----------------
print()
print("検定2　一個の球で囲む（座標を 3 倍して整数にする）")
S = 12                      # 辺 12 の大きな正四面体（もとの辺 4 を 3 倍）
T = big_tetra(S)
C = (6, 6, 6)               # 中心
R_out = d2(T[0], C)                                  # 外接球：頂点を通る
R_mid = d2(mid(T[0], T[1]), C)                       # 中接球：辺の中点を通る
# 内接球：面 (S,S,0),(S,0,S),(0,S,S) の平面 x+y+z=2S への距離の2乗 ＝ (2S−18)²/3
num = mul(2 * S - 18, 2 * S - 18)
q = 0
while q + q + q < num:
    q += 1
assert q + q + q == num, "割り切れない"
R_in = q
print(f" 半径の2乗：外接 {R_out}、中接 {R_mid}、内接 {R_in}")
g = R_in
for v in (R_out, R_mid):
    a, b = g, v
    while b:
        a, b = b, a % b
    g = a
ratio = (R_out // g, R_mid // g, R_in // g)
ok2 = ratio == (9, 3, 1)
print(f" 比：{ratio[0]}：{ratio[1]}：{ratio[2]}　判定：{'OK' if ok2 else 'NG'}")

print(" ギャスケットの点（座標 3 倍）が各球の 上 / 内 / 外 にいくつあるか")
print(" 段 | 点 | 外接球 上/内/外 | 中接球 上/内/外 | 内接球 上/内/外")
for k in range(4):
    # 3 倍した座標で段 k のギャスケットを作るため、辺 4·2^k の正四面体を作ってから 3 倍し、中心を合わせる
    base = 4
    scale = 1
    for _ in range(k):
        scale += scale
    pts = gasket(big_tetra(mul(base, scale)), k)  # 辺 4·2^k、段 k
    # 大きさを辺 12 に縮めると端数が出るので、半径の2乗の方を (2^k)^2 倍して比べる
    sc2 = mul(scale, scale)
    pts3 = [(3 * p[0], 3 * p[1], 3 * p[2]) for p in pts]
    c3 = (mul(6, scale), mul(6, scale), mul(6, scale))
    row = []
    for Rr in (R_out, R_mid, R_in):
        Rs = mul(Rr, sc2)
        on = inn = out = 0
        for p in pts3:
            dd = d2(p, c3)
            if dd == Rs:
                on += 1
            elif dd < Rs:
                inn += 1
            else:
                out += 1
        row.append(f"{on:3d}/{inn:3d}/{out:3d}")
    print(f" {k:2d} | {len(pts):3d} | {row[0]}     | {row[1]}     | {row[2]}")

# ---------------- 検定2b：入れ子の外接球 ----------------
# 段 k のギャスケットの小さな正四面体それぞれに外接球をかぶせる。
# 親（一つ上の段）の外接球と子の外接球が、内側から接するか（(R²＋r²−d²)² ＝ 4R²r²、R²＋r²−d² > 0）
# 子どうしは重なるか・接するか・離れるか（d と 2r の比較 ⇔ d² と 4r²）
print()
print("検定2b　入れ子の外接球（座標を 2 倍して中心を整数にする）")
def cells(verts, depth):
    if depth == 0:
        return [verts]
    out = []
    for i in range(4):
        out += cells([mid(verts[i], verts[j]) for j in range(4)], depth - 1)
    return out
def center2(t):   # 中心の 2 倍（整数）
    return tuple(half(t[0][k] + t[1][k] + t[2][k] + t[3][k]) for k in range(3))
ok2b = True
S0 = 16
for k in range(1, 4):
    parents = cells(big_tetra(S0), k - 1)
    tang = 0
    tang_pts = set()
    pair_over = pair_touch = pair_apart = 0
    for P_ in parents:
        Pc = center2(P_)
        R2 = d2(tuple(2 * v for v in P_[0]), Pc)
        kids = cells(P_, 1)
        for K in kids:
            Kc = center2(K)
            r2 = d2(tuple(2 * v for v in K[0]), Kc)
            dd = d2(Pc, Kc)
            lhs = R2 + r2 - dd
            if lhs > 0 and mul(lhs, lhs) == mul(4, mul(R2, r2)):
                tang += 1
                # 接する点：親と子が共有する頂点
                shared = [v for v in K if v in P_]
                tang_pts |= set(shared)
            else:
                ok2b = False
        for i in range(4):
            for j in range(i + 1, 4):
                a, b = center2(kids[i]), center2(kids[j])
                r2 = d2(tuple(2 * v for v in kids[i][0]), a)
                dd = d2(a, b)
                if dd < mul(4, r2):
                    pair_over += 1
                elif dd == mul(4, r2):
                    pair_touch += 1
                else:
                    pair_apart += 1
    print(f" 段 {k}：子の球 {len(parents) * 4}、親に内側から接する {tang}、接する点は親と子が共有する頂点（{len(tang_pts)} 点）"
          f"／兄弟の組 重なる {pair_over}・接する {pair_touch}・離れる {pair_apart}")
# 負の対照：子の正四面体を一歩ずらすと親に接しない
P_ = big_tetra(S0)
K = cells(P_, 1)[0]
Ks = [(v[0] + 1, v[1] + 1, v[2]) for v in K]
Pc, Kc = center2(P_), center2(Ks)
R2 = d2(tuple(2 * v for v in P_[0]), Pc); r2 = d2(tuple(2 * v for v in Ks[0]), Kc); dd = d2(Pc, Kc)
lhs = R2 + r2 - dd
print(f" 負の対照（子を (1,1,0) だけずらす）：内側から接する {lhs > 0 and mul(lhs, lhs) == mul(4, mul(R2, r2))}")
print(" 判定：", "OK（すべての子の球が親の球に内側から接する）" if ok2b else "NG")
