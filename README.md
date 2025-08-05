# GAME CỜ CARO - HƯỚNG DẪN SỬ DỤNG

## 🎮 Cách chạy game:
- Double-click vào file `AdvancedCaroGame.exe` 

## 🚀 Tính năng mới của phiên bản nâng cao:

### 🏠 **Menu chính**:
- **👥 Chơi với người**: Chế độ 2 người chơi cổ điển
- **🤖 Chơi với máy**: Chơi với AI thông minh
- **⚙️ Cài đặt**: Tuỳ chỉnh game chi tiết
- **ℹ️ Hướng dẫn**: Hướng dẫn sử dụng đầy đủ
- **❌ Thoát**: Thoát game

### ⚙️ **Cài đặt linh hoạt**:
- **Kích thước bàn cờ**: 3x3, 4x4, 5x5, 6x6, 7x7, 8x8, 9x9, 10x10
- **Số quân cần thắng**: 3, 4, 5, 6 quân (tự động điều chỉnh theo kích thước)
- **Độ khó AI**: Dễ, Trung bình, Khó
- **Giao diện**: Sáng, Tối

### 🤖 **AI thông minh 3 cấp độ**:
- **Dễ**: Đi ngẫu nhiên - Phù hợp cho người mới
- **Trung bình**: Có chiến thuật cơ bản (chặn, tấn công) - Cân bằng
- **Khó**: Sử dụng thuật toán Minimax - Thử thách cao

### 🎮 **Tính năng game nâng cao**:
- **💡 Gợi ý**: Đề xuất nước đi tốt nhất (chỉ khi chơi với máy)
- **↶ Hoàn tác**: Hủy nước đi vừa rồi (1 nước với người, 2 nước với máy)
- **🔄 Chơi lại**: Reset ván hiện tại, giữ nguyên điểm số
- **🆕 Game mới**: Reset toàn bộ including điểm số
- **🏠 Menu**: Quay về menu chính bất cứ lúc nào

### 💾 **Lưu trữ thông minh**:
- **Cài đặt**: Tự động lưu và khôi phục cài đặt game
- **Điểm số**: Theo dõi điểm qua các ván đấu
- **Theme**: Ghi nhớ giao diện đã chọn

## 🎯 Cách chơi chi tiết:

### � **Quy tắc cơ bản**:
1. **Mục tiêu**: Đặt số quân quy định thành một hàng liên tiếp (ngang, dọc, chéo)
2. **Lượt chơi**: Người chơi X luôn đi trước
3. **Đặt quân**: Click vào ô trống để đặt quân
4. **Thắng**: Người đầu tiên đạt số quân liên tiếp sẽ thắng

### 🎮 **Điều khiển game**:
- **Mouse**: Click vào ô để đặt quân

### ⌨️ **Phím tắt nâng cao**:
- **R**: Chơi lại ván hiện tại
- **N**: Bắt đầu game mới  
- **H**: Hiển thị gợi ý (chỉ khi chơi với máy)
- **U**: Hoàn tác nước đi
- **Q**: Thoát game
- **Esc**: Quay về menu chính

### 🤖 **Hướng dẫn chơi với AI**:
1. **Chọn độ khó** phù hợp với trình độ
2. **Sử dụng gợi ý** khi bí nước
3. **Hoàn tác** để thử chiến thuật khác
4. **Thử thách bản thân** với độ khó cao hơn

### ⚙️ **Tùy chỉnh game**:
1. **Bàn cờ nhỏ (3x3, 4x4)**: Nhanh, phù hợp casual
2. **Bàn cờ trung bình (5x5, 6x6)**: Cân bằng, khuyến nghị
3. **Bàn cờ lớn (7x7+)**: Phức tạp, thử thách cao

## 📁 Cấu trúc file:

```
d:\caro\
├─ AdvancedCaroGame.exe    # Game .exe nâng cao
├── caro_game.py               # Source code Python 
├── index.html                 # Phiên bản web
├── script.js                  # JavaScript cho web
├── style.css                  # CSS cho web
├── README.md                  # File hướng dẫn này
└── caro_settings.json        # File cài đặt (tự tạo)
```


## 🎊 Tính năng đặc biệt:

- **🧠 AI thông minh**: Sử dụng thuật toán Minimax với Alpha-Beta pruning
- **🎨 Giao diện đẹp**: Theme sáng/tối, responsive design
- **💾 Lưu trữ**: Auto-save settings và scores
- **🔧 Tùy biến cao**: Từ 3x3 đến 10x10, 3-6 quân thắng

Chúc bạn chơi game vui vẻ! 🎮✨

