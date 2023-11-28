import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { makeApiRequest } from './apiUtils';

function AdminSupportPage() {
    const testRequest = async () => {
        let apiUrl = 'http://localhost:3500/api/message_broker';
        let bodyParams = { 
            "data": {
                email: sessionStorage.getItem('email')
            },
            "topic": "request.notifications.test"
        };
        const apiResponse = await makeApiRequest('POST', apiUrl, bodyParams)
        if (apiResponse.success) {
            console.log(apiResponse.data)
        }
    };

    return (
        <div>
            <h1>Welcome to the Support page!</h1>
            <button key="blahblah" onClick={testRequest}>Login</button>
        </div>
    )
}

export default AdminSupportPage;