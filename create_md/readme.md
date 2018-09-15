---
title: readme
date: 2018-09-15 10:52:19
tags: readme
---

# 使用方法

<script>
function get_node(text) {
            let li = document.createElement('li');
            let span = document.createElement('span');

            span.className = 'cntent-title';
            span.innerText = text;

            //添加点击事件 点击隐藏或显示当前标签下的 ul标签
            /* span.onclick = function() {
                let ul = this.parentElement.getElementsByTagName('ul')[0];
                let spans = this.parentElement.parentElement;
                if (ul) {
                    if (ul.style.display == 'none') {
                        ul.style.display = 'block';
                        this.style.width = '-webkit-fill-available';
                        set_width(spans, this.offsetWidth);
                        this.style.width = '-webkit-fill-available';
                    } else {
                        ul.style.display = 'none';
                        set_width(spans, '100px');
                    }
                }
            } */
            li.appendChild(span);

            return li;
        }

        function genContent(l_list) {
            let all_elements = document.body.childNodes;
            let node_list = [];
            let top_l = Infinity;
            let container = document.createElement('div');
            container.className = 'content-container';

            for (let i = 0; i < all_elements.length; i++) {
                let l = l_list.indexOf(all_elements[i].localName) + 1;
                if (l > 0) {
                    let text = all_elements[i].innerText;
                    let node = get_node(text);

                    if (top_l >= l) {
                        top_l = l - 1;
                        node_list[top_l] = container;
                    }

                    if (node_list[l + 1]) {
                        node_list[l + 1] = undefined;
                    }

                    if (!node_list[l]) {
                        let ul = document.createElement('ul');
                        //ul.style.display = (l - 1 == top_l ? 'block' : 'none');
                        ul.appendChild(node);
                        node_list[l - 1].appendChild(ul);
                        node_list[l - 1] = ul;
                        node_list[l] = node;
                    } else {
                        node_list[l - 1].appendChild(node);
                        node_list[l] = node;
                    }
                }
            }
            console.log(container);
            document.body.appendChild(container);
            return container;
        }

        window.onload = function() {
            let style = 'ul,ol,li {    list-style: inherit;}.content-container {    position: fixed;    top: 100px;    left: 50px;    border: 1px solid black;}.content-container ul,.content-container li {    display: block;    padding: 0;    margin: 0;}.content-container ul {    position: relative;    list-style: none;    margin-left: 30px;}.content-container>ul {    margin: 5px;}.content-container li span {    display: block;    min-width: 100px;    margin: 5px 0;    border-bottom: 1px solid black;}';
            let style_tag = document.createElement('style');
            style_tag.type = 'text/css';
            style_tag.innerHTML = style;
            document.head.appendChild(style_tag);
            genContent(['h1', 'h2', 'h3', 'h4']);
        }
</script>

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

tags保存在 config下的 tags文件中，在设置过 tags后，该文件夹会自动创建