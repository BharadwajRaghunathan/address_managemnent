from flask import Blueprint, request, jsonify, send_file
from app import db
from app.models import Family, Person
from app.utils import generate_excel_export, generate_csv_export
from datetime import datetime

# Create Blueprint
bp = Blueprint('api', __name__, url_prefix='/api')


# ==================== FAMILY ROUTES ====================

@bp.route('/families', methods=['GET'])
def get_families():
    """Get all families with their members"""
    try:
        families = Family.query.order_by(Family.created_at.desc()).all()
        return jsonify([family.to_dict() for family in families]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/families/<int:id>', methods=['GET'])
def get_family(id):
    """Get a single family by ID"""
    try:
        family = Family.query.get_or_404(id)
        return jsonify(family.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@bp.route('/families', methods=['POST'])
def create_family():
    """Create a new family"""
    try:
        data = request.json
        
        # Validation
        if not data.get('family_name'):
            return jsonify({'error': 'Family name is required'}), 400
        if not data.get('address'):
            return jsonify({'error': 'Address is required'}), 400
        
        # Create new family
        new_family = Family(
            family_name=data['family_name'].strip(),
            address=data['address'].strip()
        )
        
        db.session.add(new_family)
        db.session.commit()
        
        return jsonify(new_family.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/families/<int:id>', methods=['PUT'])
def update_family(id):
    """Update an existing family"""
    try:
        family = Family.query.get_or_404(id)
        data = request.json
        
        # Validation
        if 'family_name' in data and not data['family_name'].strip():
            return jsonify({'error': 'Family name cannot be empty'}), 400
        if 'address' in data and not data['address'].strip():
            return jsonify({'error': 'Address cannot be empty'}), 400
        
        # Update fields
        if 'family_name' in data:
            family.family_name = data['family_name'].strip()
        if 'address' in data:
            family.address = data['address'].strip()
        
        family.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(family.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/families/<int:id>', methods=['DELETE'])
def delete_family(id):
    """Delete a family and all its members"""
    try:
        family = Family.query.get_or_404(id)
        family_name = family.family_name
        member_count = len(family.members)
        
        db.session.delete(family)
        db.session.commit()
        
        return jsonify({
            'message': f'Family "{family_name}" and {member_count} member(s) deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== PERSON ROUTES ====================

@bp.route('/persons', methods=['POST'])
def create_person():
    """Add a new person to a family"""
    try:
        data = request.json
        
        # Validation
        if not data.get('family_id'):
            return jsonify({'error': 'Family ID is required'}), 400
        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        # Check if family exists
        family = Family.query.get(data['family_id'])
        if not family:
            return jsonify({'error': 'Family not found'}), 404
        
        # Create new person
        new_person = Person(
            family_id=data['family_id'],
            name=data['name'].strip()
        )
        
        db.session.add(new_person)
        db.session.commit()
        
        return jsonify(new_person.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/persons/<int:id>', methods=['PUT'])
def update_person(id):
    """Update a person's details"""
    try:
        person = Person.query.get_or_404(id)
        data = request.json
        
        # Validation
        if 'name' in data and not data['name'].strip():
            return jsonify({'error': 'Name cannot be empty'}), 400
        
        # Update fields
        if 'name' in data:
            person.name = data['name'].strip()
        
        person.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(person.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/persons/<int:id>', methods=['DELETE'])
def delete_person(id):
    """Delete a person from a family"""
    try:
        person = Person.query.get_or_404(id)
        person_name = person.name
        
        db.session.delete(person)
        db.session.commit()
        
        return jsonify({
            'message': f'Person "{person_name}" deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== EXPORT ROUTES ====================

@bp.route('/export/excel', methods=['GET'])
def export_excel():
    """Export guest list as Excel file"""
    try:
        families = Family.query.order_by(Family.family_name).all()
        
        excel_file, filename = generate_excel_export(families)
        
        return send_file(
            excel_file,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/export/csv', methods=['GET'])
def export_csv():
    """Export guest list as CSV file"""
    try:
        families = Family.query.order_by(Family.family_name).all()
        
        csv_file, filename = generate_csv_export(families)
        
        return send_file(
            csv_file,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== STATS ROUTE ====================

@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    try:
        total_families = Family.query.count()
        total_guests = Person.query.count()
        
        return jsonify({
            'total_families': total_families,
            'total_guests': total_guests
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== SEARCH ROUTE ====================

@bp.route('/search', methods=['GET'])
def search():
    """Search families by name, member name, or address"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify([]), 200
        
        # Search in family names and addresses
        families = Family.query.filter(
            db.or_(
                Family.family_name.ilike(f'%{query}%'),
                Family.address.ilike(f'%{query}%')
            )
        ).all()
        
        # Search in person names
        persons = Person.query.filter(Person.name.ilike(f'%{query}%')).all()
        
        # Get unique families from person search
        person_families = {person.family for person in persons}
        
        # Combine and remove duplicates
        all_families = set(families) | person_families
        
        # Convert to dict and sort
        result = sorted(
            [family.to_dict() for family in all_families],
            key=lambda x: x['family_name']
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
