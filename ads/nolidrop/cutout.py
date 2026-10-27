"""Cut Noli poses (white background) into RGBA sprites: flood-fill the near-white background from the border."""
import sys, glob
import numpy as np, cv2
from PIL import Image
for f in sys.argv[1:]:
    a = np.asarray(Image.open(f).convert("RGB")).astype(np.int16)
    bg = ((a.min(axis=2) > 196) & (a.max(axis=2) - a.min(axis=2) < 26)).astype(np.uint8)
    h, w = bg.shape
    ff = bg.copy(); mask = np.zeros((h + 2, w + 2), np.uint8)
    # connected component of background touching the border
    n, lab = cv2.connectedComponents(bg)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    back = np.isin(lab, list(border))
    # white pockets enclosed by the legs (lower part of the figure) are background too; eye whites sit higher up
    ys, xs = np.where(~back)
    y0, y1 = ys.min(), ys.max()
    n2, lab2, st2, cen2 = cv2.connectedComponentsWithStats((bg & ~back).astype(np.uint8))
    for k in range(1, n2):
        if cen2[k][1] > y0 + 0.66 * (y1 - y0) and st2[k, cv2.CC_STAT_AREA] > 3000:
            back |= lab2 == k
    alpha = (~back).astype(np.uint8) * 255
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    # keep largest component (drop specks), soften edge
    n, lab, st, _ = cv2.connectedComponentsWithStats((alpha > 0).astype(np.uint8))
    keep = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
    alpha = np.where(lab == keep, 255, 0).astype(np.uint8)
    alpha = cv2.erode(alpha, np.ones((3, 3), np.uint8))
    alpha = cv2.GaussianBlur(alpha, (5, 5), 0)
    rgba = np.dstack([a.astype(np.uint8), alpha])
    x, y, ww, hh = cv2.boundingRect((alpha > 8).astype(np.uint8))
    out = f.replace("img/", "sprites/").replace("refs/", "sprites/").rsplit(".", 1)[0] + ".png"
    Image.fromarray(rgba[y:y + hh, x:x + ww]).save(out)
    print(out, ww, hh)
