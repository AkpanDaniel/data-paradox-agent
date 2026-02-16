import pandas as pd
from typing import Dict, List, Optional
import io

class DataAnalyzer:
    """
    Analyzes uploaded CSV data and validates claims against actual data.
    """
    
    def __init__(self):
        self.df = None
        self.summary_stats = None
        self.platform_col = None
        self.metric_cols = {}
    
    def load_csv(self, csv_content: bytes) -> Dict:
        """
        Load and validate CSV data.
        
        Returns dict with success status and either data summary or error message.
        """
        try:
            # Try to read CSV
            self.df = pd.read_csv(io.BytesIO(csv_content))
            
            # Detect column names (case-insensitive)
            self._detect_columns()
            
            if not self.platform_col:
                return {
                    'success': False,
                    'error': 'Could not find platform/channel column. Expected columns like: platform, channel, ad_platform, source'
                }
            
            # Generate summary stats
            self.summary_stats = self._generate_summary()
            
            return {
                'success': True,
                'rows': int(len(self.df)),
                'columns': list(self.df.columns),
                'summary': self.summary_stats
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to parse CSV: {str(e)}'
            }
    
    def _detect_columns(self):
        """Detect relevant columns (case-insensitive)."""
        cols_lower = {col.lower(): col for col in self.df.columns}
        
        # Detect platform column
        platform_keywords = ['platform', 'channel', 'ad_platform', 'source', 'medium']
        for keyword in platform_keywords:
            if keyword in cols_lower:
                self.platform_col = cols_lower[keyword]
                break
        
        # Detect metric columns
        metric_mappings = {
            'roas': ['roas', 'return_on_ad_spend', 'roi'],
            'ctr': ['ctr', 'click_through_rate', 'clickthrough_rate'],
            'cpc': ['cpc', 'cost_per_click'],
            'cpa': ['cpa', 'cost_per_acquisition', 'cost_per_action'],
            'conversions': ['conversions', 'conv', 'purchases'],
            'spend': ['spend', 'cost', 'budget', 'investment'],
            'revenue': ['revenue', 'sales', 'income']
        }
        
        for metric_name, keywords in metric_mappings.items():
            for keyword in keywords:
                if keyword in cols_lower:
                    self.metric_cols[metric_name] = cols_lower[keyword]
                    break
    
    def _generate_summary(self) -> Dict:
        """Generate summary statistics by platform."""
        if not self.platform_col:
            return {}
        
        summary = {
            'by_platform': {},
            'overall': {}
        }
        
        # Group by platform
        grouped = self.df.groupby(self.platform_col)
        
        for platform, group in grouped:
            platform_stats = {'count': int(len(group))}
            
            # Calculate metrics
            for metric_name, col_name in self.metric_cols.items():
                if col_name in group.columns:
                    platform_stats[metric_name] = {
                        'mean': float(round(group[col_name].mean(), 2)),
                        'median': float(round(group[col_name].median(), 2)),
                        'min': float(round(group[col_name].min(), 2)),
                        'max': float(round(group[col_name].max(), 2))
                    }
            
            summary['by_platform'][str(platform)] = platform_stats
        
        # Overall stats
        for metric_name, col_name in self.metric_cols.items():
            if col_name in self.df.columns:
                summary['overall'][metric_name] = {
                    'mean': float(round(self.df[col_name].mean(), 2)),
                    'median': float(round(self.df[col_name].median(), 2)),
                    'min': float(round(self.df[col_name].min(), 2)),
                    'max': float(round(self.df[col_name].max(), 2))
                }
        
        return summary
    
    def validate_claim(self, claim_text: str) -> Dict:
        """
        Validate a claim against the loaded data.
        
        Returns verification results.
        """
        if self.df is None:
            return {
                'verified': False,
                'message': 'No data loaded. Upload CSV first.'
            }
        
        claim_lower = claim_text.lower()
        verifications = []
        
        # Check for platform mentions
        for platform in self.summary_stats['by_platform'].keys():
            if platform.lower() in claim_lower:
                verifications.append({
                    'type': 'platform_detected',
                    'platform': platform,
                    'stats': self.summary_stats['by_platform'][platform]
                })
        
        # Check for metric claims (e.g., "ROAS is 9.5")
        import re
        for metric_name, col_name in self.metric_cols.items():
            # Look for patterns like "ROAS is 9.5" or "ROAS: 9.5"
            patterns = [
                rf'{metric_name}\s*(?:is|:|=)\s*(\d+\.?\d*)',
                rf'{metric_name}\s*(?:of|at)\s*(\d+\.?\d*)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, claim_lower)
                if match:
                    claimed_value = float(match.group(1))
                    
                    # Find what platforms match this value
                    matching_platforms = []
                    for platform, stats in self.summary_stats['by_platform'].items():
                        if metric_name in stats:
                            actual_mean = stats[metric_name]['mean']
                            actual_max = stats[metric_name]['max']
                            
                            # Check if claimed value is close to actual
                            if abs(claimed_value - actual_mean) < 0.5:
                                matching_platforms.append({
                                    'platform': platform,
                                    'actual_value': actual_mean,
                                    'match_type': 'mean'
                                })
                            elif abs(claimed_value - actual_max) < 0.5:
                                matching_platforms.append({
                                    'platform': platform,
                                    'actual_value': actual_max,
                                    'match_type': 'max'
                                })
                    
                    verifications.append({
                        'type': 'metric_claim',
                        'metric': metric_name,
                        'claimed_value': claimed_value,
                        'matching_platforms': matching_platforms
                    })
        
        return {
            'verified': len(verifications) > 0,
            'verifications': verifications,
            'summary': self.summary_stats
        }
    
    def get_platform_comparison(self, metric: str = 'roas') -> Dict:
        """Get platform comparison for a specific metric."""
        if not self.summary_stats or metric not in self.metric_cols:
            return {}
        
        comparison = {}
        for platform, stats in self.summary_stats['by_platform'].items():
            if metric in stats:
                comparison[platform] = stats[metric]['mean']
        
        # Sort by value
        sorted_comparison = dict(sorted(comparison.items(), key=lambda x: x[1], reverse=True))
        
        return sorted_comparison


# Test function
if __name__ == "__main__":
    analyzer = DataAnalyzer()
    
    # Test with sample CSV path (you'd replace this)
    print("Data Analyzer module ready for testing")