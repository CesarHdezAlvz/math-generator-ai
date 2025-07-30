<script>
    import { createEventDispatcher, onMount } from 'svelte';
    import { gameState } from '../stores/gameStore.js';
    import { mathAPI } from '../lib/api.js';

    const dispatch = createEventDispatcher();
    
    let userAnswer = '';
    let startTime = Date.now();
    let showFeedback = false;
    let isCorrect = false;
    let isSubmitting = false;

    $: if ($gameState.currentProblem && !showFeedback) {
        startTime = Date.now();
        userAnswer = '';
    }

    async function submitAnswer() {
        if (userAnswer === '' || isSubmitting) return;
        
        isSubmitting = true;
        const timeSpent = (Date.now() - startTime) / 1000;
        const answer = parseInt(userAnswer);
        isCorrect = answer === $gameState.currentProblem.answer;
        showFeedback = true;

        // Record attempt with backend
        try {
            await mathAPI.recordAttempt($gameState.currentProblem, answer, timeSpent);
        } catch (error) {
            console.error('Failed to record attempt:', error);
        }

        // Update local state
        gameState.update(state => {
            const newStats = {
                ...state.sessionStats,
                total: state.sessionStats.total + 1,
                correct: state.sessionStats.correct + (isCorrect ? 1 : 0),
                incorrect: state.sessionStats.incorrect + (isCorrect ? 0 : 1)
            };
            
            return {
                ...state,
                sessionStats: newStats
            };
        });

        isSubmitting = false;
        dispatch('answer', { answer, timeSpent, isCorrect });
    }

    function handleKeyPress(event) {
        if (event.key === 'Enter') {
            if (showFeedback) {
                nextProblem();
            } else {
                submitAnswer();
            }
        }
    }

    function nextProblem() {
        const nextIndex = $gameState.problemIndex + 1;
        
        if (nextIndex >= $gameState.totalProblems) {
            dispatch('complete');
            return;
        }

        gameState.update(state => ({
            ...state,
            problemIndex: nextIndex,
            currentProblem: state.problems[nextIndex]
        }));

        showFeedback = false;
        userAnswer = '';
    }

    onMount(() => {
        // Focus on input when component mounts
        setTimeout(() => {
            const input = document.querySelector('input[type="number"]');
            if (input) input.focus();
        }, 100);
    });
</script>

<div class="problem-container">
    {#if $gameState.currentProblem}
        <div class="header">
            <div class="progress">
                Problem {$gameState.problemIndex + 1} of {$gameState.totalProblems}
            </div>
            <div class="stats">
                ✅ {$gameState.sessionStats.correct} | ❌ {$gameState.sessionStats.incorrect}
            </div>
        </div>
        
        <div class="difficulty">
            Difficulty: {'⭐'.repeat($gameState.currentProblem.difficulty)}
            {#if $gameState.currentProblem.ai_adapted}
                <span class="ai-badge">🤖 AI Adapted</span>
            {/if}
        </div>
        
        <div class="problem">
            <h2>{$gameState.currentProblem.problem} = ?</h2>
        </div>
        
        {#if !showFeedback}
            <div class="input-section">
                <input 
                    type="number" 
                    bind:value={userAnswer} 
                    on:keypress={handleKeyPress}
                    placeholder="Your answer"
                    disabled={isSubmitting}
                />
                <button 
                    on:click={submitAnswer} 
                    disabled={userAnswer === '' || isSubmitting}
                    class="submit-btn"
                >
                    {#if isSubmitting}
                        Submitting...
                    {:else}
                        Submit
                    {/if}
                </button>
            </div>
            
            <div class="hint">
                Press Enter to submit your answer
            </div>
        {:else}
            <div class="feedback {isCorrect ? 'correct' : 'incorrect'}">
                {#if isCorrect}
                    <div class="feedback-icon">🎉</div>
                    <p class="feedback-text">Excellent! You got it right!</p>
                {:else}
                    <div class="feedback-icon">💡</div>
                    <p class="feedback-text">
                        Not quite. The correct answer is <strong>{$gameState.currentProblem.answer}</strong>
                    </p>
                {/if}
                
                <button on:click={nextProblem} class="next-btn">
                    {$gameState.problemIndex + 1 >= $gameState.totalProblems ? 'View Results' : 'Next Problem'}
                    <span class="arrow">→</span>
                </button>
            </div>
            
            <div class="continue-hint">
                Press Enter to continue
            </div>
        {/if}
    {/if}
</div>

<style>
    .problem-container {
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding: 0 1rem;
    }
    
    .progress {
        font-size: 1.1rem;
        color: #6c757d;
        font-weight: 500;
    }
    
    .stats {
        font-size: 1.1rem;
        color: #495057;
        font-weight: 500;
    }
    
    .difficulty {
        font-size: 1rem;
        margin-bottom: 2rem;
        color: #6c757d;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }
    
    .ai-badge {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .problem h2 {
        font-size: 3rem;
        margin: 2rem 0;
        color: #2c3e50;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        font-weight: 700;
    }
    
    .input-section {
        margin: 2rem 0;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .input-section input {
        font-size: 1.8rem;
        padding: 1rem;
        border: 3px solid #e9ecef;
        border-radius: 12px;
        width: 200px;
        text-align: center;
        transition: all 0.3s ease;
        background: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .input-section input:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
    
    .input-section input:disabled {
        background: #f8f9fa;
        cursor: not-allowed;
    }
    
    .submit-btn {
        font-size: 1.3rem;
        padding: 1rem 2rem;
        background: linear-gradient(45deg, var(--accent-color-two) 0%, var(--accent-color-two) 100%);
        color: var(--accent-color-three);
        border: none;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    
    .submit-btn:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
    }
    
    .submit-btn:disabled {
        background: #6c757d;
        cursor: not-allowed;
        box-shadow: none;
        transform: none;
    }
    
    .hint {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 1rem;
        font-style: italic;
    }
    
    .feedback {
        margin: 2rem 0;
        padding: 2rem;
        border-radius: 15px;
        animation: slideIn 0.5s ease-out;
    }
    
    .feedback.correct {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        color: #155724;
        border: 2px solid #b8dabd;
    }
    
    .feedback.incorrect {
        background: linear-gradient(135deg, #f8d7da, #f1aeb5);
        color: #721c24;
        border: 2px solid #f1aeb5;
    }
    
    .feedback-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feedback-text {
        font-size: 1.3rem;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    
    .next-btn {
        font-size: 1.2rem;
        padding: 1rem 2rem;
        background: linear-gradient(45deg, var(--accent-color-two) 0%, var(--accent-color-two) 100%);
        color: var(--accent-color-three);
        border: none;
        border-radius: 12px;
        cursor: pointer;
        margin-top: 1rem;
        transition: all 0.3s ease;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        justify-content: center;
        margin: 1rem auto 0;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
    }
    
    .next-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 123, 255, 0.4);
    }
    
    .arrow {
        transition: transform 0.3s ease;
    }
    
    .next-btn:hover .arrow {
        transform: translateX(4px);
    }
    
    .continue-hint {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 1rem;
        font-style: italic;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @media (max-width: 640px) {
        .problem-container {
            margin: 1rem;
            padding: 1.5rem;
        }
        
        .problem h2 {
            font-size: 2.5rem;
        }
        
        .input-section {
            flex-direction: column;
        }
        
        .input-section input {
            width: 100%;
            max-width: 250px;
        }
        
        .header {
            flex-direction: column;
            gap: 0.5rem;
        }
    }
</style>