#!/usr/bin/env python
"""
Simple script to display all user data.
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediconnect_project.settings')
django.setup()

from mediconnect_app.models import CustomUser

def display_users():
    """Display all users."""
    users = CustomUser.objects.all()
    
    print("=" * 70)
    print("ALL USERS IN DATABASE")
    print("=" * 70)
    
    for user in users:
        print(f"\nUser ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"First Name: '{user.first_name}'")
        print(f"Last Name: '{user.last_name}'")
        print(f"Role: {user.role}")
        
        # Check for template syntax
        has_template_first = '{{' in (user.first_name or '')
        has_template_last = '{{' in (user.last_name or '')
        
        if has_template_first or has_template_last:
            print("⚠️  WARNING: This user has template syntax in their name!")
            if has_template_first:
                print(f"   - Template found in first_name")
            if has_template_last:
                print(f"   - Template found in last_name")
        
        print("-" * 70)
    
    print(f"\nTotal users: {users.count()}")
    print("=" * 70)

if __name__ == '__main__':
    display_users()
