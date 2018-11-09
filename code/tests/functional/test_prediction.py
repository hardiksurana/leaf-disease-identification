import json
import pytest
import pytest_flask

def test_prediction(client):
    data = {
        'feature_array': [7.4,0.66,0,1.8,0.075,13,40,0.9978,3.51,0.56,9.4]
    }
    res = client.post('/predict', data=json.dumps(data))

    print(json.loads(res.data)['predictions'][0])
    assert False
    # assert res.status_code == 200
