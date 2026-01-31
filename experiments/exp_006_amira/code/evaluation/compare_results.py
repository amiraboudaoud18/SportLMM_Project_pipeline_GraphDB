# compare_results.py
"""
Compare evaluation results from different model configurations
Generates comparison tables and recommendations
"""

import json
import os
import glob
from typing import List, Dict
from datetime import datetime
import statistics


class ResultsComparator:
    """Compares evaluation results from multiple configurations"""
    
    def __init__(self, results_dir: str = "evaluation_results"):
        """Initialize comparator"""
        self.results_dir = results_dir
        self.results_files = []
        self.results_data = []
        
    def load_all_results(self):
        """Load all result files from directory"""
        
        if not os.path.exists(self.results_dir):
            print(f"❌ Directory {self.results_dir} not found!")
            return False
        
        # Find all JSON files
        pattern = os.path.join(self.results_dir, "results_*.json")
        self.results_files = glob.glob(pattern)
        
        if not self.results_files:
            print(f"❌ No result files found in {self.results_dir}")
            print("   Run evaluate.py first to generate results!")
            return False
        
        print(f"📂 Found {len(self.results_files)} result files:")
        
        # Load each file
        for filepath in self.results_files:
            filename = os.path.basename(filepath)
            print(f"   - {filename}")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.results_data.append({
                    'filename': filename,
                    'filepath': filepath,
                    'data': data
                })
        
        return True
    
    def compare(self):
        """Generate comparison report"""
        
        if not self.results_data:
            print("❌ No results loaded. Run load_all_results() first!")
            return
        
        print("\n" + "="*80)
        print("📊 COMPARISON REPORT")
        print("="*80)
        
        # Comparison table
        self._print_comparison_table()
        
        # RAGAS scores comparison
        self._print_ragas_comparison()
        
        # Performance by category
        self._print_category_comparison()
        
        # Recommendations
        self._print_recommendation()
        
        # Save comparison report
        self._save_comparison_report()
    
    def _print_comparison_table(self):
        """Print main comparison table"""
        
        print("\n📈 OVERALL PERFORMANCE COMPARISON")
        print("="*80)
        
        # Table header
        print(f"{'Configuration':<30} {'Success Rate':<15} {'Avg Time':<12} {'Min/Max Time':<15}")
        print("-"*80)
        
        for result in self.results_data:
            config = result['data']['metadata']['model_config']
            stats = result['data']['statistics']
            
            # Extract model names
            sparql_model = config['sparql_model'].split('-')[0]
            answer_model = config['answer_model'].split('-')[0]
            config_name = f"{sparql_model} + {answer_model}"
            
            # Stats
            success_rate = f"{stats['success_rate']:.1f}%"
            avg_time = f"{stats['average_time']:.2f}s"
            min_max = f"{stats['min_time']:.1f}s / {stats['max_time']:.1f}s"
            
            print(f"{config_name:<30} {success_rate:<15} {avg_time:<12} {min_max:<15}")
    
    def _print_ragas_comparison(self):
        """Print RAGAS scores comparison"""
        
        print("\n🎯 RAGAS QUALITY SCORES")
        print("="*80)
        
        # Check if RAGAS scores available
        ragas_results = [r for r in self.results_data if 'ragas_scores' in r['data'] and r['data']['ragas_scores']]
        
        if not ragas_results:
            print("⚠️  No RAGAS scores available")
            print("   Install RAGAS: pip install ragas datasets")
            return
        
        # Table header
        metrics = ['faithfulness', 'answer_relevancy', 'context_precision', 'answer_correctness']
        header = f"{'Configuration':<30}"
        for metric in metrics:
            header += f" {metric[:12]:<13}"
        print(header)
        print("-"*80)
        
        for result in ragas_results:
            config = result['data']['metadata']['model_config']
            scores = result['data']['ragas_scores']
            
            sparql_model = config['sparql_model'].split('-')[0]
            answer_model = config['answer_model'].split('-')[0]
            config_name = f"{sparql_model} + {answer_model}"
            
            row = f"{config_name:<30}"
            for metric in metrics:
                score = scores.get(metric, 0)
                row += f" {score:>12.4f}"
            print(row)
        
        # Calculate averages
        print("-"*80)
        avg_row = f"{'AVERAGE':<30}"
        for metric in metrics:
            scores = [r['data']['ragas_scores'].get(metric, 0) for r in ragas_results]
            avg = statistics.mean(scores) if scores else 0
            avg_row += f" {avg:>12.4f}"
        print(avg_row)
    
    def _print_category_comparison(self):
        """Print performance by category"""
        
        print("\n📂 PERFORMANCE BY CATEGORY")
        print("="*80)
        
        # Collect all categories
        all_categories = set()
        for result in self.results_data:
            categories = result['data']['statistics']['by_category'].keys()
            all_categories.update(categories)
        
        for category in sorted(all_categories):
            print(f"\n{category}:")
            print("-"*80)
            print(f"{'Configuration':<30} {'Questions':<12} {'Avg Time':<12} {'Success Rate':<15}")
            print("-"*80)
            
            for result in self.results_data:
                config = result['data']['metadata']['model_config']
                cat_stats = result['data']['statistics']['by_category'].get(category, {})
                
                if not cat_stats:
                    continue
                
                sparql_model = config['sparql_model'].split('-')[0]
                answer_model = config['answer_model'].split('-')[0]
                config_name = f"{sparql_model} + {answer_model}"
                
                count = cat_stats.get('count', 0)
                avg_time = f"{cat_stats.get('average_time', 0):.2f}s"
                
                print(f"{config_name:<30} {count:<12} {avg_time:<12}")
    
    def _print_recommendation(self):
        """Print recommendation based on results"""
        
        print("\n🏆 RECOMMENDATION")
        print("="*80)
        
        # Find best configuration
        best_success = max(self.results_data, key=lambda r: r['data']['statistics']['success_rate'])
        best_speed = min(self.results_data, key=lambda r: r['data']['statistics']['average_time'])
        
        # Check if RAGAS available
        ragas_results = [r for r in self.results_data if 'ragas_scores' in r['data'] and r['data']['ragas_scores']]
        
        if ragas_results:
            # Calculate overall RAGAS score (average of all metrics)
            for result in ragas_results:
                scores = result['data']['ragas_scores']
                if 'error' not in scores:
                    valid_scores = [v for k, v in scores.items() if isinstance(v, (int, float))]
                    result['overall_quality'] = statistics.mean(valid_scores) if valid_scores else 0
                else:
                    result['overall_quality'] = 0
            
            best_quality = max(ragas_results, key=lambda r: r.get('overall_quality', 0))
        else:
            best_quality = None
        
        # Print recommendations
        config_success = best_success['data']['metadata']['model_config']
        print(f"\n✅ Best Success Rate: {config_success['sparql_model']} + {config_success['answer_model']}")
        print(f"   Success Rate: {best_success['data']['statistics']['success_rate']:.1f}%")
        
        config_speed = best_speed['data']['metadata']['model_config']
        print(f"\n⚡ Fastest: {config_speed['sparql_model']} + {config_speed['answer_model']}")
        print(f"   Average Time: {best_speed['data']['statistics']['average_time']:.2f}s")
        
        if best_quality:
            config_quality = best_quality['data']['metadata']['model_config']
            print(f"\n🎯 Best Quality (RAGAS): {config_quality['sparql_model']} + {config_quality['answer_model']}")
            print(f"   Overall Score: {best_quality['overall_quality']:.4f}")
        
        # Overall recommendation
        print("\n💡 OVERALL RECOMMENDATION:")
        
        if best_quality and best_quality['overall_quality'] > 0:
            # Recommend based on quality if available
            if best_quality == best_success:
                print(f"   👉 {config_quality['sparql_model']} + {config_quality['answer_model']}")
                print(f"   Reason: Best quality AND success rate")
            else:
                print(f"   👉 {config_quality['sparql_model']} + {config_quality['answer_model']}")
                print(f"   Reason: Highest RAGAS quality score")
                print(f"   Trade-off: Slightly lower success rate ({best_quality['data']['statistics']['success_rate']:.1f}% vs {best_success['data']['statistics']['success_rate']:.1f}%)")
        else:
            # Recommend based on success + speed
            if best_success == best_speed:
                print(f"   👉 {config_success['sparql_model']} + {config_success['answer_model']}")
                print(f"   Reason: Best success rate AND fastest")
            else:
                # Calculate trade-off
                success_diff = best_success['data']['statistics']['success_rate'] - best_speed['data']['statistics']['success_rate']
                time_diff = best_success['data']['statistics']['average_time'] - best_speed['data']['statistics']['average_time']
                
                if success_diff > 5 or time_diff < 0.5:  # Significant success difference or small time difference
                    print(f"   👉 {config_success['sparql_model']} + {config_success['answer_model']}")
                    print(f"   Reason: Best success rate (+{success_diff:.1f}%)")
                else:
                    print(f"   👉 {config_speed['sparql_model']} + {config_speed['answer_model']}")
                    print(f"   Reason: Much faster ({time_diff:.2f}s faster)")
    
    def _save_comparison_report(self):
        """Save comparison report to file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comparison_report_{timestamp}.txt"
        filepath = os.path.join(self.results_dir, filename)
        
        # Redirect print to file
        import sys
        original_stdout = sys.stdout
        
        with open(filepath, 'w', encoding='utf-8') as f:
            sys.stdout = f
            self._print_comparison_table()
            self._print_ragas_comparison()
            self._print_category_comparison()
            self._print_recommendation()
        
        sys.stdout = original_stdout
        
        print(f"\n💾 Comparison report saved to: {filepath}")


def main():
    """Main execution"""
    
    print("\n" + "="*80)
    print("📊 EVALUATION RESULTS COMPARISON")
    print("="*80)
    
    # Create comparator
    comparator = ResultsComparator()
    
    # Load all results
    if not comparator.load_all_results():
        return
    
    # Generate comparison
    comparator.compare()
    
    print("\n✅ Comparison complete!")


if __name__ == "__main__":
    main()
