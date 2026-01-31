#!/usr/bin/env python3
"""
generate_manual_evaluation.py

Runs all test questions through the chatbot and saves responses
in a clean format for manual evaluation by team members.
"""

import json
import sys
from datetime import datetime
from typing import List, Dict
from intelligent_chatbot import IntelligentEquestrianChatbot

def generate_responses(test_dataset_file: str, output_file: str = None):
    """Generate chatbot responses for all test questions"""
    
    print("\n" + "="*80)
    print("GENERATING RESPONSES FOR MANUAL EVALUATION")
    print("="*80)
    
    # Load test dataset
    print(f"\nloading test dataset: {test_dataset_file}")
    with open(test_dataset_file, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    questions = dataset.get('test_questions', [])
    print(f"Loaded {len(questions)} questions")
    
    # Initialize chatbot
    print("\nInitializing chatbot...")
    chatbot = IntelligentEquestrianChatbot()
    print("Chatbot ready!")
    
    # Prepare results structure
    results = {
        "metadata": {
            "generation_date": datetime.now().isoformat(),
            "total_questions": len(questions),
            "dataset_version": dataset.get('metadata', {}).get('version', 'unknown'),
            "model_config": {
                "sparql_model": chatbot.sparql_llm.model,
                "answer_model": chatbot.answer_llm.model
            }
        },
        "responses": []
    }
    
    # Process each question
    print(f"\nProcessing {len(questions)} questions...")
    print("="*80)
    
    for i, q in enumerate(questions, 1):
        question_id = q['question_id']
        question = q['question']
        ground_truth = q['ground_truth']
        category = q.get('category', 'unknown')
        difficulty = q.get('difficulty', 'unknown')
        
        print(f"\n[{i}/{len(questions)}] {question_id}: {question[:60]}...")
        
        try:
            # Get chatbot response
            result = chatbot.answer_question(question, verbose=False)
            
            if result['success']:
                response_data = {
                    "question_id": question_id,
                    "question": question,
                    "ground_truth": ground_truth,
                    "category": category,
                    "difficulty": difficulty,
                    "chatbot_response": {
                        "answer": result['answer'],
                        "sparql_query": result.get('sparql_query', ''),
                        "results_count": result.get('results_count', 0),
                        "response_time": result.get('response_time', 0)
                    },
                    "status": "success"
                }
                print(f"  Success ({result.get('response_time', 0):.2f}s)")
            else:
                response_data = {
                    "question_id": question_id,
                    "question": question,
                    "ground_truth": ground_truth,
                    "category": category,
                    "difficulty": difficulty,
                    "chatbot_response": {
                        "answer": result.get('answer', 'ERROR'),
                        "error": result.get('error', 'Unknown error')
                    },
                    "status": "failed"
                }
                print(f"  Failed: {result.get('error', 'Unknown')}")
        
        except Exception as e:
            response_data = {
                "question_id": question_id,
                "question": question,
                "ground_truth": ground_truth,
                "category": category,
                "difficulty": difficulty,
                "chatbot_response": {
                    "error": str(e)
                },
                "status": "error"
            }
            print(f"  Error: {e}")
        
        results['responses'].append(response_data)
    
    # Calculate statistics
    successful = [r for r in results['responses'] if r['status'] == 'success']
    results['metadata']['statistics'] = {
        "total_questions": len(questions),
        "successful": len(successful),
        "failed": len(questions) - len(successful),
        "success_rate": len(successful) / len(questions) * 100 if questions else 0
    }
    
    # Save results
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"manual_evaluation_{timestamp}.json"
    
    print(f"\n Saving results to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "="*80)
    print(" GENERATION COMPLETE")
    print("="*80)
    print(f"\nTotal Questions: {len(questions)}")
    print(f"Successful: {len(successful)} ({results['metadata']['statistics']['success_rate']:.1f}%)")
    print(f"Failed: {len(questions) - len(successful)}")
    print(f"\nResults saved to: {output_file}")
    print("\nReady for manual evaluation!")
    print("="*80 + "\n")
    
    return output_file


def create_readable_report(json_file: str, output_file: str = None):
    """Create a human-readable text report from JSON results"""
    
    # Load JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create readable report
    if output_file is None:
        output_file = json_file.replace('.json', '_readable.txt')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("="*80 + "\n")
        f.write("MANUAL EVALUATION REPORT\n")
        f.write("="*80 + "\n\n")
        
        # Metadata
        meta = data['metadata']
        f.write(f"Generation Date: {meta['generation_date']}\n")
        f.write(f"Total Questions: {meta['total_questions']}\n")
        f.write(f"SPARQL Model: {meta['model_config']['sparql_model']}\n")
        f.write(f"Answer Model: {meta['model_config']['answer_model']}\n")
        f.write(f"\nSuccess Rate: {meta['statistics']['success_rate']:.1f}%\n")
        f.write(f"Successful: {meta['statistics']['successful']}/{meta['statistics']['total_questions']}\n")
        f.write("\n" + "="*80 + "\n\n")
        
        # Each question
        for i, response in enumerate(data['responses'], 1):
            f.write(f"QUESTION {i}: {response['question_id']}\n")
            f.write("-"*80 + "\n")
            f.write(f"Question: {response['question']}\n\n")
            f.write(f"Ground Truth:\n{response['ground_truth']}\n\n")
            
            if response['status'] == 'success':
                f.write(f"Chatbot Response:\n{response['chatbot_response']['answer']}\n\n")
                f.write(f"SPARQL Query:\n{response['chatbot_response']['sparql_query']}\n\n")
                f.write(f"Results Count: {response['chatbot_response']['results_count']}\n")
                f.write(f"Response Time: {response['chatbot_response']['response_time']:.2f}s\n")
            else:
                f.write(f"FAILED\n")
                f.write(f"Error: {response['chatbot_response'].get('error', 'Unknown')}\n")
            
            f.write(f"\nCategory: {response['category']}\n")
            f.write(f"Difficulty: {response['difficulty']}\n")
            f.write("\n" + "="*80 + "\n\n")
    
    print(f" Readable report created: {output_file}")
    return output_file


def main():
    """Main execution"""
    
    if len(sys.argv) < 2:
        print("\n" + "="*80)
        print(" GENERATE MANUAL EVALUATION RESPONSES")
        print("="*80)
        print("\nUsage:")
        print("   python generate_manual_evaluation.py <test_dataset.json> [output.json]")
        print("\nExample:")
        print("   python generate_manual_evaluation.py test_dataset.json")
        print("\nThis will:")
        print("   1. Load all test questions")
        print("   2. Run each through your chatbot")
        print("   3. Save responses in JSON format")
        print("   4. Create readable text report")
        print("   5. Ready for manual evaluation by team!")
        print()
        sys.exit(1)
    
    test_dataset = sys.argv[1]
    output_json = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Generate responses
    json_file = generate_responses(test_dataset, output_json)
    
    # Create readable report
    readable_file = create_readable_report(json_file)
    
    print("\n" + "="*80)
    print("FILES CREATED")
    print("="*80)
    print(f"\n JSON (for processing): {json_file}")
    print(f" TXT (for reading): {readable_file}")
    print("\nShare these files with your team for evaluation!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
