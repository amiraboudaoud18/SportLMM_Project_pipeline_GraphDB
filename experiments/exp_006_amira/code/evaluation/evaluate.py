# evaluate.py
"""
RAGAS Evaluation Script for GraphRAG Chatbot
Evaluates quality (RAGAS metrics) + performance (speed)
"""

import json
import time
from datetime import datetime
from typing import Dict, List
import sys
import os

# Import your chatbot
from intelligent_chatbot import IntelligentEquestrianChatbot
from config import get_active_models

# RAGAS imports
try:
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_precision,
        answer_correctness
    )
    from datasets import Dataset
    RAGAS_AVAILABLE = True
except ImportError:
    print("⚠️  RAGAS not installed. Install with: pip install ragas datasets")
    RAGAS_AVAILABLE = False


class ChatbotEvaluator:
    """Evaluates chatbot with RAGAS metrics + performance"""
    
    def __init__(self, test_dataset_path: str = "test_dataset.json"):
        """Initialize evaluator"""
        print("🔧 Initializing Evaluator...")
        
        # Load test dataset
        with open(test_dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.test_questions = data['test_questions']
            self.metadata = data.get('metadata', {})
        
        print(f"Loaded {len(self.test_questions)} test questions")
        
        # Get current model configuration
        self.model_config = get_active_models()
        print("\nCurrent Configuration:")
        print(f"   SPARQL Model: {self.model_config['sparql_model']}")
        print(f"   Answer Model: {self.model_config['answer_model']}")
        
        # Initialize chatbot
        print("\n🐴 Initializing Chatbot...")
        self.chatbot = IntelligentEquestrianChatbot()
        
        # Results storage
        self.results = []
        
    def run_evaluation(self, save_results: bool = True):
        """
        Run complete evaluation on all test questions
        
        Returns:
            Dictionary with all evaluation results
        """
        print("\n" + "="*80)
        print("🚀 STARTING EVALUATION")
        print("="*80)
        
        start_time = time.time()
        
        # Run chatbot on all questions
        print(f"\n📝 Processing {len(self.test_questions)} questions...")
        
        for i, test_q in enumerate(self.test_questions, 1):
            print(f"\n[{i}/{len(self.test_questions)}] {test_q['question_id']}: {test_q['question'][:60]}...")
            
            result = self._evaluate_single_question(test_q)
            self.results.append(result)
            
            # Show quick stats
            if result['success']:
                print(f"   ✅ Success | Time: {result['performance']['total_time']:.2f}s")
            else:
                print(f"   ❌ Failed | Error: {result.get('error', 'Unknown')}")
        
        total_time = time.time() - start_time
        
        # Calculate statistics
        print("\n📊 Calculating Statistics...")
        stats = self._calculate_statistics()
        
        # Prepare final results
        final_results = {
            'metadata': {
                'evaluation_date': datetime.now().isoformat(),
                'model_config': self.model_config,
                'total_questions': len(self.test_questions),
                'total_evaluation_time': total_time
            },
            'results': self.results,
            'statistics': stats
        }
        
        # Save results
        if save_results:
            filename = self._save_results(final_results)
            print(f"\n💾 Results saved to: {filename}")
        
        # Print summary
        self._print_summary(stats, total_time)
        
        # Run RAGAS if available
        if RAGAS_AVAILABLE:
            print("\n" + "="*80)
            print("🎯 RAGAS QUALITY METRICS")
            print("="*80)
            try:
                ragas_scores = self._run_ragas_evaluation()
                final_results['ragas_scores'] = ragas_scores
                
                if save_results:
                    # Update saved file with RAGAS scores
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(final_results, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"⚠️  RAGAS evaluation skipped due to error: {e}")
                print("💡 Your performance results are still valid!")
                print("💡 To enable RAGAS: export OPENAI_API_KEY=your-key")
                final_results['ragas_scores'] = {'error': str(e), 'note': 'Performance metrics still valid'}
        
        return final_results
    
    def _evaluate_single_question(self, test_q: Dict) -> Dict:
        """Evaluate a single question"""
        
        question = test_q['question']
        ground_truth = test_q['ground_truth']
        
        # Timing
        times = {}
        
        try:
            # Total time
            start = time.time()
            
            # Run chatbot (with verbose=False for cleaner output)
            result = self.chatbot.answer_question(question, verbose=False)
            
            times['total_time'] = time.time() - start
            
            if result['success']:
                return {
                    'question_id': test_q['question_id'],
                    'question': question,
                    'ground_truth': ground_truth,
                    'generated_answer': result['answer'],
                    'context': result['context'],
                    'sparql_query': result.get('sparql_query', ''),
                    'results_count': result.get('results_count', 0),
                    'category': test_q['category'],
                    'difficulty': test_q['difficulty'],
                    'success': True,
                    'performance': {
                        'total_time': times['total_time']
                    }
                }
            else:
                return {
                    'question_id': test_q['question_id'],
                    'question': question,
                    'ground_truth': ground_truth,
                    'generated_answer': None,
                    'success': False,
                    'error': result.get('error', 'Unknown error'),
                    'category': test_q['category'],
                    'difficulty': test_q['difficulty'],
                    'performance': {
                        'total_time': times['total_time']
                    }
                }
        
        except Exception as e:
            return {
                'question_id': test_q['question_id'],
                'question': question,
                'ground_truth': ground_truth,
                'generated_answer': None,
                'success': False,
                'error': str(e),
                'category': test_q['category'],
                'difficulty': test_q['difficulty'],
                'performance': {
                    'total_time': 0
                }
            }
    
    def _calculate_statistics(self) -> Dict:
        """Calculate performance statistics"""
        
        successful = [r for r in self.results if r['success']]
        failed = [r for r in self.results if not r['success']]
        
        if not successful:
            return {
                'success_rate': 0,
                'average_time': 0,
                'by_category': {},
                'by_difficulty': {}
            }
        
        # Overall stats
        total_time = sum(r['performance']['total_time'] for r in successful)
        avg_time = total_time / len(successful)
        
        # By category
        by_category = {}
        for result in successful:
            cat = result['category']
            if cat not in by_category:
                by_category[cat] = {'count': 0, 'total_time': 0}
            by_category[cat]['count'] += 1
            by_category[cat]['total_time'] += result['performance']['total_time']
        
        for cat in by_category:
            by_category[cat]['average_time'] = by_category[cat]['total_time'] / by_category[cat]['count']
        
        # By difficulty
        by_difficulty = {}
        for result in successful:
            diff = result['difficulty']
            if diff not in by_difficulty:
                by_difficulty[diff] = {'count': 0, 'total_time': 0}
            by_difficulty[diff]['count'] += 1
            by_difficulty[diff]['total_time'] += result['performance']['total_time']
        
        for diff in by_difficulty:
            by_difficulty[diff]['average_time'] = by_difficulty[diff]['total_time'] / by_difficulty[diff]['count']
        
        return {
            'total_questions': len(self.results),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': len(successful) / len(self.results) * 100,
            'average_time': avg_time,
            'min_time': min(r['performance']['total_time'] for r in successful),
            'max_time': max(r['performance']['total_time'] for r in successful),
            'by_category': by_category,
            'by_difficulty': by_difficulty
        }
    
    def _run_ragas_evaluation(self) -> Dict:
        """Run RAGAS quality metrics"""
        
        if not RAGAS_AVAILABLE:
            return {}
        
        # Check for OpenAI API key
        import os
        if not os.getenv('OPENAI_API_KEY'):
            print("⚠️  OPENAI_API_KEY not found in environment")
            print("   Set it with: export OPENAI_API_KEY=sk-your-key-here")
            print("   Or add to .env file")
            return {'error': 'Missing OPENAI_API_KEY'}
        
        # Prepare data for RAGAS
        successful = [r for r in self.results if r['success']]
        
        if not successful:
            print("❌ No successful results to evaluate with RAGAS")
            return {}
        
        # Create dataset for RAGAS
        data = {
            'question': [r['question'] for r in successful],
            'answer': [r['generated_answer'] for r in successful],
            'contexts': [[r['context']] for r in successful],
            'ground_truth': [r['ground_truth'] for r in successful]
        }
        
        dataset = Dataset.from_dict(data)
        
        print(f"\nEvaluating {len(successful)} successful responses with RAGAS...")
        print("   Using OpenAI API for evaluation")
        print("   This may take 5-10 minutes...")
        
        try:
            # Set up OpenAI for RAGAS
            from langchain_openai import ChatOpenAI, OpenAIEmbeddings
            
            llm = ChatOpenAI(model="gpt-4o-mini")
            embeddings = OpenAIEmbeddings()
            
            # Run RAGAS evaluation with explicit LLM and embeddings
            result = evaluate(
                dataset,
                metrics=[
                    faithfulness,
                    answer_relevancy,
                    context_precision,
                    answer_correctness
                ],
                llm=llm,
                embeddings=embeddings
            )
            
            # Convert to dict
            scores = result.to_pandas().to_dict('records')[0] if hasattr(result, 'to_pandas') else dict(result)
            
            # Print scores
            print("\n✅ RAGAS Scores:")
            for metric, score in scores.items():
                print(f"   {metric}: {score:.4f}")
            
            return scores
        
        except Exception as e:
            print(f"❌ RAGAS evaluation failed: {e}")
            print(f"   Error type: {type(e).__name__}")
            print(f"\n💡 Troubleshooting:")
            print("   1. Verify OPENAI_API_KEY is valid")
            print("   2. Check OpenAI credits: https://platform.openai.com/account/usage")
            print("   3. Try: pip install --upgrade langchain-openai")
            return {'error': str(e)}
    
    def _save_results(self, results: Dict) -> str:
        """Save results to JSON file"""
        
        # Create filename with timestamp and model names
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sparql_model = self.model_config['sparql_model'].split('-')[0]  # e.g., "qwen2.5"
        answer_model = self.model_config['answer_model'].split('-')[0]  # e.g., "llama"
        
        filename = f"results_{sparql_model}_{answer_model}_{timestamp}.json"
        
        # Create results directory if not exists
        os.makedirs('evaluation_results', exist_ok=True)
        filepath = os.path.join('evaluation_results', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def _print_summary(self, stats: Dict, total_time: float):
        """Print evaluation summary"""
        
        print("\n" + "="*80)
        print("📊 EVALUATION SUMMARY")
        print("="*80)
        
        print(f"\n✅ Success Rate: {stats['success_rate']:.1f}% ({stats['successful']}/{stats['total_questions']})")
        
        if stats['successful'] > 0:
            print(f"\n⏱️  Performance:")
            print(f"   Average Time: {stats['average_time']:.2f}s")
            print(f"   Min Time: {stats['min_time']:.2f}s")
            print(f"   Max Time: {stats['max_time']:.2f}s")
            print(f"   Total Evaluation Time: {total_time:.2f}s")
            
            print(f"\n📂 By Category:")
            for cat, data in sorted(stats['by_category'].items()):
                print(f"   {cat}: {data['count']} questions, avg {data['average_time']:.2f}s")
            
            print(f"\n🎯 By Difficulty:")
            for diff, data in sorted(stats['by_difficulty'].items()):
                print(f"   {diff}: {data['count']} questions, avg {data['average_time']:.2f}s")
        
        if stats['failed'] > 0:
            print(f"\n❌ Failed: {stats['failed']} questions")
        
        print("\n" + "="*80)


def main():
    """Main execution"""
    
    print("\n" + "="*80)
    print("🐴 GRAPHRAG CHATBOT EVALUATION SYSTEM")
    print("="*80)
    
    # Check if test dataset exists
    if not os.path.exists('test_dataset.json'):
        print("❌ test_dataset.json not found!")
        print("   Please create test_dataset.json first")
        sys.exit(1)
    
    # Create evaluator
    evaluator = ChatbotEvaluator()
    
    # Run evaluation
    results = evaluator.run_evaluation(save_results=True)
    
    print("\n✅ Evaluation complete!")
    print("\n💡 Next steps:")
    print("   1. Change models in .env")
    print("   2. Run: python evaluate.py")
    print("   3. Compare results: python compare_results.py")


if __name__ == "__main__":
    main()
