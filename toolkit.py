

import os
import re
a= "![在这里插入图片描述](D:\00note\MD\.pic\watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NzeHlwcg==,size_16,color_FFFFFF,t_70-16447402270516.png)"
per_md_pic_list = re.findall(r'!\[.*?]\((.*?)\)', a)
print(per_md_pic_list)



