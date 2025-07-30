<script>
    import SessionSetup from '../components/SessionSetup.svelte';
    import ProblemDisplay from '../components/ProblemDisplay.svelte';
    import ResultsSummary from '../components/ResultsSummary.svelte';
    import { gameState } from '../stores/gameStore.js';

    let currentView = 'setup'; // 'setup', 'practice', 'results'

    function handleStartSession() {
        currentView = 'practice';
    }

    function handleSessionComplete() {
        currentView = 'results';
    }

    function handleRestart() {
        currentView = 'setup';
        // Reset game state
        gameState.update(state => ({
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
        }));
    }
</script>

<main class="app">
    <div class="container">
        {#if currentView === 'setup'}
            <SessionSetup on:start={handleStartSession} />
        {:else if currentView === 'practice'}
            <ProblemDisplay on:complete={handleSessionComplete} />
        {:else if currentView === 'results'}
            <ResultsSummary on:restart={handleRestart} />
        {/if}
    </div>
</main>

<style>
    .app {
        min-height: 100vh;
        padding: 1rem;
        background: linear-gradient(135deg, var(--bg-color) 0%, var(--accent-color-one) 100%);
    }

    .container {
        max-width: 1200px;
        margin: 0 auto;
    }
</style>