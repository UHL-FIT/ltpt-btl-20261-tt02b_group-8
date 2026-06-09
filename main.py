# Import lớp MainView từ file views/main_view.py
from views.main_view import MainView
from models.main_model import MainModel
from controllers.main_controller import MainController

# Kiểm tra xem file này có phải file đang được chạy trực tiếp không
if __name__ == "__main__":
    # Tạo đối tượng giao diện chính
    app = MainView()

    # Chạy vòng lặp giao diện Tkinter
    app.mainloop()