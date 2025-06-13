import { API_URL } from "../models/newsModel";

export async function getAuthorName(authorId: number): Promise<any> {
    try {
        const response = await fetch(`${API_URL}users/${authorId}`, {
            method: 'GET'
        });
        const data = await response.json();
        return data.username;
    } catch (error) {
        console.error('Error fetching author name:', error);
        return undefined;
    }
}