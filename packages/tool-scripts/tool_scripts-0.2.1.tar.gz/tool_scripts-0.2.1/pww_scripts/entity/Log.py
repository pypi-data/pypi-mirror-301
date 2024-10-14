import logging
import datetime


# 定义颜色常量
class LogColors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


# # 自定义日志格式化器
# class ColoredFormatter(logging.Formatter):
#     def format(self, record):
#         if record.levelno == logging.DEBUG:
#             record.msg = f"{LogColors.CYAN}{record.msg}{LogColors.RESET}"
#         elif record.levelno == logging.INFO:
#             record.msg = f"{LogColors.GREEN}{record.msg}{LogColors.RESET}"
#         elif record.levelno == logging.WARNING:
#             record.msg = f"{LogColors.YELLOW}{record.msg}{LogColors.RESET}"
#         elif record.levelno == logging.ERROR:
#             record.msg = f"{LogColors.RED}{record.msg}{LogColors.RESET}"
#         elif record.levelno == logging.CRITICAL:
#             record.msg = f"{LogColors.MAGENTA}{record.msg}{LogColors.RESET}"
#         return super().format(record)


# 设置logger
log_file_path = f'logs\\{datetime.date.today()}.log'
logging.basicConfig(filename=log_file_path, encoding='utf-8')
log = logging.getLogger("MyLogger")
log.setLevel(logging.INFO)

# 设置自定义格式化器


# # 创建文件处理器
# file_handler = logging.FileHandler(log_file_path)
# file_handler.setLevel(logging.DEBUG)
# file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s: [%(lineno)d] - %(message)s')
# file_handler.setFormatter(file_formatter)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s: [%(lineno)d] - %(message)s')
console_handler.setFormatter(console_formatter)

# 添加处理器到logger
log.addHandler(console_handler)

# # 测试日志输出
# log.debug("This is a debug message.")
# log.info("This is an info message.")
# log.warning("This is a warning message.")
# log.error("This is an error message.")
# log.critical("This is a critical message.")
