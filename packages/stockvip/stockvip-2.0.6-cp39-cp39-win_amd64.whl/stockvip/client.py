from stockvip.process_client.login import Client 

def Login(phone_number: str, password: str):
    """
    Xác thực người dùng bằng số điện thoại và mật khẩu.

    Hàm này thực hiện xác thực người dùng với hệ thống bằng cách sử dụng số điện thoại và mật khẩu.
    Nếu xác thực thành công, hàm sẽ lưu trữ token để sử dụng cho các yêu cầu lấy dữ liệu tiếp theo.

    Args:
        phone_number (str): Số điện thoại người dùng dùng để đăng nhập. Phải là chuỗi số hợp lệ (ví dụ: '0123456789').
        password (str): Mật khẩu của người dùng. Phải là chuỗi ký tự hợp lệ, phân biệt chữ hoa và chữ thường.

    Returns:
        bool: Trả về True nếu đăng nhập thành công, False nếu thất bại.

    Raises:
        ValueError: Nếu số điện thoại hoặc mật khẩu không hợp lệ hoặc không đáp ứng được yêu cầu xác thực.

    Example:
        >>> import stockvip as sv
        >>> sv.Connect("0123456789", "password123")
        True
    """
    client = Client()
    client.login(phone_number=phone_number, password=password)
