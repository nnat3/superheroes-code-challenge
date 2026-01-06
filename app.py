from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Hero(db.Model):
    __tablename__ = 'heroes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)
    
    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete-orphan')
    
    def to_dict(self, include_powers=False):
        data = {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name
        }
        if include_powers:
            data['hero_powers'] = [hp.to_dict() for hp in self.hero_powers]
        return data

class Power(db.Model):
    __tablename__ = 'powers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    hero_powers = db.relationship('HeroPower', backref='power', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    
    def to_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'strength': self.strength
        }
        if include_relations:
            data['hero'] = self.hero.to_dict()
            data['power'] = self.power.to_dict()
        else:
            data['power'] = self.power.to_dict()
        return data

@app.route('/heroes')
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

@app.route('/heroes/<int:id>')
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    return jsonify(hero.to_dict(include_powers=True))

@app.route('/powers')
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@app.route('/powers/<int:id>')
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    return jsonify(power.to_dict())

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    
    data = request.get_json()
    if 'description' in data:
        if not data['description'] or len(data['description']) < 20:
            return jsonify({'errors': ['validation errors']}), 400
        power.description = data['description']
    
    try:
        db.session.commit()
        return jsonify(power.to_dict())
    except:
        return jsonify({'errors': ['validation errors']}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    if not data or 'strength' not in data or data['strength'] not in ['Strong', 'Weak', 'Average']:
        return jsonify({'errors': ['validation errors']}), 400
    
    try:
        hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        
        db.session.add(hero_power)
        db.session.commit()
        
        return jsonify(hero_power.to_dict(include_relations=True)), 201
    except:
        return jsonify({'errors': ['validation errors']}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)