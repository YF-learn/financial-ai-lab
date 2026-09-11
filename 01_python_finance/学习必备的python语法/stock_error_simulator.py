"""
股票项目错误处理模拟器
模拟金融项目中常见的 4 种错误场景：
1. 股票代码不存在
2. API 连接失败
3. 数据为空
4. 日期格式错误

所有错误不直接崩溃，而是以 "ERROR: ..." 形式返回
"""

from datetime import datetime
import random


# ==================== 自定义异常类 ====================

class StockError(Exception):
    """股票相关错误的基类"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"ERROR: {self.message}"


class InvalidStockCodeError(StockError):
    """股票代码不存在"""
    pass


class APIConnectionError(StockError):
    """API 连接失败"""
    pass


class EmptyDataError(StockError):
    """数据为空"""
    pass


class DateFormatError(StockError):
    """日期格式错误"""
    pass


# ==================== 模拟数据 ====================

VALID_STOCK_CODES = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'META']


# ==================== 错误处理函数 ====================

def get_stock_price(stock_code: str) -> str:
    """
    获取股票价格
    :param stock_code: 股票代码，如 'AAPL'
    :return: 价格或错误信息
    """
    try:
        # 模拟 10% 概率 API 失败
        if random.random() < 0.1:
            raise APIConnectionError("API connection failed. Please try again later.")

        # 验证股票代码
        if stock_code not in VALID_STOCK_CODES:
            raise InvalidStockCodeError(f"Invalid stock code: '{stock_code}'")

        # 模拟返回价格
        prices = {
            'AAPL': 175.50,
            'GOOGL': 140.25,
            'MSFT': 380.80,
            'AMZN': 178.90,
            'TSLA': 245.30,
            'NVDA': 495.60,
            'META': 510.75
        }
        return f"SUCCESS: Stock {stock_code} price is ${prices[stock_code]:.2f}"

    except StockError as e:
        return str(e)


def fetch_stock_data(stock_code: str, start_date: str, end_date: str) -> str:
    """
    获取股票历史数据
    :param stock_code: 股票代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 数据或错误信息
    """
    try:
        # 验证日期格式
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise DateFormatError(
                f"Invalid date format: '{start_date}' or '{end_date}'. Expected format: YYYY-MM-DD"
            )

        # 验证日期逻辑
        if start > end:
            raise DateFormatError(f"Start date {start_date} is after end date {end_date}")

        # 验证股票代码
        if stock_code not in VALID_STOCK_CODES:
            raise InvalidStockCodeError(f"Invalid stock code: '{stock_code}'")

        # 模拟 15% 概率数据为空（节假日等）
        if random.random() < 0.15:
            raise EmptyDataError(f"No data available for {stock_code} between {start_date} and {end_date}")

        # 模拟返回数据
        days = (end - start).days
        return f"SUCCESS: Fetched {days} days of data for {stock_code}"

    except StockError as e:
        return str(e)


def validate_date(date_str: str) -> str:
    """
    验证日期格式
    :param date_str: 日期字符串
    :return: 验证结果或错误信息
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return f"SUCCESS: Date '{date_str}' is valid"
    except ValueError:
        return str(DateFormatError(f"Invalid date format: '{date_str}'. Expected: YYYY-MM-DD"))


# ==================== 测试演示 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("股票项目错误处理模拟器")
    print("=" * 60)

    # 测试 1：股票代码不存在
    print("\n【测试1】股票代码不存在")
    print(get_stock_price('INVALID'))
    print(get_stock_price('AAPL'))  # 正常的

    # 测试 2：API 连接失败（可能触发）
    print("\n【测试2】API 连接")
    for i in range(5):
        print(f"  Attempt {i+1}: {get_stock_price('GOOGL')}")

    # 测试 3：数据为空（可能触发）
    print("\n【测试3】数据为空")
    for i in range(5):
        result = fetch_stock_data('TSLA', '2024-01-01', '2024-01-10')
        print(f"  Attempt {i+1}: {result}")

    # 测试 4：日期格式错误
    print("\n【测试4】日期格式错误")
    print(fetch_stock_data('NVDA', '2024/01/01', '2024-01-10'))  # 错误格式
    print(fetch_stock_data('NVDA', '2024-01-01', '01-10-2024'))  # 错误格式
    print(fetch_stock_data('NVDA', '2024-13-01', '2024-01-10'))  # 无效月份
    print(validate_date('2024-01-01'))  # 正确格式
    print(validate_date('01-01-2024'))  # 错误格式

    # 测试 5：边界情况
    print("\n【测试5】边界情况")
    print(fetch_stock_data('META', '2024-12-31', '2024-01-01'))  # 开始日期在结束日期之后
    print(get_stock_price(''))  # 空字符串
    print(fetch_stock_data('', '2024-01-01', '2024-01-10'))  # 空代码

    print("\n" + "=" * 60)
    print("测试完成！所有错误都已被捕获并以 'ERROR: ...' 形式返回")
    print("程序没有崩溃 ✓")
    print("=" * 60)
