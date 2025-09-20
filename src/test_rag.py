"""
Test Script for Eugene Schwartz RAG System
Validates functionality and performance of the RAG implementation
"""

import asyncio
import time
import json
import logging
from typing import Dict, List, Any
from pathlib import Path

from rag_system import EugeneRAGSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGSystemTester:
    """Comprehensive testing suite for the RAG system"""

    def __init__(self):
        self.rag_system = EugeneRAGSystem()
        self.test_results = {}

    async def setup_test_environment(self):
        """Setup test environment"""
        logger.info("Setting up test environment...")

        # Initialize database
        setup_success = await self.rag_system.setup_database()
        if not setup_success:
            raise Exception("Failed to setup database for testing")

        logger.info("Test environment setup completed")

    async def test_pdf_extraction(self) -> Dict[str, Any]:
        """Test PDF text extraction"""
        logger.info("Testing PDF extraction...")

        pdf_path = Path("docs/Breakthrough_Advertising_-_Eugene_Schwartz.pdf")
        if not pdf_path.exists():
            return {
                "status": "skipped",
                "reason": "PDF file not found",
                "path": str(pdf_path)
            }

        start_time = time.time()
        chapters = self.rag_system.extract_text_from_pdf(str(pdf_path))
        extraction_time = time.time() - start_time

        return {
            "status": "success" if chapters else "failed",
            "chapters_extracted": len(chapters),
            "extraction_time_seconds": round(extraction_time, 2),
            "chapter_names": list(chapters.keys())[:5],  # First 5 chapters
            "avg_chapter_length": sum(len(text) for text in chapters.values()) // len(chapters) if chapters else 0
        }

    async def test_chunking_strategy(self) -> Dict[str, Any]:
        """Test semantic chunking"""
        logger.info("Testing chunking strategy...")

        # Sample text for testing
        sample_text = """
        The Five Levels of Market Sophistication

        Level 1: The Unaware Market
        At this level, your market is completely unaware that they have a problem.
        They don't know what you're selling, and they don't know why they need it.

        Level 2: The Problem-Aware Market
        Here, your market knows they have a problem, but they don't know what solutions are available.
        They are actively seeking information about their problem.

        Level 3: The Solution-Aware Market
        Your market knows about solutions to their problem, but they don't know about your specific product.
        You need to show them why your solution is different and better.
        """

        start_time = time.time()
        chunks = self.rag_system.semantic_chunking(sample_text, "Test Chapter")
        chunking_time = time.time() - start_time

        return {
            "status": "success" if chunks else "failed",
            "chunks_created": len(chunks),
            "chunking_time_ms": round(chunking_time * 1000, 2),
            "avg_chunk_length": sum(len(chunk.content) for chunk in chunks) // len(chunks) if chunks else 0,
            "categories_found": list(set(chunk.category for chunk in chunks)),
            "sample_chunk": chunks[0].content[:200] + "..." if chunks else None
        }

    async def test_embedding_generation(self) -> Dict[str, Any]:
        """Test embedding generation"""
        logger.info("Testing embedding generation...")

        test_texts = [
            "What are the 5 levels of market consciousness?",
            "How to write effective headlines",
            "PAS formula in copywriting"
        ]

        results = []
        total_time = 0

        for text in test_texts:
            start_time = time.time()
            embedding = await self.rag_system.generate_embedding(text)
            generation_time = time.time() - start_time
            total_time += generation_time

            results.append({
                "text": text,
                "success": embedding is not None,
                "embedding_size": len(embedding) if embedding else 0,
                "generation_time_ms": round(generation_time * 1000, 2)
            })

        return {
            "status": "success" if all(r["success"] for r in results) else "partial",
            "total_tests": len(test_texts),
            "successful_tests": sum(1 for r in results if r["success"]),
            "avg_generation_time_ms": round((total_time / len(test_texts)) * 1000, 2),
            "individual_results": results
        }

    async def test_book_processing(self) -> Dict[str, Any]:
        """Test complete book processing pipeline"""
        logger.info("Testing book processing...")

        pdf_path = Path("docs/Breakthrough_Advertising_-_Eugene_Schwartz.pdf")
        if not pdf_path.exists():
            return {
                "status": "skipped",
                "reason": "PDF file not found"
            }

        start_time = time.time()
        processing_success = await self.rag_system.process_eugene_book(str(pdf_path))
        processing_time = time.time() - start_time

        # Get health check to verify processing
        health_data = await self.rag_system.health_check()

        return {
            "status": "success" if processing_success else "failed",
            "processing_time_minutes": round(processing_time / 60, 2),
            "total_chunks_stored": health_data.get('total_chunks', 0),
            "category_distribution": health_data.get('category_distribution', {}),
            "database_healthy": health_data.get('database_connection', False)
        }

    async def test_retrieval_functions(self) -> Dict[str, Any]:
        """Test retrieval functions"""
        logger.info("Testing retrieval functions...")

        test_queries = [
            {
                "function": "consciousness_level_context",
                "query": "market awareness problem solution",
                "expected_category": "consciousness_theory"
            },
            {
                "function": "framework_guidance",
                "query": "sales letter structure",
                "expected_category": "frameworks"
            },
            {
                "function": "improvement_techniques",
                "query": "weak headlines",
                "expected_category": ["techniques", "examples"]
            }
        ]

        results = []

        for test_case in test_queries:
            start_time = time.time()

            if test_case["function"] == "consciousness_level_context":
                retrieval_results = await self.rag_system.get_consciousness_level_context(test_case["query"])
            elif test_case["function"] == "framework_guidance":
                retrieval_results = await self.rag_system.get_framework_guidance(test_case["query"])
            elif test_case["function"] == "improvement_techniques":
                retrieval_results = await self.rag_system.get_improvement_techniques(test_case["query"])

            retrieval_time = time.time() - start_time

            results.append({
                "function": test_case["function"],
                "query": test_case["query"],
                "results_count": len(retrieval_results),
                "retrieval_time_ms": round(retrieval_time * 1000, 2),
                "avg_similarity": round(sum(r.similarity_score for r in retrieval_results) / len(retrieval_results), 3) if retrieval_results else 0,
                "categories_returned": list(set(r.category for r in retrieval_results)),
                "success": len(retrieval_results) > 0
            })

        return {
            "status": "success" if all(r["success"] for r in results) else "partial",
            "total_tests": len(test_queries),
            "successful_tests": sum(1 for r in results if r["success"]),
            "avg_retrieval_time_ms": round(sum(r["retrieval_time_ms"] for r in results) / len(results), 2),
            "individual_results": results
        }

    async def test_performance_benchmarks(self) -> Dict[str, Any]:
        """Test performance benchmarks"""
        logger.info("Testing performance benchmarks...")

        # Performance requirements from orchestrator
        requirements = {
            "response_time_ms": 200,
            "relevance_score": 0.85,
            "context_hit_rate": 0.88
        }

        # Test concurrent requests
        concurrent_queries = [
            "consciousness level analysis",
            "copywriting frameworks",
            "headline techniques",
            "market awareness"
        ] * 5  # 20 concurrent requests

        start_time = time.time()
        tasks = [
            self.rag_system.get_consciousness_level_context(query)
            for query in concurrent_queries
        ]
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time

        # Calculate metrics
        successful_results = [r for r in results if r]
        avg_response_time = (total_time / len(concurrent_queries)) * 1000
        hit_rate = len(successful_results) / len(concurrent_queries)

        # Calculate average relevance (similarity scores)
        all_similarities = []
        for result_set in successful_results:
            if result_set:
                all_similarities.extend([r.similarity_score for r in result_set])

        avg_relevance = sum(all_similarities) / len(all_similarities) if all_similarities else 0

        return {
            "requirements": requirements,
            "measured_performance": {
                "avg_response_time_ms": round(avg_response_time, 2),
                "avg_relevance_score": round(1 - avg_relevance, 3),  # Convert distance to similarity
                "context_hit_rate": round(hit_rate, 3)
            },
            "meets_requirements": {
                "response_time": avg_response_time <= requirements["response_time_ms"],
                "relevance": (1 - avg_relevance) >= requirements["relevance_score"],
                "hit_rate": hit_rate >= requirements["context_hit_rate"]
            },
            "concurrent_requests": len(concurrent_queries),
            "total_time_seconds": round(total_time, 2)
        }

    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all tests and compile results"""
        logger.info("Starting comprehensive RAG system tests...")

        # Setup test environment
        await self.setup_test_environment()

        # Run all tests
        test_suite = {
            "pdf_extraction": await self.test_pdf_extraction(),
            "chunking_strategy": await self.test_chunking_strategy(),
            "embedding_generation": await self.test_embedding_generation(),
            "book_processing": await self.test_book_processing(),
            "retrieval_functions": await self.test_retrieval_functions(),
            "performance_benchmarks": await self.test_performance_benchmarks()
        }

        # Calculate overall health
        successful_tests = sum(1 for test in test_suite.values()
                             if test.get("status") in ["success", "partial"])
        total_tests = len(test_suite)

        overall_results = {
            "test_summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "success_rate": round(successful_tests / total_tests, 2),
                "overall_status": "healthy" if successful_tests >= total_tests * 0.8 else "needs_attention"
            },
            "individual_tests": test_suite,
            "timestamp": time.time(),
            "recommendations": self._generate_recommendations(test_suite)
        }

        return overall_results

    def _generate_recommendations(self, test_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []

        # Check PDF processing
        if test_results["pdf_extraction"]["status"] == "skipped":
            recommendations.append("Ensure Eugene Schwartz PDF is available at docs/Breakthrough_Advertising_-_Eugene_Schwartz.pdf")

        # Check performance
        perf_results = test_results.get("performance_benchmarks", {})
        meets_reqs = perf_results.get("meets_requirements", {})

        if not meets_reqs.get("response_time", True):
            recommendations.append("Consider optimizing database indexes or embedding model for faster retrieval")

        if not meets_reqs.get("relevance", True):
            recommendations.append("Review chunking strategy to improve semantic relevance")

        if not meets_reqs.get("hit_rate", True):
            recommendations.append("Increase chunk overlap or review embedding model performance")

        # Check book processing
        book_proc = test_results.get("book_processing", {})
        if book_proc.get("total_chunks_stored", 0) < 100:
            recommendations.append("Book processing may be incomplete - verify PDF content and chunking")

        if not recommendations:
            recommendations.append("All tests passing - system ready for production use")

        return recommendations

async def main():
    """Main test execution"""
    tester = RAGSystemTester()

    try:
        results = await tester.run_comprehensive_tests()

        # Print results
        print("\n" + "="*60)
        print("EUGENE SCHWARTZ RAG SYSTEM TEST RESULTS")
        print("="*60)

        # Test summary
        summary = results["test_summary"]
        print(f"\nOverall Status: {summary['overall_status'].upper()}")
        print(f"Success Rate: {summary['success_rate']*100}% ({summary['successful_tests']}/{summary['total_tests']})")

        # Individual test results
        print("\nIndividual Test Results:")
        for test_name, test_result in results["individual_tests"].items():
            status = test_result.get("status", "unknown")
            print(f"  {test_name.replace('_', ' ').title()}: {status.upper()}")

        # Recommendations
        print("\nRecommendations:")
        for i, rec in enumerate(results["recommendations"], 1):
            print(f"  {i}. {rec}")

        # Performance metrics (if available)
        perf = results["individual_tests"].get("performance_benchmarks")
        if perf and "measured_performance" in perf:
            print("\nPerformance Metrics:")
            measured = perf["measured_performance"]
            print(f"  Average Response Time: {measured['avg_response_time_ms']}ms")
            print(f"  Average Relevance Score: {measured['avg_relevance_score']}")
            print(f"  Context Hit Rate: {measured['context_hit_rate']}")

        # Save detailed results to file
        output_file = Path("tests/rag_test_results.json")
        output_file.parent.mkdir(exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\nDetailed results saved to: {output_file}")

    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        print(f"\nTest execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())