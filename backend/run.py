import os
from app import create_app, db
from app.models import Family, Person

# Create the Flask application instance
app = create_app()


@app.shell_context_processor
def make_shell_context():
    """
    Make database and models available in Flask shell
    Usage: flask shell
    """
    return {
        'db': db,
        'Family': Family,
        'Person': Person
    }


@app.cli.command()
def seed_db():
    """
    Add sample data to database for testing
    Usage: flask seed_db
    """
    try:
        with app.app_context():
            # Check if data already exists
            if Family.query.count() > 0:
                print("⚠ Database already has data.")
                overwrite = input("Do you want to add more sample data? (yes/no): ")
                if overwrite.lower() != 'yes':
                    return
            
            print("Adding sample data...")
            
            # Create sample families
            family1 = Family(
                family_name="Prabhu's Family",
                address="No. 50, New Street, Velachery, Chennai - 600042"
            )
            db.session.add(family1)
            db.session.flush()  # Get the family ID
            
            # Add members to family 1
            members1 = [
                Person(family_id=family1.id, name="Jayalakshmi"),
                Person(family_id=family1.id, name="Prabhu"),
                Person(family_id=family1.id, name="Usha"),
                Person(family_id=family1.id, name="Ananya"),
                Person(family_id=family1.id, name="Aravind")
            ]
            db.session.add_all(members1)
            
            # Create second family
            family2 = Family(
                family_name="Ramesh's Family",
                address="Flat 12B, Lake View Apartments, Anna Nagar, Chennai - 600040"
            )
            db.session.add(family2)
            db.session.flush()
            
            # Add members to family 2
            members2 = [
                Person(family_id=family2.id, name="Ramesh"),
                Person(family_id=family2.id, name="Priya"),
                Person(family_id=family2.id, name="Karthik")
            ]
            db.session.add_all(members2)
            
            # Create third family (single guest)
            family3 = Family(
                family_name="Kumar (Friend)",
                address="No. 78, Mount Road, T. Nagar, Chennai - 600017"
            )
            db.session.add(family3)
            db.session.flush()
            
            # Add member to family 3
            member3 = Person(family_id=family3.id, name="Kumar")
            db.session.add(member3)
            
            # Commit all changes
            db.session.commit()
            
            print("✓ Sample data added successfully!")
            print(f"  - {Family.query.count()} families in database")
            print(f"  - {Person.query.count()} guests in database")
            
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error seeding database: {str(e)}")


@app.cli.command()
def test_db():
    """
    Test database connection and show stats
    Usage: flask test_db
    """
    try:
        with app.app_context():
            # Try to query the database
            family_count = Family.query.count()
            person_count = Person.query.count()
            
            print("✓ Database connection successful!")
            print(f"  - Database: {app.config['DB_NAME']}")
            print(f"  - Host: {app.config['DB_HOST']}:{app.config['DB_PORT']}")
            print(f"  - User: {app.config['DB_USER']}")
            print(f"  - Families: {family_count}")
            print(f"  - Guests: {person_count}")
            
            if family_count > 0:
                print("\n  Recent families:")
                families = Family.query.order_by(Family.created_at.desc()).limit(3).all()
                for family in families:
                    print(f"    • {family.family_name} ({len(family.members)} members)")
            
    except Exception as e:
        print(f"✗ Database connection failed: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Make sure PostgreSQL is running")
        print("  2. Check your .env file credentials")
        print("  3. Verify the database 'wedding_guests' exists")
        print("     Run in psql: CREATE DATABASE wedding_guests;")
        print("  4. Initialize migrations: flask db init")
        print("  5. Create tables: flask db upgrade")


@app.cli.command()
def clear_data():
    """
    Delete all data but keep tables
    Usage: flask clear_data
    """
    try:
        with app.app_context():
            family_count = Family.query.count()
            person_count = Person.query.count()
            
            if family_count == 0:
                print("⚠ Database is already empty!")
                return
            
            print(f"⚠ WARNING: This will delete {family_count} families and {person_count} guests!")
            confirmation = input("Are you sure? Type 'DELETE' to confirm: ")
            
            if confirmation == 'DELETE':
                Person.query.delete()
                Family.query.delete()
                db.session.commit()
                print("✓ All data cleared successfully!")
            else:
                print("✗ Operation cancelled.")
                
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error clearing data: {str(e)}")


@app.cli.command()
def init_db():
    """
    Initialize database with migrations
    Usage: flask init_db
    
    This is a convenience command that:
    1. Initializes migrations (if not already done)
    2. Creates initial migration
    3. Applies migration to create tables
    """
    import subprocess
    import os
    
    try:
        migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
        
        # Check if migrations directory exists
        if not os.path.exists(migrations_dir):
            print("Step 1: Initializing migrations...")
            result = subprocess.run(['flask', 'db', 'init'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Migrations initialized")
            else:
                print(f"✗ Error: {result.stderr}")
                return
        else:
            print("✓ Migrations already initialized")
        
        # Create migration
        print("\nStep 2: Creating initial migration...")
        result = subprocess.run(
            ['flask', 'db', 'migrate', '-m', 'Initial migration'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ Migration created")
        else:
            print(f"⚠ Note: {result.stderr}")
        
        # Apply migration
        print("\nStep 3: Applying migration to database...")
        result = subprocess.run(['flask', 'db', 'upgrade'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Database tables created successfully!")
            print(f"  - Database: {app.config['DB_NAME']}")
            print(f"  - Tables: families, persons")
        else:
            print(f"✗ Error: {result.stderr}")
            
    except Exception as e:
        print(f"✗ Error initializing database: {str(e)}")
        print("\nManual steps:")
        print("  1. flask db init")
        print("  2. flask db migrate -m 'Initial migration'")
        print("  3. flask db upgrade")


if __name__ == '__main__':
    # Get host and port from environment variables or use defaults
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("=" * 70)
    print("       Wedding Guest Management API - Backend Server")
    print("=" * 70)
    print(f"Environment : {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Server URL  : http://{host}:{port}")
    print(f"Database    : {app.config['DB_NAME']} @ {app.config['DB_HOST']}:{app.config['DB_PORT']}")
    print("=" * 70)
    print("\n📁 DATABASE MIGRATION COMMANDS (Recommended):")
    print("  flask db init              - Initialize migrations folder")
    print("  flask db migrate -m 'msg'  - Create new migration")
    print("  flask db upgrade           - Apply migrations (create tables)")
    print("  flask db downgrade         - Rollback last migration")
    print("  flask db current           - Show current migration version")
    print("  flask db history           - Show migration history")
    print("\n🚀 QUICK START COMMANDS:")
    print("  flask init_db              - Auto setup: init + migrate + upgrade")
    print("  flask test_db              - Test database connection & show stats")
    print("  flask seed_db              - Add sample data for testing")
    print("  flask clear_data           - Delete all data (keep tables)")
    print("\n💡 FIRST TIME SETUP:")
    print("  1. Make sure PostgreSQL is running")
    print("  2. Create database: psql -U postgres -c 'CREATE DATABASE wedding_guests;'")
    print("  3. Run: flask init_db")
    print("  4. Run: flask seed_db")
    print("  5. Run: python run.py")
    print("=" * 70)
    print("\n✨ Starting server... Press CTRL+C to stop\n")
    
    # Run the Flask development server
    try:
        app.run(
            host=host,
            port=port,
            debug=debug
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped gracefully. Goodbye!")
    except Exception as e:
        print(f"\n✗ Error starting server: {str(e)}")
