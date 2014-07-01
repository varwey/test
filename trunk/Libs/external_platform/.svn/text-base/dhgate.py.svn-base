# -*- coding: utf-8 -*-
import traceback
import requests
from kratos.utils.logger import kr_logger as logger

__author__ = 'Zou'

API_URL_PREFIX = 'http://www.dhgate.com/'


class DHgate():
    u"""外部平台对接 DHgate工具类"""
    def __init__(self, platform_flag):
        self.platform_flag = platform_flag

    def get_product_info(self, product_id):
        u"""获得商品信息

        @param product_id: 商品id
        """
        url = '%(prefix)s/product'

        params = {
            "product_id": product_id
        }

        try:
            res = requests.post(url, params)

            return res
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc(e))

    def send_product_transalte_price(self, product_id, price):
        u"""发送商品翻译价格信息

        @param product_id: 商品id
        @param price: 一个商品的翻译总价格
        @return
        """
        url = '%(prefix)s/' % {"prefix": API_URL_PREFIX}

        params = {
            "product_id": product_id,
            "price": price
        }
        try:
            res = requests.post(url, params)
            # 判断返回结果
            return res
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc(e))