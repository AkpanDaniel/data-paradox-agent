import sys
sys.path.insert(0, 'agent')

from challenge_generator import ChallengeGenerator

def main():
    generator = ChallengeGenerator()
    
    print("\n" + "=" * 80)
    print("DATA PARADOX AGENT - Terminal Test Interface")
    print("=" * 80)
    print("\nTesting with 3 pre-loaded claims from your analysis...\n")
    
    claims = [
        {
            'name': 'High-ROAS Budget Reallocation',
            'text': "Since campaigns with a ROAS above 4.0 represent our most efficient spend, we should immediately reallocate 30% of the budget from underperforming Brand campaigns (ROAS < 2.0) to these high-performers to maximize total profit."
        },
        {
            'name': 'CTR-to-Conversion Correlation',
            'text': "Our analysis shows that campaigns with a Click-Through Rate (CTR) above 5% consistently yield a 20% lower Cost Per Acquisition (CPA), suggesting that creative optimization is the primary lever for solving the Google Tax problem."
        },
        {
            'name': 'Platform Parity Efficiency',
            'text': "Across the 1,800 campaigns, we found that YouTube and Display ads have a significantly higher ROAS than Search ads when using a 30-day view-through attribution window. Therefore, we should transition the majority of the Search budget to Video to avoid the high competition tax on Search."
        }
    ]
    
    for i, claim_data in enumerate(claims, 1):
        print(f"\n{'#' * 80}")
        print(f"TEST CASE {i}: {claim_data['name']}")
        print(f"{'#' * 80}\n")
        
        response = generator.generate_challenges(claim_data['text'])
        formatted = generator.format_for_terminal(response)
        print(formatted)
        
        if i < len(claims):
            input("Press Enter to continue to next test case...")
    
    print("\n" + "=" * 80)
    print("All test cases complete!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()