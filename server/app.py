#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return '<h1>Bakery GET API</h1>'

    @app.route('/bakeries', methods=['GET'])
    def bakeries():
        bakeries = Bakery.query.all()
        return jsonify([bakery.to_dict(rules=('-baked_goods.bakery',)) for bakery in bakeries])

    @app.route('/bakeries/<int:id>', methods=['GET'])
    def bakery_by_id(id):
        bakery = Bakery.query.get_or_404(id)
        return jsonify(bakery.to_dict(rules=('-baked_goods.bakery',)))

    @app.route('/baked_goods/by_price', methods=['GET'])
    def baked_goods_by_price():
        baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
        if not baked_goods:  
            return jsonify([]), 200  
        return jsonify([baked_good.to_dict(rules=('-bakery.baked_goods',)) for baked_good in baked_goods])

    @app.route('/baked_goods/most_expensive', methods=['GET'])
    def most_expensive_baked_good():
        baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
        if not baked_good:  
            return jsonify({"message": "No baked goods found"}), 404  
        return jsonify(baked_good.to_dict(rules=('-bakery.baked_goods',))), 200

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)