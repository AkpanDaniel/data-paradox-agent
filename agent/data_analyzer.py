import polars as pl
from typing import Dict, List, Optional
import io

class DataAnalyzer:
    """
    Analyzes uploaded CSV data and validates claims against actual data.
    Uses Polars instead of Pandas for better compatibility.
    """
    
    def __init__(self):
        self.df = None
        self.summary_stats = None
        self.platform_col = None
        self.metric_cols = {}
    
    def load_csv(self, csv_content: bytes) -> Dict:
        """Load and validate CSV data."""
        try:
            self.df = pl.read_csv(io.BytesIO(csv_content))
            self._detect_columns()
            
            if not self.platform_col:
                return {
                    'success': False,
                    'error': 'Could not find platform/channel column'
                }
            
            self.summary_stats = self._generate_summary()
            
            return {
                'success': True,
                'rows': int(len(self.df)),
                'columns': list(self.df.columns),
                'summary': self.summary_stats
            }
        except Exception as e:
            return {'success': False, 'error': f'Failed to parse CSV: {str(e)}'}
    
    def _detect_columns(self):
        """Detect relevant columns (case-insensitive)."""
        cols_lower = {col.lower(): col for col in self.df.columns}
        
        platform_keywords = ['platform', 'channel', 'ad_platform', 'source', 'medium']
        for keyword in platform_keywords:
            if keyword in cols_lower:
                self.platform_col = cols_lower[keyword]
                break
        
        metric_mappings = {
            'roas': ['roas', 'return_on_ad_spend', 'roi'],
            'ctr': ['ctr', 'click_through_rate'],
            'cpc': ['cpc', 'cost_per_click'],
            'cpa': ['cpa', 'cost_per_acquisition'],
            'conversions': ['conversions', 'conv', 'purchases'],
            'spend': ['spend', 'cost', 'budget'],
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
        
        summary = {'by_platform': {}, 'overall': {}}
        
        platforms = self.df[self.platform_col].unique().to_list()

for platform in platforms:
    group = self.df.filter(pl.col(self.platform_col) == platform)
    platform_stats = {'count': int(len(group))}
            
for metric_name, col_name in self.metric_cols.items():
                if col_name in group.columns:
                    platform_stats[metric_name] = {
                        'mean': float(round(group[col_name].mean(), 2)),
                        'median': float(round(group[col_name].median(), 2)),
                        'min': float(round(group[col_name].min(), 2)),
                        'max': float(round(group[col_name].max(), 2))
                    }
            
            summary['by_platform'][str(platform)] = platform_stats
        
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
        """Validate a claim against the loaded data."""
        if self.df is None:
            return {'verified': False, 'message': 'No data loaded'}
        
        claim_lower = claim_text.lower()
        verifications = []
        
        for platform in self.summary_stats['by_platform'].keys():
            if platform.lower() in claim_lower:
                verifications.append({
                    'type': 'platform_detected',
                    'platform': platform,
                    'stats': self.summary_stats['by_platform'][platform]
                })
        
        import re
        for metric_name, col_name in self.metric_cols.items():
            patterns = [
                rf'{metric_name}\s*(?:is|:|=)\s*(\d+\.?\d*)',
                rf'{metric_name}\s*(?:of|at)\s*(\d+\.?\d*)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, claim_lower)
                if match:
                    claimed_value = float(match.group(1))
                    matching_platforms = []
                    
                    for platform, stats in self.summary_stats['by_platform'].items():
                        if metric_name in stats:
                            actual_mean = stats[metric_name]['mean']
                            actual_max = stats[metric_name]['max']
                            
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