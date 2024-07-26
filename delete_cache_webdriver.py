import psutil

def close_all_edge_drivers():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'msedgedriver.exe':
            proc.kill()

# Gọi hàm này trước khi khởi tạo driver mới hoặc sau khi kết thúc chương trình
close_all_edge_drivers()