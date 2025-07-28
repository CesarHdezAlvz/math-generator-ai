<script>
    import { createEventDispatcher, onMount } from 'svelte';
    import { gameState, studentInsights } from '../stores/gameStore.js';
    import { mathAPI } from '../lib/api.js';

    const dispatch = createEventDispatcher();
    
    let insights = null;
    let isLoading = true;

    onMount(async () => {
        try {
            insights = await mathAPI.getStudentInsights();
            studentInsights.set(insights);
        } catch (error) {
            console.error('Failed to load insights:', error);
        } finally {
            isLoading = false;
        }
    });

    function getAccuracyColor(accuracy) {
        if (accuracy >= 0.9) return '#28a745';
        if (accuracy >= 0.75) return '#ffc107';
        if (accuracy >= 0.6) return '#fd7e14';
        return '#dc3545';
    }

    function getMotivationalMessage(accuracy) {
        if (accuracy >= 0.9) return "🌟 Outstanding! You're a math superstar!";
        if (accuracy >= 0.75) return "👍 Great job! Keep up the excellent work!";
        if (accuracy >= 0.6) return "📚 Good effort! Practice makes perfect!";
        return "💪 Keep going! Every expert was once a beginner!";
    }

    async function startNewSession() {
        await mathAPI.resetSession();
        dispatch('restart');
    }

    function formatWeakAreas(weakAreas) {
        if (!weakAreas || Object.keys(weakAreas).length === 0) {
            return "No weak areas identified yet!";
        }
        
        const sorted = Object.entries(weakAreas)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 3);
        
        return sorted.map(([op, score]) => ({
            operation: op.charAt(0).toUpperCase() + op.slice(1),
            score: (score * 100).toFixed(0)
        }));
    }
</script>

<div class="results-container">
    <h1>📊 Session Complete!</h1>
    
    <div class="session-stats">
        <div class="stat-card main-stats">
            <h2>Your Performance</h2>
            <div class="big-stat">
                <div class="accuracy" style="color: {getAccuracyColor($gameState.sessionStats.total > 0 ? $gameState.sessionStats.correct / $gameState.sessionStats.total : 0)}">
                    {$gameState.sessionStats.total > 0 ? Math.round(($gameState.sessionStats.correct / $gameState.sessionStats.total) * 100) : 0}%
                </div>
                <div class="accuracy-label">Accuracy</div>
            </div>
            
            <div class="detailed-stats">
                <div class="stat-item">
                    <span class="stat-value correct">✅ {$gameState.sessionStats.correct}</span>
                    <span class="stat-label">Correct</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value incorrect">❌ {$gameState.sessionStats.incorrect}</span>
                    <span class="stat-label">Incorrect</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value total">📝 {$gameState.sessionStats.total}</span>
                    <span class="stat-label">Total</span>
                </div>
            </div>
        </div>
        
        <div class="motivation-card">
            <p class="motivation-message">
                {getMotivationalMessage($gameState.sessionStats.total > 0 ? $gameState.sessionStats.correct / $gameState.sessionStats.total : 0)}
            </p>
        </div>
    </div>

    {#if isLoading}
        <div class="loading">
            <div class="spinner"></div>
            <p>Analyzing your performance...</p>
        </div>
    {:else if insights && insights.total_problems_attempted > 0}
        <div class="ai-insights">
            <h2>🤖 AI Learning Insights</h2>
            
            <div class="insights-grid">
                <div class="insight-card">
                    <h3>Overall Progress</h3>
                    <p><strong>{insights.total_problems_attempted}</strong> total problems attempted</p>
                    <p><strong>{Math.round(insights.recent_accuracy * 100)}%</strong> recent accuracy</p>
                </div>
                
                {#if insights.weak_areas && Object.keys(insights.weak_areas).length > 0}
                    <div class="insight-card">
                        <h3>Areas to Focus On</h3>
                        {#each formatWeakAreas(insights.weak_areas) as area}
                            <div class="weak-area">
                                <span class="area-name">{area.operation}</span>
                                <div class="area-bar">
                                    <div class="area-fill" style="width: {area.score}%"></div>
                                </div>
                            </div>
                        {/each}
                    </div>
                {/if}
                
                {#if insights.most_common_mistakes && Object.keys(insights.most_common_mistakes).length > 0}
                    <div class="insight-card">
                        <h3>Common Mistake Patterns</h3>
                        {#each Object.entries(insights.most_common_mistakes).slice(0, 3) as [mistake, count]}
                            <div class="mistake-item">
                                <span class="mistake-type">{mistake.replace('_', ' ')}</span>
                                <span class="mistake-count">{count} times</span>
                            </div>
                        {/each}
                    </div>
                {/if}
                
                {#if insights.recommended_focus}
                    <div class="insight-card recommendation">
                        <h3>💡 AI Recommendation</h3>
                        <p>Focus on practicing <strong>{insights.recommended_focus}</strong> to improve your overall performance!</p>
                    </div>
                {/if}
            </div>
        </div>
    {/if}

    <div class="actions">
        <button class="primary-btn" on:click={startNewSession}>
            🔄 Start New Session
        </button>
    </div>
</div>

<style>
    .results-container {
        max-width: 800px;
        margin: 2rem auto;
        padding: 2rem;
        text-align: center;
    }

    h1 {
        font-size: 2.5rem;
        margin-bottom: 2rem;
        color: #2c3e50;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .session-stats {
        margin-bottom: 2rem;
    }

    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    .main-stats h2 {
        margin-bottom: 1.5rem;
        font-size: 1.8rem;
    }

    .big-stat {
        margin-bottom: 2rem;
    }

    .accuracy {
        font-size: 4rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .accuracy-label {
        font-size: 1.2rem;
        opacity: 0.9;
    }

    .detailed-stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
    }

    .stat-item {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .stat-value {
        font-size: 1.8rem;
        font-weight: bold;
    }

    .stat-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .motivation-card {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(40, 167, 69, 0.3);
    }

    .motivation-message {
        font-size: 1.3rem;
        font-weight: 500;
        margin: 0;
    }

    .loading {
        padding: 3rem;
        color: #6c757d;
    }

    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .ai-insights {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    }

    .ai-insights h2 {
        color: #2c3e50;
        margin-bottom: 1.5rem;
    }

    .insights-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
    }

    .insight-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 3px 15px rgba(0,0,0,0.1);
        text-align: left;
    }

    .insight-card h3 {
        color: #495057;
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }

    .weak-area {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.5rem;
    }

    .area-name {
        min-width: 100px;
        font-weight: 500;
    }

    .area-bar {
        flex: 1;
        height: 8px;
        background: #e9ecef;
        border-radius: 4px;
        overflow: hidden;
    }

    .area-fill {
        height: 100%;
        background: linear-gradient(90deg, #dc3545, #fd7e14);
        transition: width 0.3s ease;
    }

    .mistake-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #e9ecef;
    }

    .mistake-item:last-child {
        border-bottom: none;
    }

    .mistake-type {
        font-weight: 500;
        text-transform: capitalize;
    }

    .mistake-count {
        color: #6c757d;
        font-size: 0.9rem;
    }

    .recommendation {
        border: 2px solid #28a745;
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
    }

    .recommendation h3 {
        color: #155724;
    }

    .actions {
        margin-top: 2rem;
    }

    .primary-btn {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .primary-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    @media (max-width: 640px) {
        .results-container {
            margin: 1rem;
            padding: 1.5rem;
        }

        .detailed-stats {
            grid-template-columns: 1fr;
        }

        .insights-grid {
            grid-template-columns: 1fr;
        }

        .accuracy {
            font-size: 3rem;
        }
    }
</style>