# savannah_app/tests/test_utils.py
import pytest
from unittest.mock import patch
from savannah_app.utils import send_sms, send_admin_email, send_order_notification

@pytest.mark.django_db
class TestNotifications:
    @patch('savannah_app.utils.initialize_africastalking')
    def test_send_sms(self, mock_at):
        mock_sms = mock_at.return_value
        mock_sms.send.return_value = {
            'SMSMessageData': {
                'Recipients': [{'status': 'Success'}]
            }
        }
        
        result = send_sms('1234567890', 'Test message')
        assert result is not None
        mock_sms.send.assert_called_once()
    
    @patch('savannah_app.utils.send_mail')
    def test_send_admin_email(self, mock_send_mail):
        mock_send_mail.return_value = 1
        result = send_admin_email('Test Subject', 'Test Content')
        assert result is True
        mock_send_mail.assert_called_once()
    
    @patch('savannah_app.utils.send_sms')
    @patch('savannah_app.utils.send_admin_email')
    def test_order_notification(self, mock_email, mock_sms, order):
        send_order_notification(order)
        assert mock_sms.called
        assert mock_email.called
  