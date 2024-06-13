#!/opt/anaconda/bin/python
# -*- coding: utf-8 -*-

from xhtml2pdf import pisa
import numpy as np
import random

twotonine = np.arange(2,10)
problems = [f"{e} x {e2} =" for e2 in twotonine for e in twotonine]

# 30문 랜덤 출제, 중복 없음
pm = [random.sample(problems, k=30) for e in np.arange(0, 10)]
p = [e for r in pm for e in r]

#p2 = random.sample(problems, k=60)
#p3 = random.sample(problems, k=60)
# 30문 랜덤 출제, 중복 있음
#p2 = random.choices(problems, k=30)

[print(e) for e in p]

content = "</br>".join([str(e) for e in p])

# a4 size 1123 x 794 in 96 dpi
# a4 size 595 × 842 pts in postscripts
# letter size 
# Define your data
source_html = """
<html>
<head>
<style type="text/css">
    @page {
        size: a4 portrait;
        @frame header_frame {           /* Static frame */
            -pdf-frame-content: header_content;
            left: 50pt; width: 512pt; top: 50pt; height: 40pt;
        }
        @frame col1_frame {             /* Content frame 1 */
            left: 50pt; width: 225pt; top: 90pt; height: 700pt;
        }
        @frame col2_frame {             /* Content frame 2 */
            left: 310pt; width: 225pt; top: 90pt; height: 700pt;
        }
        @frame footer_frame {           /* Static frame */
            -pdf-frame-content: footer_content;
            left: 50pt; width: 512pt; top: 772pt; height: 20pt;
        }
    }

    .chs { font-family: STSong-Light }
    .cht { font-family: MSung-Light }

    .jpn1 { font-family: HeiseiMin-W3 }
    .jpn2 { font-family: HeiseiKakuGo-W5 }

    .kor1 { font-family: HYSMyeongJo-Medium }
    .kor2 { font-family: HYGothic-Medium }

</style>
<head>
<body>
    <div id="header_content" 
         class="kor2" 
         style="font-weight:bold;font-size:30px;">곱셈연습문제 (초등2)</div>
    <div id="footer_content">(c) - page <pdf:pagenumber> of <pdf:pagecount>
    </div>
    <p style="font-size:30px">""" + content + """</p>
</body>
</html>
"""
output_filename = "test.pdf"

# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err

# Main program
if __name__ == "__main__":
    pisa.showLogging()
    convert_html_to_pdf(source_html, output_filename)