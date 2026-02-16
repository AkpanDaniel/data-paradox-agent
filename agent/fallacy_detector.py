import json
from pathlib import Path
from typing import Dict, List
from input_processor import InputProcessor

class FallacyDetector:
    """
    Matches processed claims against fallacy patterns.
    Returns detected fallacies with their associated challenges.
    """
    
    def __init__(self):
        self.processor = InputProcessor()
        self.fallacies = self._load_fallacies()
    
    def _load_fallacies(self) -> Dict:
        """Load the fallacy database from JSON."""
        fallacy_path = Path(__file__).parent.parent / 'config' / 'fallacies.json'
        with open(fallacy_path, 'r') as f:
            return json.load(f)
    
    def detect(self, claim_text: str) -> List[Dict]:
        """
        Analyze claim and detect potential fallacies.
        
        Args:
            claim_text: The user's analytical claim
            
        Returns:
            List of detected fallacies with confidence scores
        """
        # Process the claim first
        processed = self.processor.process(claim_text)
        
        # Check for signs of good methodology (reduce false positives)
        good_signals = self._check_good_methodology(claim_text.lower())
        
        detected = []
        
        # Check each fallacy for pattern matches
        for fallacy_id, fallacy_data in self.fallacies.items():
            match_score = self._calculate_match_score(processed, fallacy_data)
            
            # Reduce score if good methodology signals present
            if good_signals['has_controlled_experiment']:
                match_score = max(0, match_score - 5)  # Reduce by 5 points
            if good_signals['has_statistical_test']:
                match_score = max(0, match_score - 3)  # Reduce by 3 points
            if good_signals['has_large_sample']:
                match_score = max(0, match_score - 2)  # Reduce by 2 points
            
            if match_score > 0:
                detected.append({
                    'fallacy_id': fallacy_id,
                    'fallacy_name': fallacy_data['name'],
                    'description': fallacy_data['description'],
                    'confidence': self._score_to_confidence(match_score),
                    'match_score': match_score,
                    'challenges': fallacy_data['challenges']
                })
        
        # Sort by confidence (highest first)
        detected.sort(key=lambda x: x['match_score'], reverse=True)
        
        return detected
    
    def _check_good_methodology(self, text: str) -> Dict:
        """Check for signs of proper analytical methodology."""
        import re
        
        good_signals = {
            'has_controlled_experiment': False,
            'has_statistical_test': False,
            'has_large_sample': False
        }
        
        # Check for controlled experiments
        experiment_keywords = [
            'a/b test', 'controlled test', 'randomized', 'control group',
            'experiment', 'holdout', 'split test', '50/50', '50-50'
        ]
        good_signals['has_controlled_experiment'] = any(
            keyword in text for keyword in experiment_keywords
        )
        
        # Check for statistical significance testing
        stats_keywords = [
            'p-value', 'p value', 'statistical significance', 'confidence interval',
            'statistically significant', 't-test', 'chi-square', 'regression'
        ]
        good_signals['has_statistical_test'] = any(
            keyword in text for keyword in stats_keywords
        )
        
        # Check for large sample sizes
        sample_patterns = [
            r'\d+,?\d+\s+(users|conversions|samples|participants|respondents)',
            r'sample size.*\d+,?\d+',
            r'\d+k\+?\s+(users|conversions)'
        ]
        good_signals['has_large_sample'] = any(
            re.search(pattern, text) for pattern in sample_patterns
        )
        
        return good_signals
    
    def _calculate_match_score(self, processed: Dict, fallacy_data: Dict) -> int:
        """
        Calculate how well the claim matches a fallacy pattern.
        Higher score = stronger match.
        """
        score = 0
        triggers = fallacy_data['triggers']
        
        # Check keyword matches
        claim_keywords = processed['keywords']
        fallacy_keywords = set(word.lower() for word in triggers.get('keywords', []))
        keyword_matches = claim_keywords.intersection(fallacy_keywords)
        score += len(keyword_matches) * 3  # Keywords worth 3 points each
        
        # Check metric matches
        claim_metrics = [m.lower() for m in processed['metrics_found']]
        fallacy_metrics = [m.lower() for m in triggers.get('metrics', [])]
        
        for metric in claim_metrics:
            if metric in fallacy_metrics or 'any metric' in fallacy_metrics:
                score += 5  # Metrics worth 5 points each
        
        # Check pattern matches
        claim_text_lower = processed['original_claim'].lower()
        fallacy_patterns = triggers.get('patterns', [])
        
        for pattern in fallacy_patterns:
            if pattern.lower() in claim_text_lower:
                score += 2  # Patterns worth 2 points each
        
        # Bonus for action words (indicates recommendation)
        if processed['has_recommendation'] and 'reallocate' in triggers.get('keywords', []):
            score += 3
        
        return score
    
    def _score_to_confidence(self, score: int) -> str:
        """Convert numeric score to confidence level."""
        if score >= 15:
            return "HIGH"
        elif score >= 8:
            return "MEDIUM"
        elif score >= 3:
            return "LOW"
        else:
            return "NONE"


# Test function
if __name__ == "__main__":
    detector = FallacyDetector()
    
    # Test with your first claim
    test_claim = """Since campaigns with a ROAS above 4.0 represent our most efficient spend, 
    we should immediately reallocate 30% of the budget from underperforming 'Brand' campaigns 
    (ROAS < 2.0) to these high-performers to maximize total profit."""
    
    print("=" * 70)
    print("FALLACY DETECTOR TEST")
    print("=" * 70)
    print(f"\nAnalyzing Claim:\n{test_claim}\n")
    
    detected_fallacies = detector.detect(test_claim)
    
    if detected_fallacies:
        print(f"Found {len(detected_fallacies)} potential fallacy/fallacies:\n")
        
        for i, fallacy in enumerate(detected_fallacies, 1):
            print(f"{i}. {fallacy['fallacy_name']} (Confidence: {fallacy['confidence']})")
            print(f"   Score: {fallacy['match_score']}")
            print(f"   Description: {fallacy['description']}")
            print()
    else:
        print("No fallacies detected.")
    
    print("=" * 70)