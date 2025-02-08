import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_africastalking():
    """Mock Africa's Talking API calls during tests"""
    mock_sms = MagicMock()
    
    # Configure the mock to return a success response
    mock_sms.send.return_value = {
        'SMSMessageData': {
            'Message': 'Sent',
            'Recipients': [{
                'statusCode': 101,
                'status': 'Success',
                'messageId': 'test-id',
                'cost': 'KES 0.00',
                'number': '+254711111111'
            }]
        }
    }
    
    # Mock both the SMS class and the utility functions
    with patch('savannah_app.utils.africastalking.SMS', return_value=mock_sms) as mock:
        # Also mock the utility functions that actually send the SMS
        with patch('savannah_app.views.send_order_confirmation') as mock_confirm:
            with patch('savannah_app.views.send_order_notification') as mock_notify:
                yield {
                    'sms': mock_sms,
                    'confirm': mock_confirm,
                    'notify': mock_notify
                }