def test_should_access_battery_page(client):
    response = client.get('/equipments/battery')
    assert response.status_code == 200

def test_should_block_unauthorized_access_to_change_battery_mode(client):
    response = client.post('/equipments/battery/change_battery_mode', data={
        'mode': 'discharge'
    })
    assert response.status_code == 403


