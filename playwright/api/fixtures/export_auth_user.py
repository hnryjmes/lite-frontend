def export_auth_user(email):
    return {
      'email': email,
      'user_profile': {
        'first_name': 'Automated',
        'last_name': 'Test',
      },
      'sites': {},
      'role': '00000000-0000-0000-0000-000000000003',
    }
