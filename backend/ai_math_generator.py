# ai_math_generator.py - AI logic
import random
import json
from typing import List, Dict, Tuple
from collections import defaultdict

class StudentPerformanceTracker:
    """Tracks student performance and builds learning profile"""
    
    def __init__(self):
        self.performance_history = []
        self.mistake_patterns = defaultdict(list)
        self.difficulty_feedback = defaultdict(list)
    
    def record_attempt(self, problem: Dict, user_answer: int, time_taken: float):
        """Record a student's attempt on a problem"""
        is_correct = user_answer == problem['answer']
        
        attempt = {
            'problem': problem,
            'user_answer': user_answer,
            'correct_answer': problem['answer'],
            'is_correct': is_correct,
            'time_taken': time_taken,
            'operation': problem['operation'],
            'difficulty': problem['difficulty']
        }
        
        self.performance_history.append(attempt)
        
        # Track difficulty feedback
        self.difficulty_feedback[problem['operation']].append({
            'assigned_difficulty': problem['difficulty'],
            'was_correct': is_correct,
            'time_taken': time_taken
        })
        
        # Track mistake patterns if incorrect
        if not is_correct:
            self._analyze_mistake(problem, user_answer)
    
    def _analyze_mistake(self, problem: Dict, user_answer: int):
        """Analyze the type of mistake made"""
        operation = problem['operation']
        correct_answer = problem['answer']
        
        mistake_info = {
            'problem_text': problem['problem'],
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'mistake_type': self._classify_mistake(problem, user_answer)
        }
        
        self.mistake_patterns[operation].append(mistake_info)
    
    def _classify_mistake(self, problem: Dict, user_answer: int) -> str:
        """Simple mistake classification"""
        operation = problem['operation']
        correct = problem['answer']
        
        if operation == 'addition':
            # Check if they subtracted instead
            if ' + ' in problem['problem']:
                parts = problem['problem'].split(' + ')
                a, b = int(parts[0]), int(parts[1])
                if user_answer == abs(a - b):
                    return 'wrong_operation_subtraction'
        
        elif operation == 'subtraction':
            # Check if they added instead
            if ' - ' in problem['problem']:
                parts = problem['problem'].split(' - ')
                a, b = int(parts[0]), int(parts[1])
                if user_answer == a + b:
                    return 'wrong_operation_addition'
        
        elif operation == 'multiplication':
            # Check if they added instead
            if ' × ' in problem['problem']:
                parts = problem['problem'].split(' × ')
                a, b = int(parts[0]), int(parts[1])
                if user_answer == a + b:
                    return 'wrong_operation_addition'
        
        # Check if answer is close (off by 1-2, might be calculation error)
        if abs(user_answer - correct) <= 2:
            return 'calculation_error'
        
        return 'conceptual_error'
    
    def get_weak_areas(self) -> Dict[str, float]:
        """Identify operations where student struggles most"""
        weak_areas = {}
        
        for operation in ['addition', 'subtraction', 'multiplication', 'division']:
            attempts = [a for a in self.performance_history if a['operation'] == operation]
            if attempts:
                accuracy = sum(1 for a in attempts if a['is_correct']) / len(attempts)
                weak_areas[operation] = 1 - accuracy  # Higher value = weaker area
        
        return weak_areas
    
    def predict_difficulty(self, operation: str, base_difficulty: int) -> int:
        """Predict appropriate difficulty based on past performance"""
        feedback = self.difficulty_feedback[operation]
        
        if len(feedback) < 3:  # Not enough data
            return base_difficulty
        
        # Recent performance (last 5 attempts)
        recent_feedback = feedback[-5:]
        recent_accuracy = sum(1 for f in recent_feedback if f['was_correct']) / len(recent_feedback)
        avg_time = sum(f['time_taken'] for f in recent_feedback) / len(recent_feedback)
        
        # Adjust difficulty based on performance
        if recent_accuracy > 0.8 and avg_time < 10:  # Too easy
            return min(base_difficulty + 1, 6)
        elif recent_accuracy < 0.5 or avg_time > 30:  # Too hard
            return max(base_difficulty - 1, 1)
        else:
            return base_difficulty

