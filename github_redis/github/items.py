# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import Join


class GithubItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def parse_field(text):
    return str(text).strip()

class EmailItem(scrapy.Item):

    # 邮箱
    email = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    url = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    # 关注他的人数量
    follower = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    # 他关注的人数量
    following = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )

    # 项目Star数量
    star = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    # 所属机构
    mechanism = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    # 推特链接
    twitter = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )

    # 位置
    location = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )

    # 总关注数量star
    total_star = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )

    # 用户
    user = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )

    # 简介
    summery = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )

    # 项目成员简介
    highlights = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )

    # 组织
    organizations = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )

    # 项目编程语言
    programmingLanguage = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )

