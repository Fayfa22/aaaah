#!/usr/bin/env python
"""
Script to fix corrupted user names that contain Django template syntax.
This script removes template syntax like {{ message.sender.last_name }} from user names.
"""
import os
import sys
import django
import re

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediconnect_project.settings')
django.setup()

from mediconnect_app.models import CustomUser

def clean_template_syntax(text):
    """Remove Django template syntax from text."""
    if not text:
        return text
    
    # Remove {{ ... }} patterns
    cleaned = re.sub(r'\{\{[^}]+\}\}', '', text)
    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())
    return cleaned.strip()

def fix_user_names():
    """Fix all users with corrupted names."""
    users = CustomUser.objects.all()
    fixed_count = 0
    
    print("Scanning users for corrupted names...")
    print("-" * 50)
    
    for user in users:
        original_first = user.first_name
        original_last = user.last_name
        
        # Check if names contain template syntax
        has_template_first = '{{' in (user.first_name or '')
        has_template_last = '{{' in (user.last_name or '')
        
        if has_template_first or has_template_last:
            print(f"\nFound corrupted user: {user.email}")
            print(f"  Original first_name: {original_first}")
            print(f"  Original last_name: {original_last}")
            
            # Clean the names
            if has_template_first:
                user.first_name = clean_template_syntax(user.first_name)
            if has_template_last:
                user.last_name = clean_template_syntax(user.last_name)
            
            # Save the user
            user.save()
            
            print(f"  Fixed first_name: {user.first_name}")
            print(f"  Fixed last_name: {user.last_name}")
            
            fixed_count += 1
    
    print("\n" + "=" * 50)
    print(f"Total users scanned: {users.count()}")
    print(f"Users fixed: {fixed_count}")
    print("=" * 50)

if __name__ == '__main__':
    print("Starting user name cleanup...")
    print("=" * 50)
    fix_user_names()
    print("\nCleanup complete!")
