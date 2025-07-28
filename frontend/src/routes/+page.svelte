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
    :global(body) {
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .app {
        min-height: 100vh;
        padding: 1rem;
    }

    .container {
        max-width: 1200px;
        margin: 0 auto;
    }

    :global(*) {
        box-sizing: border-box;
    }

    :global(h1, h2, h3) {
        margin-top: 0;
    }

    :global(button) {
        font-family: inherit;
    }

    :global(input) {
        font-family: inherit;
    }
</style>