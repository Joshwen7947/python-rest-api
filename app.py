from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
db = SQLAlchemy(app)

# Define the Destination model 
class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    destination = db.Column(db.String(100), nullable=False) 
    country = db.Column(db.String(100), nullable=False) 
    rating = db.Column(db.Float, nullable=False)  

    def to_dict(self):
        return {
            "id": self.id,
            "destination": self.destination,
            "country": self.country,
            "rating": self.rating
        }

# Create the database tables (if they don't exist)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Travel API!"})

# Route to get all destinations from the database (GET method)
@app.route('/destinations', methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([destination.to_dict() for destination in destinations])

# Route to get a specific destination by its ID (GET method)
@app.route('/destinations/<int:destination_id>', methods=['GET'])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error": "Destination not found"}), 404

# Route to add a new destination to the database (POST method)
@app.route('/destinations', methods=['POST'])
def add_destination():
    # Parse the incoming JSON request body to extract data
    data = request.get_json()

    new_destination = Destination(
        destination=data["destination"],
        country=data["country"],
        rating=data["rating"]
    )
    db.session.add(new_destination)
    db.session.commit()

    return jsonify(new_destination.to_dict()), 201

# Route to update an existing destination by its ID (PUT method)
@app.route('/destinations/<int:destination_id>', methods=['PUT'])
def update_destination(destination_id):
    # Parse the incoming JSON request body to extract data
    data = request.get_json()
    
    destination = Destination.query.get(destination_id)
    if destination:
        destination.destination = data.get("destination", destination.destination)
        destination.country = data.get("country", destination.country)
        destination.rating = data.get("rating", destination.rating)
        db.session.commit()
        
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error": "Destination not found"}), 404

# Route to delete a destination by its ID (DELETE method)
@app.route('/destinations/<int:destination_id>', methods=['DELETE'])
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        db.session.delete(destination)
        db.session.commit()
        return jsonify({"message": "Destination deleted"})
    else:
        return jsonify({"error": "Destination not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
