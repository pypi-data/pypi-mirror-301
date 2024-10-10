from japick.main import parse, parse_html
from japick.syntax import MASK_SYMBOL


def test_it():
    body = """# これはテストです
こんにちは。
これは文章です。

* リスト
* リスト2と `code` もあります

<section>
  ここは別のパラグラフです。
  Shodo（https://shodo.ink/）とこの次の文字、Xのインデックスを取りましょう。
</section>"""
    paragraphs = list(parse(body))
    assert len(paragraphs) == 5
    assert paragraphs[0].is_head
    assert paragraphs[0].body == "これはテストです"
    assert paragraphs[1].body == "こんにちは。\nこれは文章です。"
    assert paragraphs[2].is_list
    assert paragraphs[2].body == "リスト"
    assert paragraphs[3].is_list
    assert paragraphs[3].body == f"リスト2と {MASK_SYMBOL * 6} もあります"
    assert paragraphs[3].as_original_pos(15) == (5, 17)
    assert paragraphs[3].as_original_index(15) == 51
    assert body[51] == "り"
    assert (
        paragraphs[4].body
        == """\
ここは別のパラグラフです。
Shodo（）とこの次の文字、Xのインデックスを取りましょう。"""
    )
    assert paragraphs[4].as_original_pos(29) == (9, 35)
    assert paragraphs[4].as_original_index(29) == 117
    assert body[117] == "X"


def test_html():
    html = """<h1>これはテストです</h1>
<p>こんにちは。</p>
<ul>
  <li>リスト</li>
  <li>リスト2と <code class="foo">code</code> もあります</li>
</ul>
  <p>
    ここは別のパラ
    グラフです。
  </p>
"""
    paragraphs = list(parse_html(html))
    assert len(paragraphs) == 5
    assert paragraphs[0].is_head
    assert paragraphs[0].body == "これはテストです"
    assert paragraphs[0].as_original_index(3) == 7

    assert not paragraphs[1].is_list
    assert not paragraphs[1].is_head
    assert paragraphs[1].body == "こんにちは。"

    assert paragraphs[2].is_list
    assert paragraphs[2].body == "リスト"

    assert paragraphs[3].is_list
    assert paragraphs[3].body == f"リスト2と {MASK_SYMBOL * 4} もあります"
    assert paragraphs[3].as_original_index(6) == 82
    assert paragraphs[3].as_original_pos(6) == (4, 30)
    assert paragraphs[3].as_original_pos(10, lazy=True) == (4, 34)
    assert paragraphs[3].as_original_pos(10) == (4, 41)

    assert paragraphs[4].body == "\nここは別のパラ\nグラフです。\n"
    assert paragraphs[4].as_original_index(10) == 134
    assert paragraphs[4].as_original_pos(10) == (8, 5)
