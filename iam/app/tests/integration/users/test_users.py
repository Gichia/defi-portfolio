from sqlmodel import Session


def test_get_users(client, db_session: Session):
    """Test fetching all users."""
    
    response = client.get('/api/v1/users/')

    assert response.status_code == 200
    data = response.json()
    users = data['data']['users']

    assert len(users) == 0
