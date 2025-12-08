# Giam Dung Luong Anh bang K-Means Color Quantization

## Muc tieu du an
Du an giam kich thuoc tep anh bang cach giam so luong mau sac su dung. Phuong phap K-Means clustering tren khong gian mau RGB duoc ap dung de gom cac pixel vao k cum mau va thay the moi pixel bang centroid cua cum do, giup giam dung luong anh ma van giu duoc chat luong thi giac.

## Quy trinh thuc hien
1. Doc anh – Tai anh input (vi du `input.png`) bang Pillow va chuyen thanh mang NumPy dang `(H, W, 3)`.  
2. Chuan hoa du lieu – Chuyen anh thanh dang 2D `(num_pixels, 3)` de thuan tien cho K-Means.  
3. Ap dung K-Means – Dung `sklearn.cluster.KMeans(k)` de phan cum mau.  
4. Tai tao anh – Thay moi pixel bang mau centroid cua cum tuong ung.  
5. Luu anh dau ra – Xuat file moi (vi du `output_quantized.png`).

## Thuat toan toi uu K theo dung luong anh muc tieu
Ngoai viec chon K thu cong, du an ho tro tu dong tim so cum K toi uu sao cho kich thuoc anh sau nen gan nhat voi dung luong muc tieu. Dung luong anh giam dan khi K nho va tang khi K lon, vi vay co the dung tim kiem nhi phan tren K.

### Thuat toan co ban
- Input: anh goc, `target_size_kb`, gioi han K toi thieu va toi da (vd 2 <= K <= 64).  
- Tim kiem nhi phan: o moi buoc, chon `mid = (low + high) // 2`, nen anh voi K=mid, do dung luong file tam thoi, so sanh voi `target_size_kb` va dieu chinh khoang tim kiem.  
- Tra ve gia tri K co sai khac dung luong nho nhat.

```python
def search_optimal_k(image_array, target_size_kb, k_min=2, k_max=64):
    low, high = k_min, k_max
    best_k = None
    best_diff = float("inf")
    while low <= high:
        mid = (low + high) // 2
        img_mid = quantize_image_kmeans(image_array, mid)
        save_image(img_mid, "temp.png")
        size_mid = os.path.getsize("temp.png") / 1024
        diff = abs(size_mid - target_size_kb)
        if diff < best_diff:
            best_diff = diff
            best_k = mid
        if size_mid > target_size_kb:
            high = mid - 1
        else:
            low = mid + 1
    return best_k
```

### Uu diem
- Phu hop voi moi quan he don dieu giua K va dung luong file.  
- Toc do nhanh (do phuc tap log2(k_range)).  
- Giup nguoi dung dat duoc dung luong mong muon ma khong phai thu thu cong.

## Vi du minh hoa
Anh dau vao duoc nen bang K-Means cho ra anh dau ra co kich thuoc nho hon nhieu nhung van giu cac dac trung chinh.

## Huong dan cai dat va su dung
### Cai dat thu vien
```
pip install numpy matplotlib scikit-learn pillow
```
### Chay script nen anh co ban
```
python main.py --input input.png --k 16 --output output_quantized.png
```
### Chay che do tim K toi uu theo dung luong
```
python main.py --input input.png --target_size 150 --output compressed.png
```

## Cai tien de xuat
- Thu nghiem khong gian mau Lab de phan anh tot hon cam nhan thi giac.  
- Su dung MiniBatchKMeans cho anh lon de giam thoi gian tinh toan.  
- Danh gia chat luong nen bang cac chi so PSNR/SSIM de lua chon K.
