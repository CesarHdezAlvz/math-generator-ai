// src/stores/gameStore.js - Game state management
import { writable } from 'svelte/store';

export const gameState = writable({
    currentProblem: null,
    problemIndex: 0,
    totalProblems: 0,
    problems: [],
    sessionStats: {
        correct: 0,
        incorrect: 0,
        total: 0
    },
    userAnswer: '',
    showFeedback: false,
    sessionComplete: false,
    isLoading: false,
    error: null
});

export const studentInsights = writable({
    total_problems_attempted: 0,
    recent_accuracy: 0,
    weak_areas: {},
    most_common_mistakes: {},
    recommended_focus: null
});