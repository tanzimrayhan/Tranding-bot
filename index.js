const axios = require('axios');
const qs = require('qs');

// Replace these with your actual credentials
const clientId = process.env.APP_KEY
const clientSecret = process.env.CLIENT_SECRET
const redirectUri = `https://api.schwabapi.com/v1/oauth/authorize?response_type=code&client_id=${clientId}&scope=readonly&redirect_uri=${redirectUri}`;
const authCode = 'YOUR_AUTH_CODE'; // This is obtained from the OAuth 2.0 authorization flow

// Function to get the access token
async function getAccessToken() {
  const tokenUrl = 'https://api-schwab.com/oauth2/token';
  const tokenData = {
    grant_type: 'authorization_code',
    code: authCode,
    redirect_uri: redirectUri,
    client_id: clientId,
    client_secret: clientSecret,
  };

  try {
    const response = await axios.post(tokenUrl, qs.stringify(tokenData), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data.access_token;
  } catch (error) {
    console.error('Error getting access token:', error);
    throw error;
  }
}

// Function to make an API request
async function makeApiRequest(accessToken) {
  const apiUrl = 'https://api-schwab.com/v1/accounts';
  
  try {
    const response = await axios.get(apiUrl, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    });
    console.log('API response:', response.data);
  } catch (error) {
    console.error('Error making API request:', error);
  }
}

// Main function to connect to the API and make a request
async function connectToSchwabApi() {
  try {
    const accessToken = await getAccessToken();
    await makeApiRequest(accessToken);
  } catch (error) {
    console.error('Error connecting to Schwab API:', error);
  }
}

// Call the main function
connectToSchwabApi();