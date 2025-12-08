
import argparse
import os
import tempfile
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


# ==========================
# 1. ĐỌC ẢNH
# ==========================

def read_image_as_array(path: str) -> np.ndarray:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File không tồn tại: {path}")

    try:
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        return np.array(img)
    except Exception as e:
        raise ValueError(f"Không thể đọc ảnh: {e}")


# ==========================
# 2. K-MEANS QUANTIZATION
# ==========================

def quantize_image_kmeans(image_array: np.ndarray, k: int) -> np.ndarray:
    h, w, c = image_array.shape
    pixels = image_array.reshape(-1, 3)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
    kmeans.fit(pixels)

    palette = kmeans.cluster_centers_.astype(np.uint8)
    labels = kmeans.labels_

    quantized_pixels = palette[labels]
    return quantized_pixels.reshape(h, w, c)


# ==========================
# 3. LƯU PNG-8 (INDEXED)
# ==========================

def save_indexed_png_from_array(image_array: np.ndarray, path: str, k: int) -> None:
    img_pil = Image.fromarray(image_array.astype(np.uint8))
    img_pil = img_pil.convert("P", palette=Image.Palette.ADAPTIVE, colors=k)
    img_pil.save(path, optimize=True)


def get_file_size_kb(path: str) -> float:
    return os.path.getsize(path) / 1024.0


# ==========================
# 4. TÌM K TỐI ƯU (BINARY SEARCH)
# ==========================

def find_optimal_k(image_array, target_kb, min_k=2, max_k=256, max_iter=20):
    best_k = min_k
    best_diff = float("inf")
    best_size = float("inf")

    lo, hi = min_k, max_k

    with tempfile.TemporaryDirectory() as tmpdir:
        iteration = 0

        while hi - lo > 2 and iteration < max_iter:
            iteration += 1
            mid_k = (lo + hi) // 2

            quantized = quantize_image_kmeans(image_array, mid_k)
            temp_path = os.path.join(tmpdir, f"temp_{mid_k}.png")
            save_indexed_png_from_array(quantized, temp_path, mid_k)
            size_kb = get_file_size_kb(temp_path)
            diff = abs(size_kb - target_kb)

            if diff < best_diff:
                best_diff = diff
                best_k = mid_k
                best_size = size_kb

            if size_kb > target_kb:
                hi = mid_k - 1
            else:
                lo = mid_k + 1

        for k in range(lo, hi + 1):
            quantized = quantize_image_kmeans(image_array, k)
            temp_path = os.path.join(tmpdir, f"temp_{k}.png")
            save_indexed_png_from_array(quantized, temp_path, k)
            size_kb = get_file_size_kb(temp_path)
            diff = abs(size_kb - target_kb)

            if diff < best_diff:
                best_diff = diff
                best_k = k
                best_size = size_kb

    return best_k, best_size


# ==========================
# 5. MAIN FUNCTION
# ==========================

def main():
    parser = argparse.ArgumentParser(description="Nén ảnh bằng Color Quantization K-means (không visualization).")
    parser.add_argument("--input", required=True, help="Đường dẫn ảnh đầu vào")
    parser.add_argument("--output", required=True, help="Đường dẫn ảnh đầu ra")
    parser.add_argument("--target_kb", type=float, required=True, help="Dung lượng mục tiêu (KB)")

    args = parser.parse_args()

    print(f"📂 Đang đọc ảnh: {args.input}")
    img_array = read_image_as_array(args.input)

    # Tính dung lượng ảnh gốc
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        Image.fromarray(img_array).save(tmp.name)
        original_size_kb = get_file_size_kb(tmp.name)
    os.unlink(tmp.name)

    print(f"📊 Dung lượng ảnh gốc: {original_size_kb:.2f} KB")
    print(f"🎯 Target: {args.target_kb:.2f} KB")

    # Tìm K tối ưu
    optimal_k, estimated_size = find_optimal_k(img_array, args.target_kb)
    print(f"✅ K tối ưu tìm được: {optimal_k} (ước lượng size {estimated_size:.2f} KB)")

    # Quantize ảnh với K tối ưu
    final_img = quantize_image_kmeans(img_array, optimal_k)

    # Lưu PNG-8 output
    save_indexed_png_from_array(final_img, args.output, optimal_k)
    final_size = get_file_size_kb(args.output)

    print("📦 Xuất ảnh thành công!")
    print(f"📁 File đầu ra: {args.output}")
    print(f"📉 Dung lượng sau nén: {final_size:.2f} KB")
    print(f"⚖️ Tỷ lệ nén: {(1 - final_size / original_size_kb) * 100:.1f}%")



if __name__ == "__main__":
    main()

