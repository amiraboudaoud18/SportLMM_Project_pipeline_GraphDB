#!/usr/bin/env python3
"""
add_ragas_scores.py - FIXED VERSION

Adds RAGAS scores to an existing evaluation results file.
Compatible with RAGAS v0.2+ and latest OpenAI API.
"""

import json
import sys
import os
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for OpenAI API key FIRST
if not os.getenv('OPENAI_API_KEY'):
    print("\n❌ OPENAI_API_KEY not found!")
    print("   Set it in .env file or:")
    print("   export OPENAI_API_KEY=sk-your-key-here")
    sys.exit(1)

print(f"✅ OpenAI API Key found: {os.getenv('OPENAI_API_KEY')[:15]}...")

# Import RAGAS and dependencies
try:
    print("📦 Loading RAGAS libraries...")
    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy, context_precision, answer_correctness
    from datasets import Dataset
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    print("✅ RAGAS libraries loaded")
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    print("\n📦 Install required packages:")
    print("   pip install --upgrade ragas datasets langchain-openai openai")
    sys.exit(1)


def add_ragas_to_results(results_file: str):
    """Add RAGAS scores to existing evaluation results"""
    
    print("\n" + "="*80)
    print("🎯 ADDING RAGAS SCORES TO EXISTING RESULTS")
    print("="*80)
    
    print(f"\n📂 Loading results from: {results_file}")
    
    # Load existing results
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            results_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {results_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON file: {results_file}")
        sys.exit(1)
    
    # Get successful results
    all_results = results_data.get('results', [])
    successful = [r for r in all_results if r.get('success', False)]
    
    print(f"✅ Loaded {len(all_results)} results ({len(successful)} successful)")
    
    if not successful:
        print("❌ No successful results to evaluate!")
        sys.exit(1)
    
    # Prepare data for RAGAS
    print("\n📊 Preparing data for RAGAS evaluation...")
    
    data = {
        'question': [],
        'answer': [],
        'contexts': [],
        'ground_truth': []
    }
    
    for result in successful:
        data['question'].append(result['question'])
        data['answer'].append(result['generated_answer'])
        # RAGAS expects contexts as list of strings
        context = result.get('context', '')
        data['contexts'].append([str(context)] if context else [''])
        data['ground_truth'].append(result['ground_truth'])
    
    dataset = Dataset.from_dict(data)
    
    print(f"✅ Prepared {len(data['question'])} questions for evaluation")
    
    # Initialize OpenAI components
    print("\n🔧 Initializing OpenAI components...")
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.getenv('OPENAI_API_KEY')
        )
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv('OPENAI_API_KEY')
        )
        print("✅ OpenAI components initialized")
    except Exception as e:
        print(f"❌ Failed to initialize OpenAI: {e}")
        print("\n💡 Check:")
        print("   1. API key is valid")
        print("   2. You have OpenAI credits")
        print("   3. Internet connection works")
        sys.exit(1)
    
    # Run RAGAS evaluation
    print("\n🚀 Running RAGAS evaluation...")
    print("   Model: gpt-4o-mini (faster & cheaper)")
    print("   Embeddings: text-embedding-3-small")
    print("   This will take 5-10 minutes...")
    print("   Cost: ~$0.50-$1.00 for 51 questions")
    print("")
    
    try:
        result = evaluate(
            dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                answer_correctness
            ],
            llm=llm,
            embeddings=embeddings,
            raise_exceptions=False  # Don't stop on individual failures
        )
        
        # Convert to dict
        if hasattr(result, 'to_pandas'):
            scores_df = result.to_pandas()
            # Get mean scores for each metric
            scores = {
                col: float(scores_df[col].mean()) 
                for col in scores_df.columns 
                if col in ['faithfulness', 'answer_relevancy', 'context_precision', 'answer_correctness']
            }
        else:
            scores = dict(result)
        
        print("\n✅ RAGAS Evaluation Complete!")
        print("\n📊 RAGAS Scores:")
        for metric, score in scores.items():
            print(f"   {metric}: {score:.4f}")
        
        # Add to results data
        results_data['ragas_scores'] = scores
        
        # Save updated results
        print(f"\n💾 Saving updated results to: {results_file}")
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        print("\n✅ SUCCESS! RAGAS scores added to results file!")
        print(f"   File updated: {results_file}")
        
        # Show summary
        print("\n" + "="*80)
        print("📊 FINAL SUMMARY")
        print("="*80)
        config = results_data['metadata']['model_config']
        stats = results_data['statistics']
        
        print(f"\nConfiguration:")
        print(f"   SPARQL: {config['sparql_model']}")
        print(f"   Answer: {config['answer_model']}")
        
        print(f"\nPerformance:")
        print(f"   Success Rate: {stats['success_rate']:.1f}%")
        print(f"   Average Time: {stats['average_time']:.2f}s")
        
        print(f"\nRAGAS Quality Scores:")
        for metric, score in scores.items():
            rating = "🏆" if score > 0.90 else "⭐" if score > 0.85 else "✅" if score > 0.75 else "⚠️"
            print(f"   {metric}: {score:.4f} {rating}")
        
        print("\n" + "="*80)
        print("✅ Done! You can now compare this with other model configurations!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ RAGAS evaluation failed!")
        print(f"   Error: {e}")
        print(f"   Type: {type(e).__name__}")
        
        import traceback
        print("\n📋 Full error trace:")
        traceback.print_exc()
        
        print(f"\n💡 Troubleshooting:")
        print("   1. Verify API key is valid: https://platform.openai.com/api-keys")
        print("   2. Check OpenAI credits: https://platform.openai.com/account/usage")
        print("   3. Try: pip install --upgrade openai langchain-openai ragas")
        print("   4. Check internet connection")
        sys.exit(1)


def main():
    """Main execution"""
    
    if len(sys.argv) < 2:
        print("\n" + "="*80)
        print("🎯 ADD RAGAS SCORES TO EXISTING EVALUATION")
        print("="*80)
        print("\nUsage:")
        print("   python add_ragas_scores.py <results_file.json>")
        print("\nExample:")
        print("   python add_ragas_scores.py evaluation_results/results_qwen2.5_llama_20250115_143022.json")
        print("\nRequirements:")
        print("   - OPENAI_API_KEY must be set (in .env or environment)")
        print("   - ~$0.50-$1.00 in OpenAI credits")
        print("   - Internet connection")
        print("\nThis script will:")
        print("   1. Read your existing evaluation results")
        print("   2. Run RAGAS evaluation using OpenAI")
        print("   3. Add quality scores to the same file")
        print("   4. Preserve all existing data")
        print("")
        sys.exit(1)
    
    results_file = sys.argv[1]
    add_ragas_to_results(results_file)


if __name__ == "__main__":
    main()
