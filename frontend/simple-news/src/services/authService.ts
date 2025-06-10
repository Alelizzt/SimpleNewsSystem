import router from "../router";
import { useAuthStore } from "../stores/authStore";



const API_URL = 'http://127.0.0.1:8000/v1/login/';


export async function login(username: string, password: string): Promise<any> {
    try {
        const auth = useAuthStore();

        const body = new URLSearchParams({
            username,
            password
        }).toString();

        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: body,
        });

        if (!response.ok) {
            throw new Error('Login failed with status: ' + response.status);
        }

        const data = await response.json();
        if (response.ok && data.access_token) {
            auth.setToken(data.access_token); // Store the token in the Pinia store
        }
        return data;
    } catch (error) {
        console.error('Error during login:', error);
        throw error; // Propagate the error to be handled by the caller
    }
}

export async function logout() {
    try {
        const auth = useAuthStore();
        auth.clearToken(); // Clear the token from the Pinia store
        router.push({ name: 'Login' });
        return Promise.resolve(); // Return a resolved promise to indicate successful logout
    } catch (error) {
        console.error('Error during logout:', error);
        throw error; // Propagate the error to be handled by the caller
    }
}

export function getCurrentUser(): string | null {
    const auth = useAuthStore();

    return auth.token; // Return the token from the Pinia store
}
