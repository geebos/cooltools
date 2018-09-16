---
title: readme
date: 2018-09-15 10:52:19
tags: readme
---

# 使用方法


总共有两个参数

-n : name，要创建的文件名称

-t : tags，要创建的文件的标签

如：`create-md -n readme -t test`

生成的文件内容如下：

```markdown
---
title: readme
date: 2018-09-15 10:52:19
tags: readme
---
```

# 注意：

脚本会自动记录上一次的 tag值，如果未指定 tags，默认使用上一次使用的 tags

tags保存在 config下的 tags文件中，在设置过 tags后，该文件夹会自动创建<div style="position: fixed;top: 100px;left: 50px;padding: 5px;border: 1px solid black;">
    <ul style=" position: relative;list-style: none;margin: 0;display: block;padding: 0;">
    <li style="list-style: inherit;display: block;padding: 0;margin: 0;">
    <span style="display: block;min-width: 100px;margin: 5px 0;border-bottom: 1px solid black;">
    使用方法
</span>
</li><ul style=" position: relative;list-style: none;margin: 0 0 0 30px;display: block;padding: 0;">
    <li style="list-style: inherit;display: block;padding: 0;margin: 0;">
    <span style="display: block;min-width: 100px;margin: 5px 0;border-bottom: 1px solid black;">
    注意：
</span>
</li>
</ul>
</ul>
</div>