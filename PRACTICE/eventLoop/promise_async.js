// 1. Promises: The Solution to "Callback Hell"

const { error } = require("console");
const { readFile } = require("fs");

// The old way:
readFile("../resources/file.txt", (error, data) => { /* call back function here */ })

// The new way:
readFile("../resources/file.txt")
    .then((data) => {
        console.log("Do stuff here!")
    })
    .catch((err) => {
        console.log("The error that could possibly appear!")
    })


// 2. Async/Await: Promises Made Easy

async function loadUserData() {
    try {
        // 1. Await pauses here until API call resolves
        const userResponse = await fetch('/api/user');
        const user = await userResponse.json();

        // 2. This would only run after the first await is handled
        const postResponses = await fetch(`/api/posts/${user.id}`);
        const posts = await postResponses.json();

        console.log(`user Posts: ${posts}`);

    } catch(error) {
        // Error handling for any failed Promise in the chain
        console.error('Failed to load data:', error);
    }
}

// 3. Axios Fetching
import axios from 'axios';
import { create } from 'domain';
axios.get('https://api.example.com/users')
    .then((response) => {
        // upon succefful execution of the axios and await library
        // this will run
        console.log("User Data", response.data);
    })
    .catch((error) => {
        // catch the error and print it here
        console.error("Failed to load data:", error);
    })

// 4. Modern Aync & Await
async function fetchUsers() {
    try {
        const response = await axios.get("https://api.example.com/users");

        const users = response.data;
        console.log("User Data: ", users);
    } catch(error) {
        console.error("Failed to load data", error.message);
    }
}

fetchUsers();

// Axios POST Request
async function createUser(name, email) {
    const newUser = {
        name: name,
        email: email,
    };

    try {
        const response = await axios.post("https://api.example.com/users",  newUser);

        // The server typically responds with the newly created resource, often with an ID
        console.log("New User created: ", response.data);
        console.log("Status Code: ", response.status); // usually 201 for created.
    } catch(error) {
        console.error("Error creating user: ", error.message);
    }
}

createUser('Alex Johnson', 'alexjames@gamil.com');

// Authenticated headers with Axios
async function getProtectedData(token) {
    const config = {
        // Configuration object
        headers: {
            // Authorization header for protected endpoints
            'Authorization': `Bearer ${token}` 
        },
        // Query parameters are passed in a 'params' object
        params: {
            limit: 10,
            sort: 'date'
        },
        timeout: 5000 // Timeout after 5 seconds
    };
  
    try {
        const response = await axios.get('https://api.example.com/protected/posts', config);
        console.log('Protected Posts:', response.data);
    } catch (error) {
        console.error('Authentication or Fetch Error:', error);
    }
}

// DRY code
// 1. create a custom instance
const api = axios.create({
    baseURL: 'https://api.myapp.com/v1', // All requests use this base URL
    timeout: 5000,
    headers: {
        "Content-Type" :'application/json',
        "X-Custom-Header": 'Axios App'
    }
});

// Interceptors -- perfect way to insert auth headers or tokens.

// Request Interceptors
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("authToken");

        if(token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    }, 
    (error) => {
        return Promise.reject(error);
    }
)

// Response Interceptors
api.interceptors.response.use(
    (response) => { return response },
    (error) => {
        if (error.response.status == 401) {
            console.error("Unauthorized! Redirecting to login...");
        }
        return Promise.reject(error);
    }
);

// function getProfile with custom instance
async function getProfile(userId) {
    try {
        const response = await api.get(`/user/${userId}`);
        return response.data;
    } catch(error) {
        if (error.message) {
            console.error("Error fetchign user data: ", error.response.status);
        } else {
            console.error("Network or timeout error: ", error.message);
        }
        throw error;
    }
}

// example usage:
// const profile = await getProfile(42);