import re
from typing import Dict, List, Set

class InputProcessor:
    """
    Extracts key information from user's analytical claim.
    Identifies metrics, action words, and patterns for fallacy detection.
    """
    
    def __init__(self):
        # Common metrics in marketing analytics
        self.known_metrics = [
            'ROAS', 'ROI', 'CPA', 'CTR', 'CPC', 'CPM', 'conversion rate',
            'click-through rate', 'cost per acquisition', 'return on ad spend',
            'cost per click', 'engagement rate', 'bounce rate', 'CAC'
        ]
        
        # Action words that suggest recommendations
        self.action_words = [
            'should', 'reallocate', 'shift', 'move', 'increase', 'decrease',
            'optimize', 'scale', 'reduce', 'allocate', 'invest', 'cut',
            'transition', 'switch', 'change', 'adjust'
        ]
        
        # Comparison indicators
        self.comparison_words = [
            'better', 'worse', 'higher', 'lower', 'more', 'less',
            'superior', 'inferior', 'outperform', 'underperform',
            'vs', 'versus', 'compared to', 'than'
        ]
    
    def process(self, claim_text: str) -> Dict:
        """
        Process the claim and extract structured information.
        
        Args:
            claim_text: The user's analytical claim
            
        Returns:
            Dictionary with extracted information
        """
        claim_lower = claim_text.lower()
        
        result = {
            'original_claim': claim_text,
            'metrics_found': self._extract_metrics(claim_lower),
            'action_words_found': self._extract_action_words(claim_lower),
            'comparison_words_found': self._extract_comparison_words(claim_lower),
            'has_recommendation': self._has_recommendation(claim_lower),
            'has_comparison': self._has_comparison(claim_lower),
            'keywords': self._extract_all_keywords(claim_lower)
        }
        
        return result
    
    def _extract_metrics(self, text: str) -> List[str]:
        """Extract marketing metrics mentioned in the text."""
        found_metrics = []
        for metric in self.known_metrics:
            if metric.lower() in text:
                found_metrics.append(metric)
        return list(set(found_metrics))  # Remove duplicates
    
    def _extract_action_words(self, text: str) -> List[str]:
        """Extract action/recommendation words."""
        found_actions = []
        for action in self.action_words:
            if re.search(r'\b' + re.escape(action) + r'\b', text):
                found_actions.append(action)
        return found_actions
    
    def _extract_comparison_words(self, text: str) -> List[str]:
        """Extract comparison indicators."""
        found_comparisons = []
        for comp in self.comparison_words:
            if re.search(r'\b' + re.escape(comp) + r'\b', text):
                found_comparisons.append(comp)
        return found_comparisons
    
    def _has_recommendation(self, text: str) -> bool:
        """Check if the claim contains a recommendation."""
        return any(action in text for action in self.action_words)
    
    def _has_comparison(self, text: str) -> bool:
        """Check if the claim makes a comparison."""
        return any(comp in text for comp in self.comparison_words)
    
    def _extract_all_keywords(self, text: str) -> Set[str]:
        """Extract all significant keywords for pattern matching."""
        # Split into words and filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been'}
        words = re.findall(r'\b\w+\b', text)
        keywords = {word for word in words if word not in stop_words and len(word) > 2}
        return keywords


# Test function
if __name__ == "__main__":
    # Test with your first claim
    processor = InputProcessor()
    
    test_claim = """Since campaigns with a ROAS above 4.0 represent our most efficient spend, 
    we should immediately reallocate 30% of the budget from underperforming 'Brand' campaigns 
    (ROAS < 2.0) to these high-performers to maximize total profit."""
    
    result = processor.process(test_claim)
    
    print("=" * 60)
    print("INPUT PROCESSOR TEST")
    print("=" * 60)
    print(f"\nOriginal Claim:\n{test_claim}\n")
    print(f"Metrics Found: {result['metrics_found']}")
    print(f"Action Words: {result['action_words_found']}")
    print(f"Comparison Words: {result['comparison_words_found']}")
    print(f"Has Recommendation: {result['has_recommendation']}")
    print(f"Has Comparison: {result['has_comparison']}")
    print(f"\nKeywords Extracted: {result['keywords']}")
    print("=" * 60)