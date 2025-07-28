// src/lib/api.js - API client
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const mathAPI = {
    async generateProblems(operations, count) {
        try {
            const response = await api.post('/generate-problems', {
                operations,
                count
            });
            return response.data;
        } catch (error) {
            console.error('Error generating problems:', error);
            throw error;
        }
    },

    async recordAttempt(problem, userAnswer, timeSpent) {
        try {
            const response = await api.post('/record-attempt', {
                problem,
                user_answer: userAnswer,
                time_taken: timeSpent
            });
            return response.data;
        } catch (error) {
            console.error('Error recording attempt:', error);
            throw error;
        }
    },

    async getStudentInsights() {
        try {
            const response = await api.get('/student-insights');
            return response.data;
        } catch (error) {
            console.error('Error getting insights:', error);
            throw error;
        }
    },

    async resetSession() {
        try {
            const response = await api.post('/reset-session');
            return response.data;
        } catch (error) {
            console.error('Error resetting session:', error);
            throw error;
        }
    }
};