from flask import Blueprint, jsonify, abort
from flask import render_template
from flask import request

from election.db import get_db
from election.election_lib import simulate_election

bp = Blueprint("election", __name__, url_prefix="/election")


# Define the list of regions and parties
@bp.route('/regions', methods=['GET','PUT', 'DELETE'])
def regions():
    if request.method == 'GET':
        db= get_db()
        regions=db.execute("SELECT region_name, seats FROM region").fetchall()
        return jsonify(regions)
    elif request.method == 'PUT':
        request_json = request.get_json()
        new_region_name = request_json['region_name']
        new_seats= request_json['number_of_seats']
        db= get_db()
        try:
            db.execute("INSERT INTO region (region_name, seats) VALUES (?, ?)",
                        (new_region_name,new_seats))
            db.commit()
        except db.IntegrityError:
            error = f"{new_region_name} is already registered."
            abort(406,description = error)
        return (f'{new_region_name} is successfully added with {new_seats} seats')
    elif request.method == "DELETE":
        request_json = request.get_json()
        new_region_name = request_json['region_name']
        db= get_db()
        db.execute("DELETE FROM region WHERE region_name = ?",
                    (new_region_name,))
        db.commit()
        return (f'{new_region_name} is successfully deleted')
    else:
        abort(403, description = "Unsupported method.")    

#Define the list of regions and parties
@bp.route('/parties', methods=['GET', 'PUT', 'DELETE'])
def parties():
    if request.method == 'PUT':
        request_json = request.get_json()
        new_party_name = request_json['party_name']
        db= get_db()
        try:
            db.execute("INSERT INTO parties (party_name) VALUES (?)",
                        (new_party_name,))
            db.commit()
        except db.IntegrityError:
            error = f"{new_party_name} is already registered."
            abort(406,description = error)
        return (f'{new_party_name} is successfully added')
    elif request.method == 'GET':    
	# Render the HTML form with the list of regions and parties
        db=get_db()
        parties=db.execute("SELECT party_name FROM parties").fetchall()
        return jsonify(parties)
    elif request.method == "DELETE":
        request_json = request.get_json()
        new_party_name = request_json['party_name']
        db= get_db()
        db.execute("DELETE FROM parties WHERE party_name = ?",
                    (new_party_name,))
        db.commit()
        return (f'{new_party_name} is successfully deleted')
    else:
        abort(403, description = "Unsupported method.")

@bp.route('/simulate', methods=['POST'])
def simulate():
	# Get the user-selected values from the form submission
    request_json = request.get_json()
    selected_region = request_json["region"]
    db=get_db()
    parties=db.execute("SELECT party_name FROM parties").fetchall()
    party_percentages = {party['party_name']: float(request_json[party['party_name']] or 0) for party in parties}
    
    regions=db.execute("SELECT region_name, seats FROM region ").fetchall()
    vote_data = {}
    for region in regions:
        vote_data[region['region_name']] = {"seats":region["seats"]}  
    # Call the election simulator function with the user-selected values
    seat_counts = simulate_election(vote_data, [party['party_name'] for party in parties], selected_region, party_percentages)
    # Render the election results using a separate HTML template
    return seat_counts
