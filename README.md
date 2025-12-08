# Dự án giảm dung lượng ảnh bằng K-Means  
## Mục tiêu  
Dự án nhằm giảm kích thước tệp ảnh bằng cách giảm số lượng màu sắc sử dụng trong ảnh. Bằng cách áp dụng thuật toán phân cụm K-Means lên không gian màu RGB, chúng ta gom các pixel vào k cụm màu và thay thế mỗi pixel bằng centroid của cụm đó. Điều này giúp ảnh nhẹ hơn mà vẫn giữ được chi tiết chính.  
## Phương pháp  
- **Đọc ảnh**: sử dụng thư viện như Pillow/Matplotlib để tải ảnh (`input.png`) và chuyển về mảng numpy kích thước (H, W, 3).  
- **Chuẩn hóa dữ liệu**: chuyển mảng thành dạng 2D `(num_pixels, 3)` để phù hợp với thuật toán K-Means.  
- **Áp dụng K-Means**: sử dụng `sklearn.cluster.KMeans` với số cụm `k` (ví dụ 16) để học centroid màu.  
- **Tái tạo ảnh**: gán mỗi pixel về màu centroid tương ứng, sau đó reshape về kích thước gốc và lưu ảnh (`output_quantized.png`).  
- **Đánh giá**: so sánh kích thước file và chất lượng thị giác giữa ảnh gốc và ảnh sau khi nén.  
## Hướng dẫn chạy  
1. Cài đặt các thư viện cần thiết:  
   ```  
   pip install numpy matplotlib scikit-learn pillow  
   ```  
2. Chạy script `main.py` với tham số số cụm `k` và đường dẫn ảnh:  
   ```  
   python main.py --input input.png --k 16 --output output_quantized.png  
   ```  
3. Hoặc mở notebook `visual.ipynb` để xem từng bước trực quan.  
## Kết quả  
Dưới đây là ảnh gốc và ảnh sau khi nén bằng K-Means với k cụm màu:  
![Ảnh gốc](input.png)  
![Ảnh sau nén](output_quantized.png)  
Ảnh sau khi nén có kích thước nhỏ hơn đáng kể so với ảnh gốc, trong khi chất lượng thị giác vẫn được giữ ở mức chấp nhận được. Việc thay đổi giá trị `k` sẽ ảnh hưởng tới mức nén và chất lượng: `k` nhỏ hơn cho ảnh nhẹ hơn nhưng có thể mất chi tiết, `k` lớn hơn giữ chi tiết tốt hơn nhưng ảnh lớn hơn.  
## Cải tiến  
- Thử các giá trị `k` khác nhau và tính toán chỉ số PSNR/SSIM để đánh giá chất lượng.  
- Áp dụng K-Means trên không gian màu khác như Lab để phù hợp với nhận thức của mắt người.  
- Tối ưu tốc độ bằng cách sử dụng MiniBatchKMeans cho ảnh lớn.
