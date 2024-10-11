import sys

import megfile as mf
from pypandoc import convert_text
from loguru import logger

sys.path.append('/data/workspace/pdf_parse_pipeline')
from offline.benchmark.table.src.convert_clean_html import clean_html, html_table_to_markdown


test_latex_table = r"""
\begin{tabular}{|c|c|c|c|}
    \hline \multicolumn{4}{|c|}{ 发行要素 } \\
    \hline 名称 & \begin{tabular}{c} 
    韵达控股股份有限 \\
    公司 2022 年度第 \\
    三期超短期融资券
    \end{tabular} & 简称 & \begin{tabular}{c}
    22 韵达股份 \\
    SCP003
    \end{tabular} & \begin{tabular}{c}
    \hline 代码 & 012282550.IB & 期限 & 140 天 \\
    \hline 利率类型 & \multicolumn{3}{|c|}{ 固定利率 } \\
    \hline 起息日 & 2022 年 7 月 20 日 & 兄付日 & 2022 年 12 月 7 日 \\
    \hline 计划发行总额 & 4 亿元 & 实际发行总额 & 4 亿元 \\
    \hline 发行利率 & \(2.40 \%\) & 发行价格 & 100 元/百元面值 \\
    \hline 主承销商 & \multicolumn{3}{|c|}{ 招商银行股份有限公司、中国银行股份有限公司 } \\
    \hline
\end{tabular}
"""

def read_txt_file(filename: str) -> str:
    # 读取 txt 中的内容，并整个放到 content 变量中，content 的类型是 str。
    with mf.smart_open(filename, 'rb') as file:
        content = file.read()
        decompressed_content = file.read().decode('utf-8') 
    return content, decompressed_content

def read_html_file(html_file_path):
    # 使用 'open' 函数以读取模式 ('r') 打开文件
    # 编码设置为 'utf-8'，这是常见的网页编码方式
    with open(html_file_path, 'r', encoding='utf-8') as file:
        # 读取文件内容
        html_content = file.read()

    # 输出HTML内容
    print(html_content)


def latex2html2md(latex_code, htmlpath, mdpath):
    try:
        # origin_html = convert_text(latex_code, 'md', format='latex')
        # ailab_clean_html = clean_html(origin_html)
        html = '/data/tmp_data/0923/latex2html_rsts/test.html'
        # html = '/data/tmp_data/0923/Title.html'
        with open(html, 'r', encoding='utf-8') as file:
        # 读取文件内容
            html_content = file.read()
        ailab_md = html_table_to_markdown(html_content)
        origin_html = convert_text(html_content, 'md', format='html')
        # img_name = mf.SmartPath(img).name
        # img_dict = {
        #     img_name: {
        #         "ailab_html": ailab_clean_html,
        #         "ailab_md": ailab_md
        #     }
        # }
        print(11111)
        # with mf.smart_open(htmlpath, 'w') as html_file:
        #     html_file.write(ailab_clean_html)
        with mf.smart_open(mdpath, "w") as md_file:
            md_file.write(ailab_md)
    except Exception as e:
        logger.error(f'error is {e}')


if __name__=='__main__':
    # txtpath = 's3://fucheng/test/0923/GOT_ocr/cpu/table_datas/0007.txt'
    # latex_table_content, decompressed_content = read_txt_file(txtpath)
    latex_table_content = test_latex_table
    htmlpath = 's3://fucheng/test/0923/test_latex_table.html'
    mdpath = 's3://fucheng/test/0923/test_latex_table.md'
    latex2html2md(latex_table_content, htmlpath, mdpath)