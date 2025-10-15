#!/usr/bin/env python3
"""
Test script to check if Flask can serve static files.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_static_files():
    """Test if Flask can serve static files."""
    print("Testing static file serving...")
    
    # Create app
    app = create_app('testing')
    
    # Test the static file endpoint
    with app.test_client() as client:
        response = client.get('/static/js/main.js')
        print(f"Static file status: {response.status_code}")
        if response.status_code == 200:
            print(f"Static file content length: {len(response.data)}")
            print("Static file serving is working correctly!")
        else:
            print(f"Error response: {response.get_json()}")
            
            # Let's also check what files Flask thinks are available
            static_folder = app.static_folder
            if static_folder and os.path.exists(static_folder):
                print("Static folder exists")
                js_folder = os.path.join(static_folder, 'js')
                if os.path.exists(js_folder):
                    print("JS folder exists")
                    main_js = os.path.join(js_folder, 'main.js')
                    
                    if os.path.exists(main_js):
                        print("main.js file exists")
                        print(f"main.js size: {os.path.getsize(main_js)} bytes")
                    else:
                        print("main.js file does not exist")
                else:
                    print("JS folder does not exist")
            else:
                print("Static folder does not exist")

if __name__ == "__main__":
    test_static_files()