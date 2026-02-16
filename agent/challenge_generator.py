from typing import List, Dict
from fallacy_detector import FallacyDetector

class ChallengeGenerator:
    """
    Takes detected fallacies and formats them into readable challenges.
    Provides both constructive and direct feedback.
    """
    
    def __init__(self):
        self.detector = FallacyDetector()
    
    def generate_challenges(self, claim_text: str, max_fallacies: int = 3) -> Dict:
        """
        Generate formatted challenges for a claim.
        
        Args:
            claim_text: The user's analytical claim
            max_fallacies: Maximum number of fallacies to include (default 3)
            
        Returns:
            Formatted challenge response
        """
        detected = self.detector.detect(claim_text)
        
        if not detected:
            return {
                'status': 'no_issues',
                'message': 'No obvious fallacies detected. However, always validate with data!'
            }
        
        # Take only top N fallacies
        top_fallacies = detected[:max_fallacies]
        
        response = {
            'status': 'challenges_found',
            'claim': claim_text,
            'fallacies_detected': len(detected),
            'challenges': []
        }
        
        for fallacy in top_fallacies:
            challenge_section = {
                'fallacy_name': fallacy['fallacy_name'],
                'confidence': fallacy['confidence'],
                'description': fallacy['description'],
                'constructive_questions': fallacy['challenges']['constructive'][:3],
                'direct_challenges': fallacy['challenges']['direct'][:3],
                'missing_data': fallacy['challenges']['missing_data'],
                'alternative_explanations': fallacy['challenges']['alternatives'][:2]
            }
            response['challenges'].append(challenge_section)
        
        return response
    
    def compare_claims(self, claim_a: str, claim_b: str) -> Dict:
        """
        Compare two claims and provide a recommendation.
        
        Args:
            claim_a: First analytical claim
            claim_b: Second analytical claim
            
        Returns:
            Comparison results with recommendation
        """
        # Analyze both claims
        response_a = self.generate_challenges(claim_a, max_fallacies=3)
        response_b = self.generate_challenges(claim_b, max_fallacies=3)
        
        # Calculate risk scores
        risk_a = self._calculate_risk_score(response_a)
        risk_b = self._calculate_risk_score(response_b)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(risk_a, risk_b)
        
        return {
            'claim_a': {
                'text': claim_a,
                'analysis': response_a,
                'risk_score': risk_a
            },
            'claim_b': {
                'text': claim_b,
                'analysis': response_b,
                'risk_score': risk_b
            },
            'recommendation': recommendation
        }
    
    def _calculate_risk_score(self, analysis: Dict) -> Dict:
        """Calculate risk score from analysis results."""
        if analysis['status'] == 'no_issues':
            return {
                'total': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
                'level': 'MINIMAL'
            }
        
        high_count = 0
        medium_count = 0
        low_count = 0
        
        for challenge in analysis.get('challenges', []):
            conf = challenge['confidence']
            if conf == 'HIGH':
                high_count += 1
            elif conf == 'MEDIUM':
                medium_count += 1
            elif conf == 'LOW':
                low_count += 1
        
        # Calculate total risk score (weighted)
        total_score = (high_count * 10) + (medium_count * 5) + (low_count * 2)
        
        # Determine risk level
        if total_score >= 20:
            risk_level = 'CRITICAL'
        elif total_score >= 12:
            risk_level = 'HIGH'
        elif total_score >= 6:
            risk_level = 'MODERATE'
        else:
            risk_level = 'LOW'
        
        return {
            'total': total_score,
            'high': high_count,
            'medium': medium_count,
            'low': low_count,
            'level': risk_level
        }
    
    def _generate_recommendation(self, risk_a: Dict, risk_b: Dict) -> Dict:
        """Generate comparison recommendation."""
        score_a = risk_a['total']
        score_b = risk_b['total']
        
        if score_a == 0 and score_b == 0:
            return {
                'winner': 'both',
                'message': 'Both claims show solid methodology with minimal logical risks.',
                'reasoning': 'Either approach appears analytically sound based on the information provided.'
            }
        
        if score_a == score_b:
            return {
                'winner': 'tie',
                'message': f'Both claims have similar risk levels ({risk_a["level"]}).',
                'reasoning': 'Consider other factors like implementation complexity, resource requirements, or strategic alignment.'
            }
        
        if score_a < score_b:
            winner = 'claim_a'
            winner_label = 'Claim A'
            loser_label = 'Claim B'
            winner_risk = risk_a
            loser_risk = risk_b
        else:
            winner = 'claim_b'
            winner_label = 'Claim B'
            loser_label = 'Claim A'
            winner_risk = risk_b
            loser_risk = risk_a
        
        # Build reasoning
        reasoning_parts = []
        
        if winner_risk['high'] < loser_risk['high']:
            reasoning_parts.append(f"{winner_label} has fewer HIGH-confidence risks ({winner_risk['high']} vs {loser_risk['high']})")
        
        if winner_risk['level'] in ['MINIMAL', 'LOW'] and loser_risk['level'] in ['HIGH', 'CRITICAL']:
            reasoning_parts.append(f"{winner_label} has {winner_risk['level']} risk while {loser_label} has {loser_risk['level']} risk")
        
        if not reasoning_parts:
            reasoning_parts.append(f"{winner_label} has a lower overall risk score ({winner_risk['total']} vs {loser_risk['total']})")
        
        reasoning = '. '.join(reasoning_parts) + '.'
        
        return {
            'winner': winner,
            'message': f'{winner_label} appears to be the lower-risk option.',
            'reasoning': reasoning
        }
    
    def format_for_terminal(self, response: Dict) -> str:
        """
        Format the response for nice terminal output.
        """
        if response['status'] == 'no_issues':
            return f"\n✅ {response['message']}\n"
        
        output = []
        output.append("\n" + "=" * 80)
        output.append("🔍 DATA PARADOX AGENT - CHALLENGE REPORT")
        output.append("=" * 80)
        output.append(f"\nYour Claim:\n{response['claim']}\n")
        output.append(f"Potential Issues Found: {response['fallacies_detected']}")
        output.append(f"Showing Top {len(response['challenges'])} Challenge(s)\n")
        
        for i, challenge in enumerate(response['challenges'], 1):
            output.append("=" * 80)
            output.append(f"\n🚨 CHALLENGE #{i}: {challenge['fallacy_name']}")
            output.append(f"Confidence: {challenge['confidence']}")
            output.append(f"\n📝 What This Means:")
            output.append(f"   {challenge['description']}\n")
            
            output.append("🟡 CONSTRUCTIVE QUESTIONS:")
            for q in challenge['constructive_questions']:
                output.append(f"   • {q}")
            
            output.append("\n🔴 DIRECT CHALLENGES:")
            for c in challenge['direct_challenges']:
                output.append(f"   • {c}")
            
            output.append("\n📊 MISSING DATA YOU SHOULD CHECK:")
            for m in challenge['missing_data']:
                output.append(f"   • {m}")
            
            output.append("\n💡 ALTERNATIVE EXPLANATIONS:")
            for a in challenge['alternative_explanations']:
                output.append(f"   • {a}")
            
            output.append("")
        
        output.append("=" * 80)
        output.append("✅ How to Strengthen Your Analysis:")
        output.append("   1. Address the missing data points identified above")
        output.append("   2. Run controlled experiments to test causality")
        output.append("   3. Consider alternative explanations before finalizing")
        output.append("=" * 80 + "\n")
        
        return "\n".join(output)


# Test function
if __name__ == "__main__":
    generator = ChallengeGenerator()
    
    # Test with your first claim
    test_claim = """Since campaigns with a ROAS above 4.0 represent our most efficient spend, 
    we should immediately reallocate 30% of the budget from underperforming 'Brand' campaigns 
    (ROAS < 2.0) to these high-performers to maximize total profit."""
    
    response = generator.generate_challenges(test_claim)
    formatted = generator.format_for_terminal(response)
    
    print(formatted)