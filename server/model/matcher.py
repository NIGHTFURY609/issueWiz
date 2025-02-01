# matcher.py
from concurrent.futures import ThreadPoolExecutor
import asyncio
import aiohttp
from typing import Dict, List
import numpy as np
from .cache import Cache
from .embeddings import EmbeddingGenerator
import logging
class IssueMatcher:
    def __init__(self):
        self.cache = Cache()
        self.embedding_generator = EmbeddingGenerator()
        self.max_workers = 5
        
    async def download_file_content(self, session, file):
        if not file.get('download_url'):  # Ensure 'download_url' exists
            logging.error(f"File does not have a valid URL: {file}")
            return None
        try:
            async with session.get(file['download_url'], timeout=5) as response:
                if response.status == 200:
                    content = await response.text()
                    return {'path': file['path'], 'content': content}
        except Exception as e:
            pass
        return None

    async def fetch_all_files(self, files):
        async with aiohttp.ClientSession() as session:
            tasks = [self.download_file_content(session, file) for file in files]
            results = await asyncio.gather(*tasks)
            return [r for r in results if r]

    def preprocess_content(self, content: str) -> str:
        # Simplified preprocessing for speed
        content = content.lower()
        # Keep only essential technical terms and patterns
        return ' '.join(word for word in content.split() 
                       if len(word) > 2 or word.isalnum())

    def calculate_similarity(self, vec1, vec2):
        return float(np.dot(vec1, vec2) / 
                    (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

    async def match_files(self, issue_data: Dict, filtered_files: List[Dict]) -> Dict:
        try:
            # Check cache first
            cache_key = self.cache.get_cache_key({
                'issue': issue_data,
                'files': [f['path'] for f in filtered_files]
            })
            
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return cached_result

            # Process issue text
            issue_text = f"{issue_data['title']} {issue_data.get('description', '')}"
            issue_embedding = self.embedding_generator.generate_embedding(issue_text)

            # Fetch file contents concurrently
            file_contents = await self.fetch_all_files(filtered_files)
            
            if not file_contents:
                return {"status": "error", "message": "No valid files to analyze"}

            # Process files in parallel
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                file_embeddings = list(executor.map(
                    lambda x: {
                        'path': x['path'],
                        'embedding': self.embedding_generator.generate_embedding(
                            self.preprocess_content(x['content'])
                        )
                    },
                    file_contents
                ))

            # Calculate similarities
            matches = []
            for file_data in file_embeddings:
                similarity = self.calculate_similarity(
                    issue_embedding.cpu().numpy(),
                    file_data['embedding'].cpu().numpy()
                )
                if similarity > 0.1:  # Minimum threshold
                    matches.append({
                        "file": file_data['path'],
                        "similarity_score": round(similarity, 2)
                    })

            # Sort and get top matches
            matches.sort(key=lambda x: x['similarity_score'], reverse=True)
            result = {
                "status": "success",
                "matches": matches[:]
            }

            # Cache the result
            self.cache.set(cache_key, result)
            
            return result

        except Exception as e:
            return {"status": "error", "message": str(e)}