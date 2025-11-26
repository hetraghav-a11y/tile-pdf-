from app import app, Tile
with app.app_context():
    rows = [(t.id, t.name, t.web_path) for t in Tile.query.order_by(Tile.id).all()]
    print(rows)
