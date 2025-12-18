#!/usr/bin/env python3
"""
ABP NSFW规则转换为Surge规则列表脚本 - 从URL获取并直接输出
"""

import re
import sys
import urllib.request
import gzip
import io
from datetime import datetime, timezone

def convert_abp_to_surge_from_url(url):
    """
    从URL下载ABP格式的NSFW规则并转换为Surge规则列表格式，直接输出到标准输出

    Args:
        url: ABP规则文件URL
    """

    domains = set()  # 使用set去重

    print("开始从URL下载ABP规则文件...", file=sys.stderr)

    try:
        # 下载文件
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; SurgeRuleConverter/1.0)'
        })

        with urllib.request.urlopen(req) as response:
            # 检查是否为gzip压缩
            if response.headers.get('Content-Encoding') == 'gzip':
                content = gzip.decompress(response.read())
            else:
                content = response.read()

            # 解码内容
            content_str = content.decode('utf-8')

        print("下载完成，开始解析规则...", file=sys.stderr)

        # 逐行处理
        lines = content_str.splitlines()
        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # 跳过注释和空行
            if not line or line.startswith('!') or line.startswith('[Adblock Plus]'):
                continue

            # 处理||domain^格式的规则
            if line.startswith('||') and line.endswith('^'):
                # 提取域名部分
                domain = line[2:-1]  # 去掉||和^

                # 跳过无效域名
                if not domain or domain.startswith('.') or domain.endswith('.'):
                    continue

                # 清理域名
                domain = domain.lower().strip()

                # 验证域名格式
                if is_valid_domain(domain):
                    domains.add(domain)

            if line_num % 10000 == 0:
                print(f"已处理 {line_num} 行，收集到 {len(domains)} 个域名", file=sys.stderr)

    except Exception as e:
        print(f"下载或解析文件时出错：{e}", file=sys.stderr)
        return False

    print(f"共收集到 {len(domains)} 个有效域名", file=sys.stderr)

    # 输出Surge规则到标准输出
    try:
        # 获取当前UTC时间
        utc_now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

        # 写入文件头
        print("# NSFW域名规则列表")
        print("# 从ABP NSFW列表转换而来")
        print("# 来源: https://cdn.jsdelivr.net/gh/sjhgvr/oisd@main/abp_nsfw.txt")
        print(f"# 生成时间: {utc_now}")
        print()

        # 按字母顺序排序并输出规则
        sorted_domains = sorted(domains)
        for domain in sorted_domains:
            print(f"DOMAIN-SUFFIX,{domain}")

        print(f"\n# 转换完成！共生成 {len(sorted_domains)} 条规则", file=sys.stderr)

    except Exception as e:
        print(f"输出规则时出错：{e}", file=sys.stderr)
        return False

    return True

def is_valid_domain(domain):
    """
    验证域名格式
    """
    # 简单的域名验证正则表达式
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'

    # 允许包含数字的域名
    if re.match(pattern, domain):
        return True

    # 检查是否是有效的子域名
    if '.' in domain and len(domain) > 1:
        return True

    return False

def main():
    url = "https://cdn.jsdelivr.net/gh/sjhgvr/oisd@main/abp_nsfw.txt"

    print(f"使用默认URL: {url}", file=sys.stderr)

    success = convert_abp_to_surge_from_url(url)

    if success:
        print("转换成功！", file=sys.stderr)
    else:
        print("转换失败！", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
