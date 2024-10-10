from stockvip.config.ensure_logged_in import ensure_logged_in
from stockvip.process_stock.ohlcv import get_ohlcv
from stockvip.process_stock.foreign import get_foreign
from stockvip.process_stock.propTrading import get_propTrading
from stockvip.process_stock.supplyAndDemand import get_supply_and_demand
from stockvip.process_stock.dividend import get_dividend
from stockvip.config.config import dict_unit
import pandas as pd
from datetime import datetime,timedelta

class Stock:
    """
    Lớp Stock đại diện cho một mã cổ phiếu và cung cấp phương thức để lấy dữ liệu liên quan đến mã cổ phiếu.

    Attributes:
        ticker (str): Mã cổ phiếu, ví dụ như "HPG".
        unit (str): Đơn vị tính cho giá trị giao dịch, với các lựa chọn sau:
        
            - "tỷ đồng": Đơn vị tỷ đồng.
            - "triệu đồng": Đơn vị triệu đồng.
            - "ngàn đồng": Đơn vị ngàn đồng.
            - "đồng": Đơn vị đồng.
    """

    def __init__(self, ticker: str,unit: str ='tỷ đồng') -> None:
        """
        Khởi tạo đối tượng Stock với mã cổ phiếu và đơn vị cụ thể.

        Args:
            ticker (str): Mã cổ phiếu (ví dụ: "HPG").
            unit (str, optional): Đơn vị tính cho giá trị giao dịch. Các lựa chọn hợp lệ bao gồm:
            
                - "tỷ đồng": Đơn vị tỷ đồng (mặc định).
                - "triệu đồng": Đơn vị triệu đồng.
                - "ngàn đồng": Đơn vị ngàn đồng.
                - "đồng": Đơn vị đồng.
        """
        self.ticker = ticker
        self.unit=unit
    def check_period(self,period):
        """
        Kiểm tra tính hợp lệ của tham số period.

        Phương thức này kiểm tra xem giá trị của `period` có nằm trong danh sách các khoảng thời gian hợp lệ hay không.
        Nếu `period` không hợp lệ, nó sẽ ném ra một ngoại lệ `ValueError`.

        Args:
            period (str): Khoảng thời gian cần kiểm tra. Các giá trị hợp lệ bao gồm:
            
                - "D": Hàng ngày (Daily)
                - "W": Hàng tuần (Weekly)
                - "1M": 1 tháng (1 Month)
                - "3M": 3 tháng (3 Months)
                - "6M": 6 tháng (6 Months)
                - "1Y": 1 năm (1 Year)
                - "3Y": 3 năm (3 Years)

        Raises:
            ValueError: Nếu `period` không nằm trong các giá trị hợp lệ.
        """
        valid_periods = ["D", "W", "1M", "3M", "6M", "1Y", "3Y"]
        if period not in valid_periods:
            raise ValueError(f"Period '{period}' không hợp lệ. Chỉ chấp nhận các giá trị: {', '.join(valid_periods)}")
    def check_rangeTime(self,fromDate,toDate):
        """
        Kiểm tra tính hợp lệ của khoảng thời gian từ `fromDate` đến `toDate`.

        Phương thức này sẽ kiểm tra:
        1. Định dạng của `fromDate` và `toDate` phải là 'YYYY-MM-DD'.
        2. `toDate` phải lớn hơn hoặc bằng `fromDate`.

        Nếu bất kỳ điều kiện nào không được đáp ứng, hàm sẽ ném ra một ngoại lệ `ValueError`.

        Args:
            fromDate (str): Ngày bắt đầu cần kiểm tra, định dạng 'YYYY-MM-DD'.
            toDate (str): Ngày kết thúc cần kiểm tra, định dạng 'YYYY-MM-DD'.

        Raises:
            ValueError: Nếu định dạng ngày không đúng hoặc `toDate` nhỏ hơn `fromDate`.
            Exception: Nếu có lỗi trong quá trình chuyển đổi ngày từ chuỗi sang đối tượng datetime.

        Example:
            >>> check_rangeTime("2023-01-01", "2023-12-31")
            # Không có lỗi

            >>> check_rangeTime("2023-01-01", "2022-12-31")
            ValueError: Giá trị không hợp lệ -> toDate < fromDate. Vui lòng kiểm tra lại

            >>> check_rangeTime("01-01-2023", "31-12-2023")
            ValueError: Lỗi định dạng: fromDate | toDate cần là: "yyyy-mm-dd"
        """
        try:
            fromDate_dt=datetime.strptime(fromDate,'%Y-%m-%d')
            toDate_dt=datetime.strptime(toDate,'%Y-%m-%d')
            if toDate_dt<fromDate_dt:
                raise ValueError("Giá trị không hợp lệ -> toDate < fromDate. Vui lòng kiểm tra lại")
        except Exception as e:
            print(e)
            raise ValueError(f'''Lỗi định dạng: fromDate | toDate cần là: "yyyy-mm-dd"
Dữ liệu input của bạn:
fromDate: {fromDate}
toDate: {toDate}
Hãy kiểm tra lại''')        
    @ensure_logged_in
    def ohlcv(self, fromDate: str=None, toDate: str=None, period: str = "D") -> pd.DataFrame:
        """
        Trả về dữ liệu lịch sử giao dịch của mã cổ phiếu trong khoảng thời gian cụ thể với khoảng thời gian tùy chọn.

        Phương thức này yêu cầu người dùng đã đăng nhập và lấy dữ liệu giao dịch của mã cổ phiếu 
        từ ngày `fromDate` đến ngày `toDate`. Người dùng có thể chọn khoảng thời gian (`period`) cho dữ liệu là ngày, tuần, tháng, hoặc các chu kỳ dài hơn.

        Args:
            fromDate (str): Ngày bắt đầu dưới định dạng 'YYYY-MM-DD'. Nếu không được truyền vào, 
                            giá trị mặc định là ngày 30 ngày trước ngày hiện tại.
            toDate (str): Ngày kết thúc dưới định dạng 'YYYY-MM-DD'. Nếu không được truyền vào,
                        giá trị mặc định là ngày hiện tại.
            period (str): Khoảng thời gian của dữ liệu. Mặc định là "D" (ngày).
                         
                         Các lựa chọn hợp lệ bao gồm:
                         
                         - "D": Hàng ngày (Daily)
                         - "W": Hàng tuần (Weekly)
                         - "1M": Hàng tháng (1 Month)
                         - "3M": 3 tháng (3 Months)
                         - "6M": 6 tháng (6 Months)
                         - "1Y": 1 năm (1 Year)
                         - "3Y": 3 năm (3 Years)

        Returns:
            pd.DataFrame: Dữ liệu giao dịch của mã cổ phiếu, bao gồm các cột như giá mở cửa, giá đóng cửa, khối lượng giao dịch, v.v.

        Raises:
            ValueError: Nếu định dạng ngày không đúng (phải là 'YYYY-MM-DD') hoặc period không hợp lệ.
            Exception: Nếu có lỗi xảy ra khi kết nối hoặc token đăng nhập hết hạn.

        Example:
            >>> import stockvip as sv
            >>> sv.Connect("0123456789", "password123")
            >>> hpg = sv.Stock("HPG")
            >>> df = hpg.ohlcv(fromDate="2024-01-01", toDate="2024-09-30", period="W")
            >>> print(df.head())
        """
        if fromDate is None:
            fromDate=(datetime.today().date()-timedelta(days=30)).strftime("%Y-%m-%d")
        if toDate is None:
            toDate=datetime.today().strftime("%Y-%m-%d")
        # Kiểm tra tính hợp lệ của period.
        self.check_period(period)
        # Kiểm tra tính hợp lệ của khoảng thời gian
        self.check_rangeTime(fromDate,toDate)
        # Lấy dữ liệu giao dịch từ API với ticker và khoảng thời gian cụ thể
        data = get_ohlcv(
            ticker=self.ticker,
            fromDate=fromDate,
            toDate=toDate,
            period=period,
        )
        return data
    @ensure_logged_in
    def foreign(self, fromDate: str=None, toDate: str=None, period: str = "D") -> pd.DataFrame:
        """
        Trả về dữ liệu giao dịch nước ngoài của mã cổ phiếu trong khoảng thời gian cụ thể.

        Phương thức này yêu cầu người dùng đã đăng nhập và lấy dữ liệu giao dịch nước ngoài
        của mã cổ phiếu từ ngày `fromDate` đến ngày `toDate`. Người dùng có thể chọn khoảng thời gian (`period`)
        để dữ liệu là ngày, tuần, tháng, hoặc các chu kỳ dài hơn.

        Args:
            fromDate (str): Ngày bắt đầu dưới định dạng 'YYYY-MM-DD'. Nếu không được truyền vào, 
                            giá trị mặc định là ngày 30 ngày trước ngày hiện tại.
            toDate (str): Ngày kết thúc dưới định dạng 'YYYY-MM-DD'. Nếu không được truyền vào,
                        giá trị mặc định là ngày hiện tại.
            period (str, optional): Khoảng thời gian của dữ liệu. Mặc định là "D" (ngày). Các lựa chọn hợp lệ bao gồm:
            
                - "D": Hàng ngày (Daily)
                - "W": Hàng tuần (Weekly)
                - "1M": Hàng tháng (1 Month)
                - "3M": 3 tháng (3 Months)
                - "6M": 6 tháng (6 Months)
                - "1Y": 1 năm (1 Year)
                - "3Y": 3 năm (3 Years)

        Returns:
            pd.DataFrame: Dữ liệu giao dịch nước ngoài của mã cổ phiếu, bao gồm các cột giá đóng cửa, 
            khối lượng mua/bán, giá trị mua/bán và giá trị giao dịch ròng của nhà đầu tư nước ngoài.

        Raises:
            ValueError: Nếu định dạng ngày không đúng (phải là 'YYYY-MM-DD') hoặc `toDate` nhỏ hơn `fromDate`.
            ValueError: Nếu `period` không nằm trong các giá trị hợp lệ.
            Exception: Nếu có lỗi xảy ra khi kết nối hoặc token đăng nhập hết hạn.

        Example:
            >>> import stockvip as sv
            >>> stock = sv.Stock("HPG")
            >>> stock.foreign(fromDate="2024-01-01", toDate="2024-12-31", period="D")
            # Trả về dữ liệu giao dịch nước ngoài của mã HPG trong khoảng thời gian đã chỉ định.
        """
        if fromDate is None:
            fromDate=(datetime.today().date()-timedelta(days=30)).strftime("%Y-%m-%d")
        if toDate is None:
            toDate=datetime.today().strftime("%Y-%m-%d")
        # Kiểm tra tính hợp lệ của period.
        self.check_period(period)
        # Kiểm tra tính hợp lệ của khoảng thời gian
        self.check_rangeTime(fromDate,toDate)
        divide=self.unit.lower().strip().replace("  ","")
        data = get_foreign(
            ticker=self.ticker,
            fromDate=fromDate,
            toDate=toDate,
            period=period,
            unit=dict_unit[divide]   
        )
        return data
    @ensure_logged_in
    def propTrading(self, fromDate: str=None, toDate: str=None, period: str = "D") -> pd.DataFrame:
        """
        Trả về dữ liệu giá đóng cửa và giá trị tự doanh mua ròng của mã cổ phiếu trong khoảng thời gian cụ thể.

        Phương thức này sẽ trả về dữ liệu giá đóng cửa và giá trị tự doanh mua ròng của mã cổ phiếu từ ngày `fromDate` 
        đến ngày `toDate`. Nếu `fromDate` hoặc `toDate` không được cung cấp, mặc định sẽ lấy dữ liệu từ 30 ngày trước 
        đến ngày hiện tại. Người dùng cũng có thể chọn khoảng thời gian (`period`) để dữ liệu là ngày, tuần, tháng, hoặc 
        các chu kỳ dài hơn.

        Args:
            fromDate (str, optional): Ngày bắt đầu dưới định dạng 'YYYY-MM-DD'. Mặc định là 30 ngày trước ngày hiện tại nếu không được cung cấp.
            toDate (str, optional): Ngày kết thúc dưới định dạng 'YYYY-MM-DD'. Mặc định là ngày hiện tại nếu không được cung cấp.
            period (str, optional): Khoảng thời gian của dữ liệu. Mặc định là "D" (ngày). Các lựa chọn hợp lệ bao gồm:
            
                - "D": Hàng ngày (Daily)
                - "W": Hàng tuần (Weekly)
                - "1M": Hàng tháng (1 Month)
                - "3M": 3 tháng (3 Months)
                - "6M": 6 tháng (6 Months)
                - "1Y": 1 năm (1 Year)
                - "3Y": 3 năm (3 Years)

        Returns:
            pd.DataFrame: Dữ liệu giá đóng cửa và giá trị tự doanh mua ròng của mã cổ phiếu, bao gồm các cột như giá đóng cửa, 
            giá trị mua ròng của tự doanh, và các thông tin liên quan khác.

        Raises:
            ValueError: Nếu định dạng ngày không đúng (phải là 'YYYY-MM-DD') hoặc `toDate` nhỏ hơn `fromDate`.
            ValueError: Nếu `period` không nằm trong các giá trị hợp lệ.
            Exception: Nếu có lỗi xảy ra khi kết nối API hoặc token hết hạn.

        Example:
            >>> import stockvip as sv
            >>> stock = sv.Stock("HPG")
            >>> stock.propTrading(fromDate="2023-01-01", toDate="2023-12-31", period="D")
            # Trả về dữ liệu giá đóng cửa và giá trị tự doanh mua ròng của mã HPG trong khoảng thời gian đã chỉ định.
        """        
        
        if fromDate is None:
            fromDate=(datetime.today().date()-timedelta(days=30)).strftime("%Y-%m-%d")
        if toDate is None:
            toDate=datetime.today().strftime("%Y-%m-%d")
        # Kiểm tra tính hợp lệ của period.
        self.check_period(period)
        # Kiểm tra tính hợp lệ của khoảng thời gian
        self.check_rangeTime(fromDate,toDate)
        divide=self.unit.lower().strip().replace("  ","")
        data = get_propTrading(
            ticker=self.ticker,
            fromDate=fromDate,
            toDate=toDate,
            period=period,
            unit=dict_unit[divide]   
        )
        return data
    @ensure_logged_in
    def supply_demand(self, fromDate: str=None, toDate: str=None, period: str = "D") -> pd.DataFrame:
        """
        Trả về dữ liệu cung và cầu của mã cổ phiếu trong khoảng thời gian cụ thể.

        Phương thức này sẽ trả về dữ liệu bao gồm giá đóng cửa, số lệnh đặt mua và bán, 
        khối lượng dư mua và dư bán của mã cổ phiếu từ ngày `fromDate` đến ngày `toDate`. 
        Nếu `fromDate` hoặc `toDate` không được cung cấp, mặc định sẽ lấy dữ liệu từ 30 ngày trước 
        đến ngày hiện tại. Người dùng cũng có thể chọn khoảng thời gian (`period`) để dữ liệu 
        được hiển thị theo ngày, tuần, tháng, hoặc các chu kỳ dài hơn.

        Args:
            fromDate (str, optional): Ngày bắt đầu dưới định dạng 'YYYY-MM-DD'. Mặc định là 30 ngày trước ngày hiện tại nếu không được cung cấp.
            toDate (str, optional): Ngày kết thúc dưới định dạng 'YYYY-MM-DD'. Mặc định là ngày hiện tại nếu không được cung cấp.
            period (str, optional): Khoảng thời gian của dữ liệu. Mặc định là "D" (ngày). Các lựa chọn hợp lệ bao gồm:
            
                - "D": Hàng ngày (Daily)
                - "W": Hàng tuần (Weekly)
                - "1M": Hàng tháng (1 Month)
                - "3M": 3 tháng (3 Months)
                - "6M": 6 tháng (6 Months)
                - "1Y": 1 năm (1 Year)
                - "3Y": 3 năm (3 Years)

        Returns:
            pd.DataFrame: Dữ liệu cung và cầu của mã cổ phiếu, bao gồm các cột như giá đóng cửa, số lệnh đặt mua, 
            số lệnh đặt bán, khối lượng dư mua và khối lượng dư bán.

        Raises:
            ValueError: Nếu định dạng ngày không đúng (phải là 'YYYY-MM-DD') hoặc `toDate` nhỏ hơn `fromDate`.
            ValueError: Nếu `period` không nằm trong các giá trị hợp lệ.
            Exception: Nếu có lỗi xảy ra khi kết nối API hoặc token hết hạn.

        Example:
            >>> import stockvip as sv
            >>> stock = Stock("HPG")
            >>> stock.supply_demand(fromDate="2024-01-01", toDate="2024-12-31", period="D")
            # Trả về dữ liệu cung và cầu của mã HPG trong khoảng thời gian đã chỉ định.
        """
        if fromDate is None:
            fromDate=(datetime.today().date()-timedelta(days=30)).strftime("%Y-%m-%d")
        if toDate is None:
            toDate=datetime.today().strftime("%Y-%m-%d")
        # Kiểm tra tính hợp lệ của period.
        self.check_period(period)
        # Kiểm tra tính hợp lệ của khoảng thời gian
        self.check_rangeTime(fromDate,toDate)

        data = get_supply_and_demand(
            ticker=self.ticker,
            fromDate=fromDate,
            toDate=toDate,
            period=period,
        )
        return data
    def dividend(self, fromDate: str=None, toDate: str=None) -> pd.DataFrame:
        """
        Lấy dữ liệu cổ tức của cổ phiếu (dividend) của mã cổ phiếu trong một khoảng thời gian nhất định.

        Phương thức này yêu cầu lấy dữ liệu về cổ tức của mã cổ phiếu từ ngày `fromDate` đến `toDate`. 
        Nếu không có dữ liệu, sẽ tự động trả về lỗi. Thời gian mặc định nếu không được cung cấp sẽ là 30 ngày trước tính từ hôm nay.

        Args:
            fromDate (str, optional): Ngày bắt đầu dưới định dạng 'YYYY-MM-DD'. Nếu không được cung cấp, mặc định sẽ là 30 ngày trước ngày hiện tại.
            toDate (str, optional): Ngày kết thúc dưới định dạng 'YYYY-MM-DD'. Nếu không được cung cấp, mặc định sẽ là ngày hiện tại.

        Returns:
            pd.DataFrame: Dữ liệu cổ tức dưới dạng DataFrame, bao gồm các cột thông tin về mã cổ phiếu, ngày giao dịch không hưởng quyền, 
            ngày đăng ký cuối cùng, ngày thực hiện và nội dung sự kiện. Các giá trị NaN sẽ được thay bằng dấu "-".

        Raises:
            ValueError: Nếu có lỗi xảy ra trong quá trình lấy dữ liệu, chẳng hạn như không tìm thấy dữ liệu hoặc thông tin không hợp lệ.
        
        Example:
            >>> stock = Stock("HPG")
            >>> df = stock.dividend(fromDate="2023-01-01", toDate="2023-09-30")
            >>> print(df.head())
        """
        
        if fromDate is None:
            fromDate=(datetime.today().date()-timedelta(days=30)).strftime("%Y-%m-%d")
        if toDate is None:
            toDate=datetime.today().strftime("%Y-%m-%d")
        # Kiểm tra tính hợp lệ của period.

        # Kiểm tra tính hợp lệ của khoảng thời gian
        self.check_rangeTime(fromDate,toDate)
        data = get_dividend(
            ticker=self.ticker,
            fromDate=fromDate,
            toDate=toDate,
        )
        return data