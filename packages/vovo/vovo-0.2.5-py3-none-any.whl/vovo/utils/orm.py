import threading
import time
from functools import lru_cache
from typing import Type, List

from sqlalchemy import inspect

from vovo.core.decorators import singleton


@lru_cache(maxsize=256)  # 设置缓存的最大大小（256个模型）
def get_primary_keys(model: Type) -> List[str]:

    model_inspector = inspect(model)  # 直接使用 SQLAlchemy 的 inspect
    primary_keys = [key.name for key in model_inspector.mapper.primary_key]  # 获取所有主键的列名
    return primary_keys


@singleton
class IDGen:
    def __init__(self, datacenter_id=0, machine_id=0, epoch=1704067200000):
        """
        IDGen 构造函数，支持 datacenter_id 和 machine_id 缺省
        :param datacenter_id: 数据中心ID（默认值为0）
        :param machine_id: 机器ID（默认值为0）
        :param epoch: 自定义纪元时间（默认是 Twitter 起始时间）
        """
        # 校验参数合法性
        if datacenter_id > 31 or datacenter_id < 0:
            raise ValueError("datacenter_id must be between 0 and 31")
        if machine_id > 31 or machine_id < 0:
            raise ValueError("machine_id must be between 0 and 31")

        self.datacenter_id = datacenter_id
        self.machine_id = machine_id
        self.epoch = epoch  # 起始时间戳（自定义纪元）
        self.sequence = 0  # 序列号
        self.last_timestamp = -1  # 记录上次生成ID时的时间戳

        # 位数定义
        self.datacenter_id_bits = 5
        self.machine_id_bits = 5
        self.sequence_bits = 12

        # 最大值定义
        self.max_sequence = -1 ^ (-1 << self.sequence_bits)  # 4095

        # 位移定义
        self.machine_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.machine_id_bits
        self.timestamp_shift = self.sequence_bits + self.machine_id_bits + self.datacenter_id_bits

        # 锁，用于确保线程安全
        self.lock = threading.Lock()

    @staticmethod
    def _current_timestamp():
        """获取当前时间戳，单位毫秒"""
        return int(time.time() * 1000)

    def _wait_for_next_millisecond(self, last_timestamp):
        """等待直到下一毫秒"""
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp

    def generate_id(self):
        """生成唯一ID"""
        with self.lock:
            timestamp = self._current_timestamp()

            # 如果当前时间小于上一次生成ID的时间，系统时钟回拨了
            if timestamp < self.last_timestamp:
                raise Exception("Clock moved backwards. Refusing to generate id")

            # 同一毫秒内，递增序列号
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.max_sequence
                # 如果序列号溢出，等待下一毫秒
                if self.sequence == 0:
                    timestamp = self._wait_for_next_millisecond(self.last_timestamp)
            else:
                # 如果时间戳变化了，序列号重置为0
                self.sequence = 0

            # 更新最后生成ID的时间戳
            self.last_timestamp = timestamp

            # 生成ID
            unique_id = (
                    (timestamp - self.epoch) << self.timestamp_shift
                    | (self.datacenter_id << self.datacenter_id_shift)
                    | (self.machine_id << self.machine_id_shift)
                    | self.sequence
            )

            return unique_id
