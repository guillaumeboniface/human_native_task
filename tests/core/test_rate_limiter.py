import pytest
from fastapi import HTTPException
from app.core.rate_limiter import RateLimiter, rate_limit_middleware
from unittest.mock import Mock, patch
import time

@pytest.fixture
def rate_limiter():
    return RateLimiter(requests_per_minute=3)  # Using a small number for testing

def test_rate_limiter_below_limit(rate_limiter):
    client_id = "test_client"
    
    # Make 3 requests (at limit)
    assert not rate_limiter.is_rate_limited(client_id)
    assert not rate_limiter.is_rate_limited(client_id)
    assert not rate_limiter.is_rate_limited(client_id)
    
    # Fourth request should be rate limited
    assert rate_limiter.is_rate_limited(client_id)

def test_rate_limiter_different_clients(rate_limiter):
    client1 = "client1"
    client2 = "client2"
    
    # Each client should have their own limit
    assert not rate_limiter.is_rate_limited(client1)
    assert not rate_limiter.is_rate_limited(client1)
    assert not rate_limiter.is_rate_limited(client1)
    assert rate_limiter.is_rate_limited(client1)
    
    # Client 2 should still be able to make requests
    assert not rate_limiter.is_rate_limited(client2)
    assert not rate_limiter.is_rate_limited(client2)
    assert not rate_limiter.is_rate_limited(client2)

def test_rate_limiter_window_sliding():
    limiter = RateLimiter(requests_per_minute=2)
    client_id = "test_client"
    
    # Make two requests
    assert not limiter.is_rate_limited(client_id)
    assert not limiter.is_rate_limited(client_id)
    assert limiter.is_rate_limited(client_id)
    
    # Wait for 61 seconds (requests should expire)
    current_time = time.time()
    with patch('time.time') as mock_time:
        # Set the mock to return a time 61 seconds in the future
        mock_time.return_value = current_time + 61
        # Should be able to make requests again
        assert not limiter.is_rate_limited(client_id)
        assert not limiter.is_rate_limited(client_id)
        assert limiter.is_rate_limited(client_id)

@pytest.mark.asyncio
async def test_rate_limit_middleware():
    # Create a mock request
    mock_request = Mock()
    mock_request.headers = {"X-API-Key": "test_key"}
    mock_request.client.host = "127.0.0.1"
    
    # Create an async mock call_next function
    async def mock_call_next(request):
        return "response"
    
    # Test with API key
    with patch('app.core.rate_limiter.rate_limiter') as mock_limiter:
        mock_limiter.is_rate_limited.return_value = False
        response = await rate_limit_middleware(mock_request, mock_call_next)  # Should not raise exception
        assert response == "response"
        
        mock_limiter.is_rate_limited.return_value = True
        with pytest.raises(HTTPException) as exc_info:
            await rate_limit_middleware(mock_request, mock_call_next)
        assert exc_info.value.status_code == 429
