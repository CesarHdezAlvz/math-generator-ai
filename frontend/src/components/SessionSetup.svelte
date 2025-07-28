<script>
    import { createEventDispatcher } from 'svelte';
    import { mathAPI } from '../lib/api.js';
    import { gameState } from '../stores/gameStore.js';

    const dispatch = createEventDispatcher();
    
    let selectedOperations = [];
    let problemCount = 10;
    let isGenerating = false;

    const operations = [
        { id: 'addition', label: 'Addition (+)', icon: '➕' },
        { id: 'subtraction', label: 'Subtraction (-)', icon: '➖' },
        { id: 'multiplication', label: 'Multiplication (×)', icon: '✖️' },
        { id: 'division', label: 'Division (÷)', icon: '➗' }
    ];

    function toggleOperation(operationId) {
        if (selectedOperations.includes(operationId)) {
            selectedOperations = selectedOperations.filter(op => op !== operationId);
        } else {
            selectedOperations = [...selectedOperations, operationId];
        }
    }

    async function startSession() {
        if (selectedOperations.length === 0) {
            alert('Please select at least one operation!');
            return;
        }

        isGenerating = true;
        gameState.update(state => ({ ...state, isLoading: true, error: null }));

        try {
            const problems = await mathAPI.generateProblems(selectedOperations, problemCount);
            
            gameState.update(state => ({
                ...state,
                problems,
                totalProblems: problemCount,
                currentProblem: problems[0],
                problemIndex: 0,
                isLoading: false,
                sessionStats: { correct: 0, incorrect: 0, total: 0 },
                showFeedback: false,
                sessionComplete: false
            }));

            dispatch('start');
        } catch (error) {
            gameState.update(state => ({ 
                ...state, 
                isLoading: false, 
                error: 'Failed to generate problems. Please try again.' 
            }));
        } finally {
            isGenerating = false;
        }
    }
</script>

<div class="setup-container">
    <h1>🧮 Math Practice</h1>
    <p>Choose your operations and get ready to practice!</p>
    
    <div class="section">
        <h2>Select Operations</h2>
        <div class="operations-grid">
            {#each operations as operation}
                <button 
                    class="operation-btn"
                    class:selected={selectedOperations.includes(operation.id)}
                    on:click={() => toggleOperation(operation.id)}
                >
                    <span class="icon">{operation.icon}</span>
                    <span class="label">{operation.label}</span>
                </button>
            {/each}
        </div>
    </div>

    <div class="section">
        <h2>Number of Problems</h2>
        <input 
            type="range" 
            min="5" 
            max="50" 
            bind:value={problemCount}
            class="slider"
        />
        <div class="count-display">{problemCount} problems</div>
    </div>

    <button 
        class="start-btn"
        on:click={startSession}
        disabled={isGenerating || selectedOperations.length === 0}
    >
        {#if isGenerating}
            Generating Problems...
        {:else}
            Start Practice Session
        {/if}
    </button>

    {#if $gameState.error}
        <div class="error">
            {$gameState.error}
        </div>
    {/if}
</div>

<style>
    .setup-container {
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .section {
        margin: 2rem 0;
    }

    .section h2 {
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }

    .operations-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin: 1rem 0;
    }

    .operation-btn {
        padding: 1rem;
        border: 2px solid rgba(255,255,255,0.3);
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        color: white;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }

    .operation-btn:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-2px);
    }

    .operation-btn.selected {
        background: rgba(255,255,255,0.3);
        border-color: white;
        box-shadow: 0 4px 15px rgba(255,255,255,0.2);
    }

    .icon {
        font-size: 2rem;
    }

    .label {
        font-size: 0.9rem;
        font-weight: 500;
    }

    .slider {
        width: 100%;
        margin: 1rem 0;
    }

    .count-display {
        font-size: 1.2rem;
        font-weight: bold;
        margin-top: 0.5rem;
    }

    .start-btn {
        background: #28a745;
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }

    .start-btn:hover:not(:disabled) {
        background: #218838;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
    }

    .start-btn:disabled {
        background: #6c757d;
        cursor: not-allowed;
        box-shadow: none;
    }

    .error {
        background: rgba(220, 53, 69, 0.9);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }

    @media (max-width: 640px) {
        .operations-grid {
            grid-template-columns: 1fr;
        }
        
        .setup-container {
            margin: 1rem;
            padding: 1.5rem;
        }
    }
</style>