class MathGenerator:
    def __init__(self):
        self.ranges = {
            'addition': (1, 100),
            'subtraction': (1, 100),
            'multiplication': (1, 12),
            'division': (1, 144)
        }
    
    def calculate_addition_difficulty(self, a: int, b: int) -> int:
        """Calculate difficulty score for addition problems"""
        difficulty = 1
        
        if max(a, b) > 50:
            difficulty += 2
        elif max(a, b) > 20:
            difficulty += 1
        
        # Check for carrying
        units_sum = (a % 10) + (b % 10)
        tens_sum = (a // 10) + (b // 10)
        
        if units_sum >= 10:
            difficulty += 2
        if tens_sum >= 10:
            difficulty += 1
        
        return difficulty
    
    def calculate_subtraction_difficulty(self, a: int, b: int) -> int:
        """Calculate difficulty score for subtraction problems"""
        difficulty = 1
        
        if a > 50:
            difficulty += 2
        elif a > 20:
            difficulty += 1
        
        # Check for borrowing
        if (a % 10) < (b % 10):
            difficulty += 3
        if a < b * 10:
            difficulty += 1
        
        return difficulty
    
    def calculate_multiplication_difficulty(self, a: int, b: int) -> int:
        """Calculate difficulty score for multiplication problems"""
        difficulty = 1
        
        if a in [2, 5, 10] or b in [2, 5, 10]:
            difficulty += 0
        elif max(a, b) <= 9:
            difficulty += 2
        elif max(a, b) > 10:
            difficulty += 4
        
        if a > 10 or b > 10:
            difficulty += 2
        
        return difficulty
    
    def calculate_division_difficulty(self, dividend: int, divisor: int) -> int:
        """Calculate difficulty score for division problems"""
        difficulty = 1
        quotient = dividend // divisor
        
        if divisor <= 5:
            difficulty += 1
        elif divisor <= 10:
            difficulty += 2
        else:
            difficulty += 3
        
        if quotient > 10:
            difficulty += 2
        elif quotient > 5:
            difficulty += 1
        
        return difficulty
    
    def generate_addition(self) -> Dict:
        min_val, max_val = self.ranges['addition']
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        difficulty = self.calculate_addition_difficulty(a, b)
        
        return {
            'problem': f"{a} + {b}",
            'answer': a + b,
            'operation': 'addition',
            'difficulty': difficulty
        }
    
    def generate_subtraction(self) -> Dict:
        min_val, max_val = self.ranges['subtraction']
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, a)
        difficulty = self.calculate_subtraction_difficulty(a, b)
        
        return {
            'problem': f"{a} - {b}",
            'answer': a - b,
            'operation': 'subtraction',
            'difficulty': difficulty
        }
    
    def generate_multiplication(self) -> Dict:
        min_val, max_val = self.ranges['multiplication']
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        difficulty = self.calculate_multiplication_difficulty(a, b)
        
        return {
            'problem': f"{a} × {b}",
            'answer': a * b,
            'operation': 'multiplication',
            'difficulty': difficulty
        }
    
    def generate_division(self) -> Dict:
        divisor = random.randint(2, 12)
        quotient = random.randint(2, 12)
        dividend = divisor * quotient
        difficulty = self.calculate_division_difficulty(dividend, divisor)
        
        return {
            'problem': f"{dividend} ÷ {divisor}",
            'answer': quotient,
            'operation': 'division',
            'difficulty': difficulty
        }
    
    def generate_problems(self, operations: List[str], count: int) -> List[Dict]:
        problems = []
        generators = {
            'addition': self.generate_addition,
            'subtraction': self.generate_subtraction,
            'multiplication': self.generate_multiplication,
            'division': self.generate_division
        }
        
        for _ in range(count):
            operation = random.choice(operations)
            problem = generators[operation]()
            problems.append(problem)
        return problems

class AIEnhancedMathGenerator:
    """Math generator with AI-based difficulty adaptation and mistake targeting"""
    
    def __init__(self):
        self.base_generator = MathGenerator()
        self.performance_tracker = StudentPerformanceTracker()
    
    def generate_adaptive_problems(self, operations: List[str], count: int) -> List[Dict]:
        """Generate problems adapted to student's performance"""
        weak_areas = self.performance_tracker.get_weak_areas()
        weighted_operations = self._weight_operations(operations, weak_areas)
        
        problems = []
        for _ in range(count):
            operation = self._choose_weighted_operation(weighted_operations)
            
            if operation == 'addition':
                problem = self.base_generator.generate_addition()
            elif operation == 'subtraction':
                problem = self.base_generator.generate_subtraction()
            elif operation == 'multiplication':
                problem = self.base_generator.generate_multiplication()
            else:
                problem = self.base_generator.generate_division()
            
            # Adapt difficulty based on student's performance
            adapted_difficulty = self.performance_tracker.predict_difficulty(
                operation, problem['difficulty']
            )
            problem['difficulty'] = adapted_difficulty
            problem['ai_adapted'] = True
            
            problems.append(problem)
        
        return sorted(problems, key=lambda x: x['difficulty'])
    
    def _weight_operations(self, operations: List[str], weak_areas: Dict[str, float]) -> Dict[str, float]:
        weights = {}
        for op in operations:
            weakness_score = weak_areas.get(op, 0)
            weights[op] = 1 + (weakness_score * 2)
        return weights
    
    def _choose_weighted_operation(self, weights: Dict[str, float]) -> str:
        operations = list(weights.keys())
        weight_values = list(weights.values())
        total_weight = sum(weight_values)
        
        # Simple weighted random selection
        r = random.random() * total_weight
        cumulative = 0
        for op, weight in zip(operations, weight_values):
            cumulative += weight
            if r <= cumulative:
                return op
        return operations[-1]  # Fallback
    
    def record_student_attempt(self, problem: Dict, user_answer: int, time_taken: float):
        """Record student's attempt for learning"""
        self.performance_tracker.record_attempt(problem, user_answer, time_taken)
    
    def get_student_insights(self) -> Dict:
        """Get insights about student's learning"""
        weak_areas = self.performance_tracker.get_weak_areas()
        total_attempts = len(self.performance_tracker.performance_history)
        
        if total_attempts == 0:
            return {"message": "No data yet", "total_problems_attempted": 0}
        
        recent_attempts = self.performance_tracker.performance_history[-10:]
        recent_accuracy = sum(1 for a in recent_attempts if a['is_correct']) / len(recent_attempts)
        
        mistake_counts = defaultdict(int)
        for operation_mistakes in self.performance_tracker.mistake_patterns.values():
            for mistake in operation_mistakes:
                mistake_counts[mistake['mistake_type']] += 1
        
        return {
            'total_problems_attempted': total_attempts,
            'recent_accuracy': recent_accuracy,
            'weak_areas': weak_areas,
            'most_common_mistakes': dict(mistake_counts),
            'recommended_focus': max(weak_areas.items(), key=lambda x: x[1])[0] if weak_areas else None
        }