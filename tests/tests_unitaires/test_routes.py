from server import (
    index,
)

def test_index_renders_template(monkeypatch):
    monkeypatch.setattr('server.render_template', lambda x: f'MOCKED TEMPLATE: {x}')
    assert index() == "MOCKED TEMPLATE: index.html"
