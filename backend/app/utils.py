from datetime import datetime
from io import BytesIO
import pandas as pd


def generate_excel_export(families):
    """
    Generate Excel file with grouped family format
    Returns: (BytesIO object, filename)
    """
    
    # Create formatted data
    output = []
    output.append(['WEDDING GUEST LIST'])
    output.append([''])  # Empty row
    output.append([''])  # Empty row
    
    total_guests = 0
    total_families = len(families)
    
    for family in families:
        # Get all members for this family
        members = family.members
        member_names = ', '.join([person.name for person in members])
        member_count = len(members)
        total_guests += member_count
        
        # Add family block
        output.append([f'Family: {family.family_name}'])
        output.append([f'Address: {family.address}'])
        output.append([f'Members: {member_names}'])
        output.append([f'Total: {member_count}'])
        output.append([''])  # Empty row separator
        output.append(['─' * 70])  # Separator line
        output.append([''])  # Empty row
    
    # Add grand total
    output.append([''])
    output.append([f'GRAND TOTAL: {total_guests} Guests from {total_families} Families'])
    
    # Create DataFrame
    df = pd.DataFrame(output)
    
    # Create Excel file in memory
    excel_file = BytesIO()
    
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, header=False, sheet_name='Guest List')
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Guest List']
        
        # Auto-adjust column width
        worksheet.column_dimensions['A'].width = 80
    
    excel_file.seek(0)
    
    # Generate filename with current date
    filename = f'wedding_guests_{datetime.now().strftime("%d_%b_%Y")}.xlsx'
    
    return excel_file, filename


def generate_csv_export(families):
    """
    Generate CSV file with grouped family format
    Returns: (BytesIO object, filename)
    """
    
    # Create formatted data as text
    output = []
    output.append('WEDDING GUEST LIST\n')
    output.append('\n')
    
    total_guests = 0
    total_families = len(families)
    
    for family in families:
        # Get all members for this family
        members = family.members
        member_names = ', '.join([person.name for person in members])
        member_count = len(members)
        total_guests += member_count
        
        # Add family block
        output.append(f'Family: {family.family_name}\n')
        output.append(f'Address: {family.address}\n')
        output.append(f'Members: {member_names}\n')
        output.append(f'Total: {member_count}\n')
        output.append('\n')
        output.append('─' * 70 + '\n')
        output.append('\n')
    
    # Add grand total
    output.append('\n')
    output.append(f'GRAND TOTAL: {total_guests} Guests from {total_families} Families\n')
    
    # Convert to string
    csv_content = ''.join(output)
    
    # Create CSV file in memory
    csv_file = BytesIO(csv_content.encode('utf-8'))
    csv_file.seek(0)
    
    # Generate filename with current date
    filename = f'wedding_guests_{datetime.now().strftime("%d_%b_%Y")}.csv'
    
    return csv_file, filename


def format_family_for_display(family):
    """
    Format a single family object for frontend display
    Returns: Dictionary with formatted data
    """
    
    members = family.members
    member_names = [person.name for person in members]
    
    return {
        'id': family.id,
        'family_name': family.family_name,
        'address': family.address,
        'members': member_names,
        'member_count': len(members),
        'member_objects': [member.to_dict() for member in members],
        'created_at': family.created_at.isoformat() if family.created_at else None,
        'updated_at': family.updated_at.isoformat() if family.updated_at else None
    }


def validate_family_data(data):
    """
    Validate family input data
    Returns: (is_valid, error_message)
    """
    
    if not data:
        return False, 'No data provided'
    
    if not data.get('family_name') or not data['family_name'].strip():
        return False, 'Family name is required and cannot be empty'
    
    if not data.get('address') or not data['address'].strip():
        return False, 'Address is required and cannot be empty'
    
    if len(data['family_name'].strip()) > 200:
        return False, 'Family name is too long (maximum 200 characters)'
    
    return True, None


def validate_person_data(data):
    """
    Validate person input data
    Returns: (is_valid, error_message)
    """
    
    if not data:
        return False, 'No data provided'
    
    if not data.get('name') or not data['name'].strip():
        return False, 'Name is required and cannot be empty'
    
    if not data.get('family_id'):
        return False, 'Family ID is required'
    
    if len(data['name'].strip()) > 200:
        return False, 'Name is too long (maximum 200 characters)'
    
    try:
        family_id = int(data['family_id'])
        if family_id <= 0:
            return False, 'Invalid family ID'
    except (ValueError, TypeError):
        return False, 'Family ID must be a valid number'
    
    return True, None


def get_family_summary(families):
    """
    Get summary statistics for a list of families
    Returns: Dictionary with summary data
    """
    
    if not families:
        return {
            'total_families': 0,
            'total_guests': 0,
            'average_family_size': 0,
            'largest_family': None,
            'smallest_family': None
        }
    
    total_guests = sum(len(family.members) for family in families)
    family_sizes = [(family.family_name, len(family.members)) for family in families]
    
    largest = max(family_sizes, key=lambda x: x[1]) if family_sizes else None
    smallest = min(family_sizes, key=lambda x: x[1]) if family_sizes else None
    
    return {
        'total_families': len(families),
        'total_guests': total_guests,
        'average_family_size': round(total_guests / len(families), 1) if families else 0,
        'largest_family': {'name': largest[0], 'size': largest[1]} if largest else None,
        'smallest_family': {'name': smallest[0], 'size': smallest[1]} if smallest else None
    }
